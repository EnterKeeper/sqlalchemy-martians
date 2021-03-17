from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests

from data import db_session
from data import jobs_api
from data import users_api
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from forms.department import DepartmentForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_long_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("index.html", title="Журнал работ", jobs=jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    title = "Регистрация"
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title=title, form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title=title, form=form,
                                   message="Такой пользователь уже существует")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect("/login")
    return render_template("register.html", title=title, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", title="Авторизация", message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/addjob", methods=["GET", "POST"])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        jobs.category = form.category.data
        current_user.jobs.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect("/")
    return render_template("jobs.html", title="Добавление работы", form=form)


@app.route("/editjob/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == job_id,
                                          (Jobs.user_author == current_user) | (current_user.id == 1)).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
            form.category.data = jobs.category
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == job_id,
                                          (Jobs.user_author == current_user) | (current_user.id == 1)).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            jobs.is_finished = form.is_finished.data
            jobs.category = form.category.data
            session.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("jobs.html", title="Редактирование работы", form=form)


@app.route("/deletejob/<int:job_id>", methods=["GET", "POST"])
@login_required
def delete_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == job_id,
                                      (Jobs.user_author == current_user) | (current_user.id == 1)).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/departments")
def departments():
    session = db_session.create_session()
    departments = session.query(Department).all()
    return render_template("departments_list.html", title="Департаменты", departments=departments)


@app.route("/adddepartment", methods=["GET", "POST"])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Department()
        department.email = form.email.data
        department.chief = form.chief.data
        department.title = form.title.data
        department.members = form.members.data
        current_user.departments.append(department)
        session.merge(current_user)
        session.commit()
        return redirect("/departments")
    return render_template("department.html", title="Добавление департамента", form=form)


@app.route("/editdepartment/<int:department_id>", methods=["GET", "POST"])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        department = session.query(Department).filter(Department.id == department_id,
                                                      (Department.user_author == current_user) |
                                                      (current_user.id == 1)).first()
        if department:
            form.email.data = department.email
            form.chief.data = department.chief
            form.title.data = department.title
            form.members.data = department.members
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        department = session.query(Department).filter(Department.id == department_id,
                                                      (Department.user_author == current_user) |
                                                      (current_user.id == 1)).first()
        if department:
            department.email = form.email.data
            department.chief = form.chief.data
            department.title = form.title.data
            department.members = form.members.data
            session.commit()
            return redirect("/departments")
        else:
            abort(404)
    return render_template("department.html", title="Редактирование департамента", form=form)


@app.route("/deletedepartment/<int:department_id>", methods=["GET", "POST"])
@login_required
def delete_department(department_id):
    session = db_session.create_session()
    department = session.query(Department).filter(Department.id == department_id,
                                                  (Department.user_author == current_user) |
                                                  (current_user.id == 1)).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect("/departments")


@app.route("/users_show/<int:user_id>")
def users_show(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    coords = requests.get("https://geocode-maps.yandex.ru/1.x", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": user.city_from,
        "format": "json"
    }).json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].replace(" ", ",")
    image_url = f"https://static-maps.yandex.ru/1.x/?ll={coords}&l=sat,skl&z=10"
    return render_template("users_show.html", title=f"{user.name} {user.surname}", user=user, image_url=image_url)


def main():
    db_session.global_init("db/martians.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
