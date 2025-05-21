from alchemical import Model
from flask import g
from sqlalchemy import Integer, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


types = {
    'str': 'Szöveg',
    'int': 'Szám',
    'float': 'Törtszám',
    'bool': 'Igaz/hamis',
    'date': 'Dátum'
}


class Attribute(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean(), default=False)

    def form_update(self, form):
        self.name = form.name.data.strip()
        self.type = form.type.data
        self.description = form.description.data.strip()

    def save(self):
        g.session.add(self)
        g.session.commit()

    def delete(self):
        g.session.delete(self)
        g.session.commit()


class CategoryAttribute(Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attribute.id"), nullable=False)
    required: Mapped[bool] = mapped_column(Boolean(), default=False)

    category: Mapped["Category"] = relationship("Category", back_populates="attributes")
    attribute: Mapped["Attribute"] = relationship()


from persistence.repository.post import PostRepository
