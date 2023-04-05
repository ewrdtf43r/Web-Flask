from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, HiddenField
from wtforms.validators import DataRequired, Email, length as length_valid, Regexp

class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[Email("Неправильный email")], render_kw={"required": True, "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"})
    username = StringField('Имя', validators=[DataRequired("Заполните поле логина"), length_valid(max=32)], render_kw={"required": True, "maxlength": 32})
    password = PasswordField('Пароль', validators=[DataRequired("Заполните поле пароля"), length_valid(max=32)], render_kw={"required": True, "maxlength": 32})
    form_type = HiddenField('FormType', default='')
    submit = SubmitField('Регестрация')

class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired("Заполните поле логина"), length_valid(max=32)], render_kw={"required": True, "maxlength": 32})
    password = PasswordField('Пароль', validators=[DataRequired("Заполните поле пароля"), length_valid(max=32)], render_kw={"required": True, "maxlength": 32})
    form_type = HiddenField('FormType', default='')
    submit = SubmitField('Вход')