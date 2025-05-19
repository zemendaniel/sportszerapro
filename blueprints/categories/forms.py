from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired, length


class CreateCategoryForm(FlaskForm):
    name = TextAreaField('Név', validators=[DataRequired(), length(max=100)])
