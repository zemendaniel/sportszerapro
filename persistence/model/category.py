from alchemical import Model
from flask import g
from sqlalchemy import Integer, Text, ForeignKey, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
import re


class Category(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=True)
    path_slug: Mapped[str] = mapped_column(String(255), nullable=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    parent: Mapped["Category"] = relationship(remote_side=[id])

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

        update_slug_paths_for_descendants(self)
        g.session.commit()

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
        return CategoryRepository.find_all_ancestors(self.id)

    @property
    def is_leaf(self):
        return not self.direct_descendants()


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def build_path_slug(category):
    parts = []
    current = category
    while current:
        parts.insert(0, current.slug)
        current = current.parent

    path_slug = '/'.join(parts)

    base = path_slug
    i = 1
    while CategoryRepository.find_by_path_slug(path_slug):
        path_slug = f"{base}-{i}"
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


from persistence.repository.category import CategoryRepository
from persistence.repository.listing import ListingRepository
