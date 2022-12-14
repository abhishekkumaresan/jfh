from flask import jsonify
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()




def todo_serializer(todo):
    """ Serialize a To-Do object to a dict """
    todo_dict = {'id': todo.id, 'task': todo.task, 'done': todo.done}
    return todo_dict


def generate_response(code, message, todo=None):
    """ Generate a Flask response with a json playload and HTTP code  """
    if todo:
        return jsonify({'code': code, 'message': message, 'todo': todo}), code
    return jsonify({'code': code, 'message': message}), code

def hash_password(password):
    return bcrypt.generate_password_hash(password)

def check_password(password,password_hash):
    return bcrypt.check_password_hash(password_hash, password) 
