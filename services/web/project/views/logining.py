"""Module for authorization user in system """

from flask import request
from project.models import db, UserModel
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required


api = Namespace("auth", description="Authorization")


sign_up = api.model(
    "Sing up",
    {
        "username": fields.String("Enter username"),
        "password": fields.String("Enter password"),
        "is_admin": fields.Boolean("Status of user"),
    },
)

login_in = api.model(
    "Login in",
    {
        "username": fields.String("Enter username"),
        "password": fields.String("Enter password"),
    },
)


@api.route("/signup")
class SignUp(Resource):
    """Sign up users in system"""

    @staticmethod
    @api.expect(sign_up)
    def post() -> tuple:
        """Sign up users in system"""

        try:
            if request.is_json:
                data = request.json
                username = data["username"]
                password = data["password"]
                is_admin = data["is_admin"]
                user = UserModel.query.filter_by(username=username).first()

                if user:
                    return {"error": "Username already exists."}, 401
                new_user = UserModel(
                    username=username,
                    password=generate_password_hash(password, method="sha256"),
                    is_admin=is_admin,
                )

                db.session.add(new_user)
                db.session.commit()

                return {
                    "message": f"User {new_user.username} has been created successfully"
                }, 200
            return {"error": "The request payload is not in JSON format"}, 400
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/login")
class Login(Resource):
    """Login in user"""

    @staticmethod
    @api.expect(login_in)
    def post() -> tuple:
        """Login user in system"""

        if request.method == "POST":
            if request.is_json:
                data = request.get_json()
                username = data["username"]
                password = data["password"]
                user = UserModel.query.filter_by(username=username).first()

                if not user and not check_password_hash(user.password, password):
                    return {
                        "Error": "Please check your login details and try again"
                    }, 400
                login_user(user)

                return {
                    "Message": f"User {user.username} has been login successfully"
                }, 202
            return {"Error": "The request payload is not in JSON format"}, 401


@api.route("/logout")
class Logout(Resource):
    """Log out user from system"""

    @staticmethod
    @login_required
    def get():
        """Logout user from system"""
        try:
            logout_user()
            return {"message": "User is logout"}
        except:
            return {"message": "User is not logged in"}, 404
