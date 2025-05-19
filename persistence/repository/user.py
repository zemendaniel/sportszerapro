from flask import g
from sqlalchemy import func


class UserRepository:
    @staticmethod
    def save(user):
        if user.role == 'super-admin' and UserRepository.get_super_admin().id != user.id:
            raise Exception('There can only be 1 super admin')

        g.session.add(user)
        g.session.commit()

        return user

    @staticmethod
    def get_super_admin():
        statement = (
            User.select()
            .where(User.role == 'super_admin')
        )
        return g.session.scalar(statement)

    @staticmethod
    def delete(user):
        g.session.delete(user)
        g.session.commit()

    @staticmethod
    def find_by_name(name):
        name = name.lower()
        statement = (
            User
            .select()
            .where(func.lower(User.name) == name)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_by_id(user_id):
        statement = (
            User
            .select()
            .where(User.id == user_id)
        )

        return g.session.scalar(statement)

    @staticmethod
    def find_all():
        statement = (
            User
            .select()
            .order_by(User.name)
        )

        return g.session.scalars(statement).all()


from persistence.model.user import User
