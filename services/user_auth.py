from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, blueprints
from functools import wraps
import jwt
import uuid
from database_controller import User, db

SECRET_KEY = "thisissecret"
loginService = blueprints.Blueprint('loginService', __name__)


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


@loginService.route('/login')
def login():
    pass


@loginService.route('/register', methods=['POST'])
def register():
    print(">> Ednpoint accessed")
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
    print(">> new USER created : " + str(new_user))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created successfully"})

# build login function for query and return token

if __name__ == "__main__":
    pass