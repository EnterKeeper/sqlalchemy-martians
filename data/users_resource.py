import flask
from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    "users_api_v2",
    __name__,
    template_folder="templates"
)
api = Api(blueprint)

FIELDS = ("id", "surname", "name", "age", "position", "speciality", "address", "email", "city_from")
REQUIRED_FIELDS = ("surname", "name")
HASHED_PASSWORD_FIELD = "hashed_password"

SUCCESS = {'success': 'OK'}


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument("email", required=True)
parser.add_argument(HASHED_PASSWORD_FIELD, required=True)
parser.add_argument("surname", required=True)
parser.add_argument("name", required=True)
parser.add_argument("age", type=int)
parser.add_argument("position")
parser.add_argument("speciality")
parser.add_argument("address")
parser.add_argument("city_from")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({"user": user.to_dict(only=FIELDS)})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify(SUCCESS)

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        data = request.json
        if HASHED_PASSWORD_FIELD in data:
            user = session.query(User).get(user_id)
            user.set_password(data[HASHED_PASSWORD_FIELD])
            data.pop(HASHED_PASSWORD_FIELD)
        session.query(User).filter(User.id == user_id).update(data)
        session.commit()
        return jsonify(SUCCESS)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({"users": [user.to_dict(only=FIELDS[1:]) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        data = {field: args[field] for field in FIELDS[1:]}
        user = User(**data)
        user.set_password(args[HASHED_PASSWORD_FIELD])
        session.add(user)
        session.commit()
        return jsonify(SUCCESS)


api.add_resource(UserResource, "/api/v2/users/<int:user_id>")
api.add_resource(UsersListResource, "/api/v2/users")
