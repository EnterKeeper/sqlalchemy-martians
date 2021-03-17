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

FIELDS = ("id", "surname", "name", "age", "position", "speciality", "address", "email", "city_from")
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


@blueprint.route("/api/users", methods=["POST"])
def create_one_user():
    data = request.json
    if not data:
        return jsonify({"error": "Empty request"})
    if not all(field in data for field in REQUIRED_FIELDS):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    field_values = {field: data[field] for field in FIELDS if field in data}
    job = User(**field_values)
    try:
        session.add(job)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"error": "ID already exists"})
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "Not found"})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def edit_one_user(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "Empty request"})
    session = db_session.create_session()
    result = session.query(User).filter(User.id == user_id).update(data)
    session.commit()
    if not result:
        return jsonify({"error": "Not found"})
    return jsonify({'success': 'OK'})
