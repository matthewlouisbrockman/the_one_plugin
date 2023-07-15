from flask import Blueprint, jsonify, request, g, send_from_directory, Response
from config import IS_LOCALHOST
import yaml

bp = Blueprint("plugin", __name__)
print('localhost started? ', IS_LOCALHOST)

@bp.route("/.well-known/ai-plugin.json", methods=["GET"])
def get_ai_plugin():
    host = request.headers['Host']
    print('host: ', host)
    if IS_LOCALHOST:
        print('GIVING LOCALHOST YAMAL')
        with open('./plugin/manifest_local.json', 'r') as f:
            text = f.read()
            text = text.replace("PLUGIN_HOSTNAME", "http://localhost:5000")
    else:
        with open('./plugin/manifest.json', 'r') as f:
            text = f.read()
            text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
    return Response(text, mimetype="text/json")

@bp.route("/openapi.yaml", methods=["GET"])
def get_openapi():
    with open("./plugin/openapi.yaml") as f:
        host = request.headers['Host']
        text = f.read()
    if IS_LOCALHOST:
        text = text.replace("PLUGIN_HOSTNAME", "http://localhost:5000")
    else:
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")

    # load the yaml
    yaml_dict = yaml.load(text, Loader=yaml.FullLoader)
    print('yaml good')
    return Response(text, mimetype="text/yaml")

@bp.route("/logo.jpeg", methods=["GET"])
def get_logo():
    print('getting logo')
    return send_from_directory('./static', 'logo.jpeg')
