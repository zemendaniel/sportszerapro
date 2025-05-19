from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, length


class LoginForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(min=1, max=32)])
    password = PasswordField('Jelszó', validators=[DataRequired(), length(min=4, max=32)])
    stay_logged_in = BooleanField('Maradjak bejelentkezve ezen az eszközön 30 napig?', default=True)
    submit = SubmitField('Bejelentkezés')
