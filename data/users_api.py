import flask
from flask import jsonify, request
import sqlalchemy.exc

from . import db_session
from .users import User


blueprint = flask.Blueprint(
    "users_api",
    __name__,
    template_folder="templates"
)

FIELDS = ("id", "surname", "name", "age", "position", "speciality", "address", "email")
REQUIRED_FIELDS = ("surname", "name")
HASHED_PASSWORD_FIELD = "hashed_password"


@blueprint.route("/api/users")
def get_users():
    session = db_session.create_session()
    jobs = session.query(User).all()
    return jsonify(
        {
            "users": [item.to_dict(only=FIELDS) for item in jobs]
        }
    )
