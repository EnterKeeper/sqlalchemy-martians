import flask
from flask import jsonify

from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    "jobs_api",
    __name__,
    template_folder="templates"
)

FIELDS = ("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished", "category")


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
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({"error": "not found"})
    return jsonify(
        {
            "job": job.to_dict(only=FIELDS[1:])
        }
    )
