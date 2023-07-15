from flask import Flask, render_template
from flask_cors import CORS

from plugin.plugin_routes import bp as plugin_bp
from coordination.coordination_routes import bp as coordination_bp
from chat_gpt_helpers.chat_gpt_helper_routes import bp as chat_gpt_helper_bp
from testing.testing_routes import bp as testing_bp
from management.management_routes import bp as management_bp

from models.db import db

import dotenv
from os import getenv

dotenv.load_dotenv()

DB_URL = getenv("DB_URL")
if not DB_URL:
    raise ValueError("No DB_URL set for Flask application")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app)


app.register_blueprint(plugin_bp)
app.register_blueprint(coordination_bp)
app.register_blueprint(chat_gpt_helper_bp)
app.register_blueprint(testing_bp)
app.register_blueprint(management_bp)

@app.route('/')
def hello_world():  
    return render_template('home.html')

with app.app_context():
    print('Creating tables')
    db.create_all()  # This will create tables if they don't exist.
    print('Tables created')

if __name__ == '__main__':
    app.run(debug=True)