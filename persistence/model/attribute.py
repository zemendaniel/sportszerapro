from typing import List

from alchemical import Model
from flask import g
from sqlalchemy import Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import delete


types = {
    'str': 'Szöveg',
    'int': 'Szám',
    'float': 'Törtszám',
    'bool': 'Igaz/hamis',
    'date': 'Dátum',
    'list': 'Lista'
}


class Attribute(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean(), default=False)
    choices: Mapped[str] = mapped_column(String(1000), nullable=True)
    category_links: Mapped[List["CategoryAttribute"]] = relationship(back_populates="attribute", cascade="all, delete-orphan")

    def form_update(self, form):
        self.name = form.name.data.strip()
        self.type = form.type.data
        self.description = form.description.data.strip()
        self.is_default = form.is_default.data
        self.choices = form.choices.data

    def save(self):
        g.session.add(self)
        if self.is_default:
            delete_from_everywhere(self)
        g.session.commit()

    def delete(self):
        g.session.delete(self)
        g.session.commit()

    @property
    def display_type(self):
        return types[self.type]

    @property
    def is_default_display(self):
        return "alapértelmezett" if self.is_default else "nem alapértelmezett"

    @property
    def choices_list(self):
        if self.type != 'list':
            return []
        else:
            return [c.strip() for c in self.choices.split(';')]


class CategoryAttribute(Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attribute.id"), nullable=False)
    # required: Mapped[bool] = mapped_column(Boolean(), default=False)

    category: Mapped["Category"] = relationship("Category", back_populates="attributes")
    attribute: Mapped["Attribute"] = relationship(back_populates="category_links")

    def save(self):
        g.session.add(self)
        g.session.commit()

    def delete(self):
        g.session.delete(self)
        g.session.commit()

    @staticmethod
    def create(category, attribute):
        obj = CategoryAttribute(category_id=category.id, attribute_id=attribute.id)
        obj.save()

    @staticmethod
    def remove(category, attribute):
        statement = (
            CategoryAttribute
            .select()
            .where(CategoryAttribute.category_id == category.id)
            .where(CategoryAttribute.attribute_id == attribute.id)
        )

        g.session.scalar(statement).delete()
        g.session.commit()

    @staticmethod
    def remove_all_attributes(category):
        statement = (
            CategoryAttribute
            .select()
            .where(CategoryAttribute.category_id == category.id)
        )

        [obj.delete() for obj in g.session.scalars(statement).all()]
        g.session.commit()


def delete_from_everywhere(attribute):
    statement = (
        delete(CategoryAttribute).where(CategoryAttribute.attribute_id == attribute.id)
    )

    g.session.execute(statement)
    g.session.commit()


from persistence.repository.post import PostRepository
