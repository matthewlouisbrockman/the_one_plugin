from flask import Flask, render_template
from flask_cors import CORS

from plugin.plugin_routes import bp as plugin_bp
from coordination.coordination_routes import bp as coordination_bp
from chat_gpt_helpers.chat_gpt_helper_routes import bp as chat_gpt_helper_bp
from testing.testing_routes import bp as testing_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(plugin_bp)
app.register_blueprint(coordination_bp)
app.register_blueprint(chat_gpt_helper_bp)
app.register_blueprint(testing_bp)

@app.route('/')
def hello_world():  
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)