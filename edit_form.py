from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, length as length_valid, Regexp
from flask_wtf.file import FileAllowed

class EditForm(FlaskForm):
    email = EmailField("Email", validators=[Email("Неправильный email")], render_kw={"required": True, "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"})
    password = PasswordField('Пароль', validators=[length_valid(max=32)], render_kw={"maxlength": 32})
    new_password = PasswordField('Пароль', validators=[length_valid(max=32)], render_kw={"maxlength": 32})
    about = TextAreaField('О себе', validators=[length_valid(max=512)], render_kw={"rows": 5, "cols": 50, "maxlength": 512})
    photo = FileField('Загрузите файл', validators=[FileAllowed(['jpg', 'png'], 'Только картинки')], render_kw={"accept": ".jpg, .jpeg, .png"})
    submit = SubmitField('Применить')