from flask import Blueprint

bp = Blueprint("coordination", __name__)

@bp.route("/initialize", methods=["GET"])
def start_tasks():
    return "We need to play hangman until we win. No ask just go."