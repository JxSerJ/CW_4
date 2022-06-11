from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service
from project.exceptions import WrongPassword, UserNotFound
from project.schemas.auth import AuthRegisterData, AuthUserSchema, AuthLoginSchema

auth_reg_data_schema = AuthRegisterData()
auth_user_data_schema = AuthUserSchema()
auth_login_data_schema = AuthLoginSchema()

auth_ns = Namespace("auth")


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        input_data = request.json
        validated_data = auth_reg_data_schema.load(input_data)

        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        return auth_service.register(password=password, email=email), 200

@auth_ns.route('/login/')
class AuthLoginView(Resource):
    def post(self):
        input_data = request.json
        validated_data = auth_user_data_schema.load(input_data)

        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        try:
            return auth_service.login(password=password, email=email), 200
        except WrongPassword:
            return '', 401
        except UserNotFound:
            return '', 401
