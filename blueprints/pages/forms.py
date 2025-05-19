from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields.simple import TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from werkzeug.datastructures import FileStorage
from wtforms import ValidationError
from flask_ckeditor import CKEditorField


class SetOrgNameForm(FlaskForm):
    name = TextAreaField("Név", validators=[DataRequired(), Length(max=255)])


class SetFaviconForm(FlaskForm):
    icon = FileField("Favicon - maximum 1 MB lehet, .ico és .png fájlok elfogadottak", validators=[
        FileRequired("Nincs fájl kiválasztva!"),
        FileAllowed(['ico', 'png'], 'Csak .ico és .png fájlok elfogadottak!'),
        lambda form, field: SetFaviconForm._validate_file_size(form, field, max_size=1 * 1024 * 1024)  # Max size of 1 MB
    ])

    @staticmethod
    def _validate_file_size(form, field, max_size):
        """Custom validator to limit file size."""
        file: FileStorage = field.data
        if file and len(file.read()) > max_size:
            file.seek(0)  # Reset file pointer after reading
            raise ValidationError(f"A fájl maximum 1 MB lehet!")
        file.seek(0)  # Reset file pointer after reading


class SetWelcomeTextForm(FlaskForm):
    text = CKEditorField("Szöveg")