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
    return jsonify({
        "users": [item.to_dict(only=FIELDS) for item in jobs]
    })


@blueprint.route("/api/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "Not found"})
    return jsonify({
        "user": user.to_dict(only=FIELDS[1:])
    })
