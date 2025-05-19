from flask import g
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, StringField, PasswordField, HiddenField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length, EqualTo
from persistence.model.user import roles


class RegisterUserForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(max=32)])
    password = PasswordField('Jelszó', validators=[DataRequired(), length(max=32, min=4)])
    password_again = PasswordField('Jelszó újra', validators=[DataRequired(), length(max=32, min=4), EqualTo('password')])
    submit = SubmitField('Létrehozás')


class EditUserRoleForm(FlaskForm):
    # role = SelectField('Szerepkör', choices=[(role, roles[role]) for role in roles if role != 'super_admin'], validators=[DataRequired()])
    user_id = HiddenField('user_id', validators=[DataRequired()])

    def set_role(self, role_name):
        self.role.data = role_name

    def set_user_id(self, user_id):
        self.user_id.data = user_id


class UserSettingsForm(FlaskForm):
    name = StringField('Felhasználónév', validators=[DataRequired(), length(max=32)])
    submit = SubmitField('Mentés')


class UserPasswordResetForm(FlaskForm):
    old_password = PasswordField('Régi jelszó', validators=[DataRequired()])
    new_password = PasswordField('Új jelszó', validators=[DataRequired(), length(max=32, min=4)])
    new_password_again = PasswordField('Új jelszó újra', validators=[DataRequired(), length(max=32, min=4),
                                                                     EqualTo('new_password')])
    submit = SubmitField('Jelszó módosítása')


class UserDeleteForm(FlaskForm):
    password = PasswordField('Jelszó', validators=[DataRequired(), length(max=32, min=4)])
    submit = SubmitField('Fiók törlése')

