from flask import Blueprint

bp = Blueprint("help", __name__)

@bp.route("/help", methods=["GET"])
def get_help():
    return 'This is a plugin that helps to coordinate your other plugins. Let\'s see if it works!'

