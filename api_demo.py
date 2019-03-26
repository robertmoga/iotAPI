from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "thisissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\PythonWorks\\restAPI\\todo.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


# define a decorator
def token_required(f):

    @wraps(f)  # ce face asta?
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        # here the token is valid, and I pass the token to the route
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    users = User.query.all()
    output = []

    for user in users:
        user_data = dict()
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform this operation"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': "No user found!"})

    user_data = dict()
    # user_data['id'] = user.id
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform this operation"})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    print(">> New USER : " + str(new_user.name))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message:": "New user created"})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform this operation"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "No user found"})

    user.admin = True
    db.session.commit()  # how does this commit operate that is updating db based on thi current user instance updates
    return jsonify({"message": "User has been promoted"})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({"message": "Cannot perform this operation"})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"message": "User not found"})

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Delete successful"})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:  # Check if both pass and username fields are filled
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:  # check if user is in db
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        # exp : expiration date of the token
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        print(" >> Bearer TOKEN " + str(token))
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
    data = Todo.query.filter_by(user_id=current_user.id)
    output = []

    if not data:
        return jsonify({"message": "No tasks for current user"})

    for task in data:
        task_data = dict()
        task_data['id'] = task.id
        task_data['text'] = task.text
        task_data['complete'] = task.complete
        output.append(task_data)

    return jsonify({"Todos": output})


@app.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):

    print(">> Current user id " + str(current_user.id))
    task = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()

    if not task:
        return jsonify({"message": "Task with id " + str(todo_id) + " does not exist"})

    output = dict()
    output['id'] = task.id
    output['text'] = task.text
    output['complete'] = task.complete

    return jsonify({"Task": output})


@app.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Task successfully created'})


@app.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    task = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()

    if not task:
        return jsonify({"message": "Task with id " + str(todo_id) + " does not exist"})

    task.complete = True
    db.session.commit()

    return jsonify({"message": "Task status updated"})


@app.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):

    task = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()

    if not task:
        return jsonify({"message": "Task with id " + str(todo_id) + " does not exist"})

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})




if __name__ == "__main__":
    app.run(debug=True)
