from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, blueprints, make_response
from functools import wraps
from database_controller import User, db
from utils.logger import Logger
import jwt
import uuid
import datetime

# TODO: export this to a properties file
SECRET_KEY = "thisissecret"
loginService = blueprints.Blueprint('loginService', __name__)
logger = Logger(name="Login Service")

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
           print(">>> " + str(data))
           current_user = User.query.filter_by(id=data['user_id']).first()
           print(">>>>>> " + str(current_user))
        except Exception as e:
            print(">> Eror : " + str(e))
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@loginService.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        username = data['username']
        password = data['password']
    except Exception as e:
        logger.critical(" ERROR : At login the json body doesn't contain the right items " +str(e))
        # return jsonify({"Error" : " Could not verify, key elements are missing from the JSON body"}), 401
        return make_response('Could not verify, key elements are missing from the JSON body', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    try:
        user = User.query.filter_by(username=username).first()

        if not user:
            return make_response('Could not verify, wrong credentials', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, password):
            # exp : expiration of the token
            token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)}, SECRET_KEY)
            logger.info("Bearer token generated for user : {0} is {1}".format(username, token) )
            return jsonify({"token": token.decode('UTF-8')})

        return make_response('Could not verify, wrong credentials', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    except Exception as e:
        logger.critical(" ERROR : At login, unable to create a bearer token " + str(e))
        return make_response('unable to create a bearer token', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@loginService.route('/register', methods=['POST'])
def register():
    logger.info("Register endpoint accessed")
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        username = data['username']
    except Exception as e:
        logger.critical("Error - : JSON body is missing key arguments" + str(e))
        return jsonify({"Error": str("JSON body is missing key arguments: " + str(e))})

    try:
        new_user = User(id=str(uuid.uuid4()), username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        logger.critical("Error at creating a new user : " + str(e))
        return jsonify({"Error": str("Error at creating a new user : " + str(e))}), 401

    return jsonify({"message": "New user created successfully"})

# build login function for query and return token

if __name__ == "__main__":
    pass