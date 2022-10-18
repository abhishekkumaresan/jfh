from flask_restful import  Resource

from api.utils import check_password
from .models import User
from .validation_models import user_schema, new_user_schema, login_schema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError
from flask import request


class UserListAPI(Resource):
    @jwt_required()
    def get(self):
        return {"users": user_schema.dump(User.find_all(), many=True)}

    def post(self):
        try:
            user = new_user_schema.load(data=request.get_json())
        except ValidationError as e:
            return e.messages_dict

        user_obj = User(**user)
        if User.is_existing(user_obj):
            return {"message": f"User already exists"}, 400

        user_obj.save_to_db()
        return {"user": user_obj.id}, 201


class UserAPI(Resource):
    @jwt_required()
    def get(self, id):
        if not id:
            return {"message": "Invalid Request"}, 401
        user = User.find_by_id(id)
        if not user:
            return {"message": "User Does not exist"}, 401
        return user_schema.dump(user)


class Login(Resource):
    def post(self):
        try:
            user_info = login_schema.loads(request.data)
        except ValidationError as e:
            return e.messages_dict
        user_data = User.find_by_user_name(user_info.get("user_name"))
        
        if not user_data:
            return {"message": "Invalid Username or password"}, 401

        if not check_password(user_info.get("password"), user_data.password_hash):
            return {"message": "Invalid Username or password"}, 401

        access_token = create_access_token(identity=user_data.user_name)
        refresh_token = create_refresh_token(identity=user_data.user_name)
        return {"access_token": access_token, "refresh_token": refresh_token}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}
