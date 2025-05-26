from flask import g


class AttributeRepository:
    @staticmethod
    def find_all():
        statement = (
            Attribute
            .select().order_by(Attribute.name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_all_not_default():
        statement = (
            Attribute
            .select()
            .where(Attribute.is_default == False).order_by(Attribute.name)
        )

        return g.session.scalars(statement).all()

    @staticmethod
    def find_by_id(attribute_id: int):
        statement = (
            Attribute
            .select()
            .where(Attribute.id == attribute_id)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_by_name_like(name: str):
        name = name.lower()
        statement = (
            Attribute
            .select()
            .where(Attribute.name.ilike(f"%{name}%")).order_by(Attribute.name)
        )

        return g.session.scalars(statement).all()


from persistence.model.attribute import Attribute
