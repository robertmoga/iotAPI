from flask import Flask, request, jsonify, make_response
from services.iotAPI import iotAPI
from database_controller import db
from utils.logger import Logger
from services.user_auth import SECRET_KEY as SK
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid, jwt, datetime

# global configs
app = Flask(__name__)
app.config['SECRET_KEY'] = SK

# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\PythonWorks\\restAPI\\restAPI.db'
db.init_app(app)

# import services via blueprint
app.register_blueprint(iotAPI)

#logger
logger = Logger()

if __name__ == "__main__":
    app.run(debug=True)
