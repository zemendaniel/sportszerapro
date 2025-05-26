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
    slug: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="listings")

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    author: Mapped["User"] = relationship(back_populates="listings")

    def form_update(self, form):
        self.description = form.description.data.strip()
        self.title = form.title.data.strip()
        self.category_id = form.category.data

    def save(self):
        self.slug = f"{self.category.path_slug}/{slugify(self.title)}-{self.id}"
        g.session.add(self)
        g.session.commit()

    def delete(self):
        g.session.delete(self)
        g.session.commit()


from persistence.model.category import slugify
from persistence.repository.listing import ListingRepository