from datetime import datetime
from typing import List

from alchemical import Model
from sqlalchemy import Integer, Text, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask import g


class Listing(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow())
    slug: Mapped[str] = mapped_column(String(500), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="listings")
    intent: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    condition: Mapped[str] = mapped_column(String(10), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    author: Mapped["User"] = relationship(back_populates="listings")

    attribute_value_links: Mapped[List["AttributeValue"]] = relationship(back_populates="listing", cascade="all, delete-orphan")

    def form_update(self, form):
        self.description = form.description.data.strip()
        self.title = form.title.data.strip()
        self.intent = form.intent.data
        self.description = form.description.data.strip()
        self.price = int(form.price.data)
        self.location = form.location.data
        self.condition = form.condition.data

    def save(self):
        g.session.add(self)
        g.session.commit()
        self.slug = f"{self.category.path_slug}/{slugify(self.title)}-{self.id}"
        g.session.commit()

    def delete(self):
        g.session.delete(self)
        g.session.commit()

    @property
    def created_at_display(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M")

    @property
    def intent_display(self):
        return intent_choices[self.intent]

    @property
    def condition_display(self):
        return condition_choices[self.condition]

    @property
    def is_owner(self):
        return self.author_id == g.user.id


from persistence.model.category import slugify
from persistence.repository.listing import ListingRepository
from blueprints.listings.forms import intent_choices, condition_choices
