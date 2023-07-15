from flask import Blueprint, jsonify, g, request
from wrappers.auth_required import auth_required
from models.jobs import TOPJob
bp = Blueprint("management", __name__, url_prefix="/management")

@bp.route("/jobs", methods=["GET"])
@auth_required
def get_jobs():
    print('user info: ', g.user_id)

    jobs = TOPJob.find_by_user_id(g.user_id)

    print('jobs: ', jobs)

    return jsonify({'jobs': [job.serialize() for job in jobs]})

@bp.route("/jobs", methods=["POST"])
@auth_required
def create_job():
    payload = request.get_json()

    print('payload: ', payload)

    job_name = payload.get('job_name')
    job_description = payload.get('job_description')

    job = TOPJob(job_name, job_description, g.user_id)
    job.save()

    return jsonify({'job': job.serialize()})