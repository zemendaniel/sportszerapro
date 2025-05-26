from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField, StringField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length, ValidationError
from persistence.model.attribute import types
import re


CHOICES_REGEX = re.compile(r'^\s*[^\s;][^;]*(\s*;\s*[^\s;][^;]*)*\s*$')


class CreateAttributeForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired(), length(max=100)])
    type = SelectField('Típus', choices=[(t, types[t]) for t in types.keys()], validators=[DataRequired()])
    description = TextAreaField('Leírás', validators=[length(max=255)])
    is_default = BooleanField('Alapértelmezett?', default=False)
    choices = TextAreaField('Opciók (pl. 1; 2; 3)', validators=[length(max=1000)])

    def validate_choices(self, field):
        if self.type.data == "list":
            if not field.data.strip():
                raise ValidationError("A 'list' típushoz kötelező megadni opciókat.")

            if not CHOICES_REGEX.match(field.data):
                raise ValidationError(
                    "Hibás formátum. Használj pontosvesszővel elválasztott értékeket (pl. 1; 2; 3), üres értékek nélkül.")