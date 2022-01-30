from flask import *
from views import views
from auth import auth
import base64
from models import db, ADDURLPUBLIC, User
from api import api
from os import path
from flask_mobility import Mobility
from flask_login import LoginManager
from flask import render_template, request, url_for, make_response
from flask_login import current_user

DB_NAME='database.db'

# Web Secrets
app=Flask(__name__)
Mobility(app)
app.config['SECRET_KEY']='nothing'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI']=base64.b64decode(b'bXlzcWwrcHlteXNxbDovL3NxbDY0NjkxNDg6cEhSWGttclAxSUBzcWw2LmZyZWVzcWxkYXRhYmFzZS5jb20vc3FsNjQ2OTE0OA==').decode("utf-8")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
# Blueprints
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(api, url_prefix='/')
# Create Database if not exist
# create_database(app)
# db.create_all()
# Login Functions
login_manager=LoginManager()
login_manager.login_view='auth.login'
login_manager.login_message='Please login to access the page'
login_manager.login_message_category='error'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.errorhandler(404)
def not_found(error):
    return make_response(render_template('404.html'), 404)

@app.errorhandler(405)
def method_error(error):
    return make_response(render_template('404.html'), 404)

def getdate(date):
	date=date.split(' ')
	return date[0]

def gettime(date):
	date=date.split(' ')
	return date[1]

app.jinja_env.globals.update(user=current_user, getdate=getdate, gettime=gettime)
if __name__=="__main__":
	app.run(host='0.0.0.0', port=80, debug=True)


