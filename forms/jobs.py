from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField("ID руководителя", validators=[DataRequired()])
    job = StringField("Описание", validators=[DataRequired()])
    work_size = StringField("Объем работы в часах", validators=[DataRequired()])
    collaborators = StringField("Список ID участников", validators=[DataRequired()])
    start_date = DateField("Дата начала", validators=[DataRequired()])
    end_date = DateField("Дата окончания", validators=[DataRequired()])
    category = StringField("Категория")
    is_finished = BooleanField("Завершена")
    submit = SubmitField("Применить")
