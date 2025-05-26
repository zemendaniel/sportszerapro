from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField, StringField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, length, NumberRange
from wtforms.fields.choices import SelectField


class CreateListingFormMeta(FlaskForm):
    title = StringField('Hirdetés címe', validators=[DataRequired(), length(max=255)])
    intent = SelectField('Szándék', validators=[DataRequired()], choices=[('buy', 'kínál'), ('sell', 'keres')])
    condition = SelectField('Állapot', validators=[DataRequired()], choices=[('new', 'új'), ('used', 'használt'), ('bad', 'rossz')])
    description = TextAreaField('Leírás', validators=[DataRequired(), length(max=10000)])
    price = IntegerField('Ár (bruttó)', validators=[DataRequired(), NumberRange(min=0, max=10**10)])
    location = StringField('Helység', validators=[DataRequired(), length(max=255)])
