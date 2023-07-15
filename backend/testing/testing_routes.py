from flask import Blueprint, jsonify

bp = Blueprint("testing", __name__, url_prefix="/testing")

@bp.route("/test", methods=["GET"])
def get_testing():
    return jsonify({'message': 'you did a test woo'})