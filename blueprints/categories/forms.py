from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, length


class CreateCategoryForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(max=100)])
