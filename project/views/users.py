from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import UserNotFound, IncorrectPassword
from project.container import user_service, auth_service
from project.tools.security import auth_required

users_ns = Namespace("user")


@users_ns.route("/")
class UserView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    @users_ns.response(401, "Invalid token")
    @auth_required
    def get(self):
        try:
            return user_service.get_user_by_email(email=self)
        except UserNotFound:
            abort(404, message="User not found")

    @auth_required
    def patch(self):
        input_data = request.json
        try:
            user_service.get_user_by_email(email=self)
        except UserNotFound:
            abort(404, message="User not found")

        return user_service.update(email=self, data=input_data)

@users_ns.route("/password/")
class PasswordView(Resource):
    @users_ns.response(200, "OK")
    @auth_required
    def put(self):
        input_data = request.json

        password1 = input_data.get('old_password')
        password2 = input_data.get('new_password')
        try:
            auth_service.update_password(email=self, old_password=password1, new_password=password2)
            return 'Password updated', 200
        except UserNotFound:
            abort(404, message="User not found")
        except IncorrectPassword:
            abort(401, message="Incorrect password")
