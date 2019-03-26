from flask import Flask, request, jsonify, make_response
from services.iotAPI import iotAPI
from services.user_auth import loginService
from database_controller import db
from utils.logger import Logger
from services.user_auth import SECRET_KEY as SK
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid, jwt, datetime

# global configs
app = Flask(__name__)
app.config['SECRET_KEY'] = SK

# database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+basedir+'\\restAPI.db'
db.init_app(app)

# import services via blueprint
app.register_blueprint(iotAPI)
app.register_blueprint(loginService)

#logger
logger = Logger()

def create_database():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
    # create_database()