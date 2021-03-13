from flask import Flask, render_template, redirect
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_long_secret_key"


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("index.html", title="Works log", jobs=jobs)


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
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect("/login")
    return render_template("register.html", title=title, form=form)


def main():
    db_session.global_init("db/martians.db")
    app.run()


if __name__ == '__main__':
    main()
