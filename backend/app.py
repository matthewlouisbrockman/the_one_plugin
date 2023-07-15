from flask import Flask
from flask_cors import CORS

import config

from plugin.plugin_routes import bp as plugin_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(plugin_bp)

@app.route('/')
def hello_world():  
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)