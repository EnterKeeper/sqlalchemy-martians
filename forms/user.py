from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    age = IntegerField("Возраст")
    position = StringField("Должность")
    speciality = StringField("Профессия")
    address = StringField("Адрес")
    submit = SubmitField("Зарегистрироваться")
