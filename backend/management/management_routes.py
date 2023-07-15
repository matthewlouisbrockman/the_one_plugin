from flask import Blueprint, jsonify, g
from wrappers.auth_required import auth_required
from models.jobs import TOPJob
bp = Blueprint("management", __name__, url_prefix="/management")

@bp.route("/jobs", methods=["GET"])
@auth_required
def get_jobs():
    print('user info: ', g.user_id)

    jobs = TOPJob.find_by_user_id(g.user_id)

    print('jobs: ', jobs)

    return jsonify({'jobs': [{
        'id': 1,
        'name': 'job1',
    }]})

