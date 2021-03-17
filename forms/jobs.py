from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField("ID руководителя", validators=[DataRequired()])
    job = StringField("Описание", validators=[DataRequired()])
    work_size = IntegerField("Объем работы в часах")
    collaborators = StringField("Список ID участников")
    start_date = DateField("Дата начала")
    end_date = DateField("Дата окончания")
    category = IntegerField("Категория")
    is_finished = BooleanField("Завершена")
    submit = SubmitField("Применить")
