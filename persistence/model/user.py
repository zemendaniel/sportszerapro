from typing import List

from alchemical import Model
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash


# roles = [
#     {'name': 'admin', 'access_level': 1000, 'title': 'Adminisztrátor'},
#     {'name': 'user', 'access_level': 100, 'title': 'Felhasználó'}
# ]

roles = {
    'admin': 'Adminisztrátor',
    'user': 'Felhasználó',
    'super_admin': 'Adminisztrátor'
}

class User(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    _password: Mapped[str] = mapped_column(String(180), nullable=False)
    _role: Mapped[str] = mapped_column(String(64), nullable=False)
    listings: Mapped[List["Listing"]] = relationship(back_populates="author")


    @property
    def password(self) -> None:
        return None

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role_name):
        if role_name not in roles.keys() or role_name == 'super_admin':
            raise ValueError(f'Role {role_name} is not allowed')
        self._role = role_name

    @property
    # Determines whether the user is the original admin
    def is_super_admin(self):
        return self.role == 'super_admin'

    @property
    def is_admin(self):
        return self.role in ["admin", "super_admin"]

    @property
    def role_hun(self):
        return roles[self._role]

    def check_password(self, password) -> bool:
        return check_password_hash(self._password, password)

    def save(self):
        UserRepository.save(self)

    def delete(self):
        UserRepository.delete(self)

    def form_update(self, form):
        self.name = form.name.data
        self.role = 'user'
        self.password = form.password.data


from persistence.repository.user import UserRepository
