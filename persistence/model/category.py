from typing import List

from alchemical import Model
from flask import g
from flask_wtf import FlaskForm
from sqlalchemy import Integer, Text, ForeignKey, String, func, Index, BLOB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
import re
import unicodedata
import pickle

from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, length


class Category(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=True)
    path_slug: Mapped[str] = mapped_column(String(255), nullable=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    parent: Mapped["Category"] = relationship(remote_side=[id])

    attributes: Mapped[List["CategoryAttribute"]] = relationship(back_populates="category", cascade="all, delete-orphan")
    listings: Mapped[List["Listing"]] = relationship(back_populates="category")

    __table_args__ = (
        Index('ix_category_path', 'path'),
        Index('ix_category_parent_id', 'parent_id'),
        # UniqueConstraint('path_slug', name='uq_category_path_slug'),
    )

    @property
    def ids(self):
        return [int(i) for i in self.path.split('/')]

    @property
    def actual_attributes(self):
        return [attr.attribute for attr in self.attributes]

    @hybrid_property
    def depth(self):
        return len(self.path.strip('/').split('/'))

    @depth.expression
    def depth(self):
        return (
                func.length(self.path) - func.length(func.replace(self.path, '/', ''))
        )

    def form_update(self, form):
        self.name = form.name.data.strip()

    def save(self):
        self.slug = slugify(self.name)
        g.session.add(self)
        g.session.commit()
        self.path = build_path(self)
        self.path_slug = build_path_slug(self)
        g.session.add(self)
        g.session.commit()

        update_slug_paths_for_descendants(self)
        g.session.commit()

        # delete_attributes_for_all_ancestors(self)

    def delete(self):
        handle_delete(self)
        g.session.commit()

        g.session.delete(self)
        g.session.commit()

    @property
    def direct_descendants(self):
        return CategoryRepository.find_all_direct_descendants(self.id)

    @property
    def descendants(self):
        return CategoryRepository.find_all_descendants(self.id)

    @property
    def is_root(self):
        return not self.parent_id

    @property
    def all_ancestors(self):
        return CategoryRepository.find_all_ancestors(self)
        # results = []
        # current = self.parent
        # while current:
        #     results.append(current)
        #     current = current.parent
        #
        # return results

    @property
    def whole_tree(self):
        return CategoryRepository.whole_tree_for_category(self)

    @property
    def is_leaf(self):
        return not self.direct_descendants

    @property
    def all_listings(self):
        descendant_ids = [self.id] + [cat.id for cat in CategoryRepository.find_all_descendants(self.id)]
        statement = (
            Listing
            .select()
            .where(Listing.category_id.in_(descendant_ids))
        )
        return g.session.scalars(statement).all()

    @property
    def all_attributes(self):
        # statement = (
        #     Attribute
        #     .select()
        #     .where(Attribute.is_default)
        # )
        #
        # return g.session.scalars(statement).all() + [attr.attribute for attr in self.attributes]
        return CategoryRepository.all_attributes(self)

    def attribute_is_inherited_or_default(self, attribute):
        return self.attribute_is_inherited(attribute) or self.attribute_is_default(attribute)

    def attribute_is_inherited(self, attribute):
        return attribute in self.all_attributes and attribute not in self.actual_attributes and not attribute.is_default

    def attribute_is_default(self, attribute):
        return attribute in self.all_attributes and attribute.is_default

    def attribute_reason(self, attribute):
        if self.attribute_is_inherited(attribute):
            return "örökölt"
        elif self.attribute_is_default(attribute):
            return "alapértelmezett"
        else:
            return "saját"

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, slug={self.slug}, path={self.path}, path_slug={self.path_slug})"

    def build_create_listing_form(self):
        fields = {}

        for attr in self.all_attributes:
            field_kwargs = {
                'label': attr.name,
                'validators': [DataRequired()],
            }

            if attr.type == 'small_str':
                field = StringField(
                    label=attr.name,
                    validators=[DataRequired(), length(max=255)],
                )
            elif attr.type == 'big_str':
                field = TextAreaField(
                    label=attr.name,
                    validators=[DataRequired(), length(max=10000)],
                    render_kw={'class': 'no-resize'},
                )
            elif attr.type == 'int':
                field = IntegerField(**field_kwargs)
            elif attr.type == 'float':
                field = FloatField(**field_kwargs)
            elif attr.type == 'bool':
                field = BooleanField(**field_kwargs)
            elif attr.type == 'date':
                field = DateField(**field_kwargs)
            elif attr.type == 'list':
                choices = [(c, c) for c in attr.choices_list]
                field = SelectField(**field_kwargs, choices=choices)
            else:
                continue  # Skip unknown types

            fields[f'attr_{attr.id}'] = field

        # Dynamically create the form class with the fields
        DynamicForm = type(f'CreateListingForm_Category{self.id}', (CreateListingFormMeta,), fields)

        # Return an instance of the form
        return DynamicForm()

def slugify(text):
    # Normalize: "á" → "a", etc.
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return text


def build_path_slug(category):
    parts = []
    current = category
    while current:
        parts.insert(0, slugify(current.name))
        current = current.parent

    base_path_slug = '/'.join(parts)
    path_slug = base_path_slug
    i = 1

    # Keep trying until we find a unique slug or it's the same category
    while True:
        existing = CategoryRepository.find_by_path_slug(path_slug)
        if not existing or existing.id == category.id:
            break
        path_slug = f"{base_path_slug}-{i}"
        i += 1

    return path_slug


def build_path(category):
    parts = []
    current = category
    while current:
        parts.insert(0, str(current.id))
        current = current.parent

    return '/'.join(parts)


def update_slug_paths_for_descendants(category):
    descendants = CategoryRepository.find_all_descendants(category.id)

    for desc in descendants:
        desc.path_slug = build_path_slug(desc)
        g.session.add(desc)


def handle_delete(category):
    descendants = CategoryRepository.find_all_descendants(category.id)

    for desc in descendants:
        g.session.delete(desc)
        listings = ListingRepository.find_all_by_category_id(desc.id)

        for listing in listings:
            g.session.delete(listing)

    listings = ListingRepository.find_all_by_category_id(category.id)
    for listing in listings:
        g.session.delete(listing)


def delete_attributes_for_all_ancestors(category):
    parents = CategoryRepository.find_all_ancestors(category)
    for parent in parents:
        CategoryAttribute.remove_all_attributes(parent)


def update_slug_for_all_listings(category):
    categories = [category] + CategoryRepository.find_all_descendants(category.id)

    for cat in categories:
        listings = ListingRepository.find_all_by_category_id(cat.id)

        for listing in listings:
            listing.save()


from persistence.repository.category import CategoryRepository
from persistence.repository.listing import ListingRepository
from persistence.model.listing import Listing
from persistence.model.attribute import Attribute
from persistence.model.attribute import CategoryAttribute
from blueprints.listings.forms import CreateListingFormMeta