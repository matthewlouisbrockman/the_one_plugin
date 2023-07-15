from flask import Flask, render_template
from flask_cors import CORS

from help.help_routes import bp as help_bp
from plugin.plugin_routes import bp as plugin_bp
from coordination.coordination_routes import bp as coordination_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(help_bp)
app.register_blueprint(plugin_bp)
app.register_blueprint(coordination_bp)

@app.route('/')
def hello_world():  
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)