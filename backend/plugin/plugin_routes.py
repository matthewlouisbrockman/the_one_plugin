from flask import Blueprint, request, send_from_directory, Response
from config import IS_LOCALHOST
import yaml
import dotenv
from os import getenv
dotenv.load_dotenv()


bp = Blueprint("plugin", __name__)
print('localhost started? ', IS_LOCALHOST)

AUTHO_CLIENT_URL = getenv('AUTHO_CLIENT_URL')
AUTHO_AUTHORIZATION_URL = getenv('AUTHO_AUTHORIZATION_URL')
OPENAI_VERIFICATION_TOKEN = getenv('OPENAI_VERIFICATION_TOKEN')

if not (AUTHO_CLIENT_URL and AUTHO_AUTHORIZATION_URL and OPENAI_VERIFICATION_TOKEN):
    print('WARNING: THIS WILL NOT WORK ON PRODUCTION WITHOUT AUTHO_CLIENT_URL, AUTHO_AUTHORIZATION_URL, and OPENAI_VERIFICATION_TOKEN ENV VARIABLES SET')

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
        print('rendering prod manifest')
        with open('./plugin/manifest.json', 'r') as f:
            text = f.read()
            text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
            text = text.replace("AUTHO_CLIENT_URL", AUTHO_CLIENT_URL)
            text = text.replace("AUTH0_AUTHORIZATION_URL", AUTHO_AUTHORIZATION_URL)
            text = text.replace("OPENAI_VERIFICATION_TOKEN", OPENAI_VERIFICATION_TOKEN)

    return Response(text, mimetype="text/json")

@bp.route("/.well-known/ai-plugin2.json", methods=["GET"])
def get_ai_plugin():
    host = request.headers['Host']
    with open('./plugin/manifest.json', 'r') as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        text = text.replace("AUTHO_CLIENT_URL", AUTHO_CLIENT_URL)
        text = text.replace("AUTH0_AUTHORIZATION_URL", AUTHO_AUTHORIZATION_URL)
        text = text.replace("OPENAI_VERIFICATION_TOKEN", OPENAI_VERIFICATION_TOKEN)

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
    return send_from_directory('./static', 'logo.png')
