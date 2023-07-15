from flask import Blueprint, jsonify, g
from wrappers.auth_required import auth_required

bp = Blueprint("management", __name__, url_prefix="/management")

@bp.route("/jobs", methods=["GET"])
@auth_required
def get_jobs():
    print('user info: ', g.user_id)
    return jsonify({'jobs': [{
        'id': 1,
        'name': 'job1',
    }]})