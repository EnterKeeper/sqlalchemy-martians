import flask
from flask import jsonify, request
import sqlalchemy.exc

from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    "jobs_api",
    __name__,
    template_folder="templates"
)

FIELDS = ("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished", "category")
REQUIRED_FIELDS = ("team_leader", "category")


@blueprint.route("/api/jobs")
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            "jobs": [item.to_dict(only=FIELDS) for item in jobs]
        }
    )


@blueprint.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "job": job.to_dict(only=FIELDS[1:])
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])
def create_one_job():
    data = request.json
    if not data:
        return jsonify({"error": "Empty request"})
    if not all(field in data for field in REQUIRED_FIELDS):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    field_values = {field: data[field] for field in FIELDS if field in data}
    job = Jobs(**field_values)
    try:
        session.add(job)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"error": "Id already exists"})
    return jsonify({"success": "OK"})


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({"error": "Not found"})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})
