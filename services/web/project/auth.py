"""Module for authorization user"""
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from project import models


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login_post():
    """Login user in system"""

    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            username = data["username"]
            password = data["password"]
            user = models.UserModel.query.filter_by(username=username).first()

            if not user and not check_password_hash(user.password, password):

                return {"Error": "Please check your login details and try again."}
            login_user(user)
            return {"Message": f"User - {user.username} has been login successfully."}
        return {"Error": "The request payload is not in JSON format"}


@auth.route("/signup", methods=["GET", "POST"])
def signup_post():
    """Sign up user in system"""

    if request.method == "POST":
        if request.is_json:
            data = request.json
            username = data["username"]
            password = data["password"]
            user = models.UserModel.query.filter_by(username=username).first()

            if user:
                return {"error": "Username already exists."}
            new_user = models.UserModel(
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )

            models.db.session.add(new_user)
            models.db.session.commit()

            return {
                "message": f"User - {new_user.username} has been created successfully."
            }
        return {"error": "The request payload is not in JSON format"}


@auth.route("/logout")
@login_required
def logout():
    """Logout user from system"""

    logout_user()
    return {"message": "Redirected to index"}
