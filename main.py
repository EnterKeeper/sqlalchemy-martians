from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_long_secret_key"


def add_users():
    session = db_session.create_session()

    user = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="scott_chief@mars.org"
    )
    session.add(user)

    user = User(
        surname="Lewis",
        name="Melissa",
        age=41,
        position="commander",
        speciality="astronaut",
        address="module_4",
        email="melissa_lewis@mars.org"
    )
    session.add(user)

    user = User(
        surname="Montrose",
        name="Annie",
        age=30,
        position="pr director",
        speciality="public relations",
        address="module_3",
        email="annie_montrose@mars.org"
    )
    session.add(user)

    user = User(
        surname="Chris",
        name="Beck",
        age=36,
        position="flight surgeon astronaut",
        speciality="doctor",
        address="module_3",
        email="chris_beck@mars.org"
    )
    session.add(user)

    session.commit()


def main():
    db_session.global_init("db/martians.db")
    # app.run()
    add_users()


if __name__ == '__main__':
    main()
