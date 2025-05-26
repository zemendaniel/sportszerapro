from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.fields.simple import TextAreaField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, length, Optional
from persistence.repository.category import CategoryRepository


class CreateCategoryForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(max=100)])

