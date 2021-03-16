from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    chief = IntegerField("ID заведующего", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    members = StringField("Список ID сотрудников", validators=[DataRequired()])
    submit = SubmitField("Применить")
