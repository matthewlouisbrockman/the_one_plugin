from flask import Flask
from flask_cors import CORS

from help.help_routes import bp as help_bp
from plugin.plugin_routes import bp as plugin_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(help_bp)
app.register_blueprint(plugin_bp)

@app.route('/')
def hello_world():  
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)