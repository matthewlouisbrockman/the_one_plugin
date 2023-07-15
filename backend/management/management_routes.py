from flask import Blueprint, jsonify

bp = Blueprint("management", __name__, url_prefix="/management")

@bp.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify({'jobs': [{
        'id': 1,
        'name': 'job1',
    }]})