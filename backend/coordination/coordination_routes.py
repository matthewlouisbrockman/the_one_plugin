from flask import Blueprint, jsonify, request

bp = Blueprint("coordination", __name__)

@bp.route("/register_other_plugins", methods=["POST"])
def register_other_plugins():
  payload = request.get_json()
  print('payload: ', payload)

  return jsonify({
    "message": 'Thanks for registering! Continue to update me each time you do an action with your other plugins.'
  })

