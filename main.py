import json
from flask import Flask, render_template
from database import get_db, close_db

# Blueprint Imports
from blueprints import home
from blueprints import expense
from blueprints import record
from blueprints import income
from blueprints import reports
from blueprints import auth
from blueprints import api

# Load config
with open('config.json') as f:
    config = json.load(f)

# Create Flask Application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'crm_sachinshrivastav'
app.config['TEMPLATES_AUTO_RELOAD'] = True  
app.config["UPLOADS_FOLDER"] = "static/uploads"

# Register Blueprints
app.register_blueprint(home)
app.register_blueprint(expense, url_prefix='/expense')
app.register_blueprint(record, url_prefix='/record')
app.register_blueprint(income, url_prefix='/income')
app.register_blueprint(reports, url_prefix='/reports')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.context_processor
def setting_app():
    return dict(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)