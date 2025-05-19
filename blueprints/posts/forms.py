from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    content = TextAreaField('Tartalom', validators=[DataRequired()])

    submit = SubmitField('Létrehozás')


class EditPostForm(CreatePostForm):
    submit = SubmitField('Módosítás')
