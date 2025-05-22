from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField, StringField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length
from persistence.model.attribute import types


class CreateAttributeForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(max=100)])
    type = SelectField('Típus', choices=[(t, types[t]) for t in types.keys()], validators=[DataRequired()])
    description = TextAreaField('Leírás', validators=[length(max=255)])
    is_default = BooleanField('Alapértelmezett?', default=False)
