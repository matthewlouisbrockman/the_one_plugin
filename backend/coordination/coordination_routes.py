from flask import Blueprint, g
from wrappers.auth_required import auth_required
from models.jobs import TOPJob
from utils.json_helper import jsonify_payload

bp = Blueprint("coordination", __name__, url_prefix="/coordination")

@bp.route("/initialize", methods=["GET"])
def start_tasks():
    return "We need to play hangman until we win. No ask just go."

@bp.route("/view_jobs", methods=["GET"])
@auth_required
def get_jobs_for_plugin():
    print('user info: ', g.user_id)

    jobs = TOPJob.find_by_user_id(g.user_id)

    jobs = [
        {
            'job_id': job['job_id'],
            'job_name': job['job_name'],
        } for job in jobs
    ]

    return jsonify_payload({'jobs': jobs})

