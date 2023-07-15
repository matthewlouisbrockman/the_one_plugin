from flask import Blueprint, jsonify, g, request
from wrappers.auth_required import auth_required
from models.jobs import TOPJob
from utils.json_helper import jsonify_payload

bp = Blueprint("management", __name__, url_prefix="/management")

@bp.route("/jobs", methods=["GET"])
@auth_required
def get_jobs():
    print('user info: ', g.user_id)

    jobs = TOPJob.find_by_user_id(g.user_id)

    print('jobs: ', [job.serialize() for job in jobs])

    return jsonify_payload({'jobs': [job.serialize() for job in jobs]})

@bp.route("/jobs", methods=["POST"])
@auth_required
def create_job():
    payload = request.get_json()

    print('payload: ', payload)

    job_name = payload.get('job_name')
    job_description = payload.get('job_description')
    job_id = payload.get('job_id')

    if not job_id:
        print('creating job')
        job = TOPJob(job_name, job_description, g.user_id)
        job.save()

    else:
        print('updating job ', job_id)
        job = TOPJob.find_by_id(job_id)
        job.update(job_name, job_description)


    return jsonify_payload({'job': job.serialize()})