from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField, StringField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, length, NumberRange
from wtforms.fields.choices import SelectField

intent_choices = {
    'buy': 'kínál',
    'sell': 'keres'
}
condition_choices = {
    'used': 'használt',
    'new': 'új',
    'bad': 'rossz'
}


class CreateListingFormMeta(FlaskForm):
    title = StringField('Hirdetés címe', validators=[DataRequired(), length(max=255)])
    intent = SelectField('Szándék', validators=[DataRequired()], choices=[(i, intent_choices[i]) for i in intent_choices.keys()])
    condition = SelectField('Állapot', validators=[DataRequired()], choices=[(i, condition_choices[i]) for i in condition_choices.keys()])
    description = TextAreaField('Leírás', validators=[DataRequired(), length(max=10000)])
    price = IntegerField('Ár (bruttó)', validators=[DataRequired(), NumberRange(min=0, max=10**10)])
    location = StringField('Helység', validators=[DataRequired(), length(max=255)])
    brand = StringField('Márka', validators=[DataRequired(), length(max=255)])
