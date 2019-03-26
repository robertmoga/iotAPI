from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from functools import wraps
import jwt
from database_controller import User

SECRET_KEY = "thisissecret"


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
           data = jwt.decode(token, SECRET_KEY)
           current_user = User.query.filter_by(id=data['id']).first()

        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# build login function for query and return token
# build a function to commit some users , see if it is possible
# build db