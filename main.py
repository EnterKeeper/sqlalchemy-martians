from flask import Flask
from data import db_session

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_long_secret_key"


def main():
    db_session.global_init("db/martians.db")
    app.run()


if __name__ == '__main__':
    main()
