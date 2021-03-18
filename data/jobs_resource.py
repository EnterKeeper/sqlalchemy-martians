import flask
from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    "jobs_resource",
    __name__,
    template_folder="templates"
)
api = Api(blueprint)

FIELDS = ("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished", "category")
REQUIRED_FIELDS = ("team_leader", "category")

SUCCESS = {'success': 'OK'}


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    user = session.query(Jobs).get(job_id)
    if not user:
        abort(404, message=f"Job {job_id} not found")


parser = reqparse.RequestParser()
parser.add_argument("team_leader", required=True, type=int)
parser.add_argument("job")
parser.add_argument("work_size", type=int)
parser.add_argument("collaborators")
parser.add_argument("start_date")
parser.add_argument("end_date")
parser.add_argument("is_finished", type=bool)
parser.add_argument("category", required=True, type=int)


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({"job": job.to_dict(only=FIELDS[1:])})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify(SUCCESS)

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        data = request.json
        session.query(Jobs).filter(Jobs.id == job_id).update(data)
        session.commit()
        return jsonify(SUCCESS)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({"jobs": [job.to_dict(only=FIELDS[1:]) for job in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        data = {field: args[field] for field in FIELDS[1:]}
        job = Jobs(**data)
        session.add(job)
        session.commit()
        return jsonify(SUCCESS)


api.add_resource(JobsResource, "/api/v2/jobs/<int:job_id>")
api.add_resource(JobsListResource, "/api/v2/jobs")
