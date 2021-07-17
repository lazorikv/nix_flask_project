"""User methods CRUD"""

from flask import request
from services.web.project import models
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError


api = Namespace("users", description="User HTTP methods")

user_model = api.model(
    "User",
    {
        "username": fields.String("Enter Name"),
        "password": fields.String("Enter Password"),
        "is_admin": fields.Boolean("Enter status")
    },
)


@api.route("/get")
class GetUser(Resource):
    """Method GET"""

    @staticmethod
    def get() -> tuple:
        """Get data about all users
        Format: json
        """

        users = models.UserModel.query.all()
        if users:
            user_list = [
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "password": user.password,
                    "is_admin": user.is_admin
                }
                for user in users
            ]
            return {"users": user_list}, 200
        return {"Error": "Users was not found"}, 404


@api.route("/get/<int:user_id>")
class GetOneUser(Resource):
    """Method GET one user"""

    @staticmethod
    def get(user_id: int) -> tuple:
        """Get data about one user
        Format: json
        """

        user = (
            models.db.session.query(models.UserModel).filter_by(user_id=user_id).first()
        )
        if user:
            return {
                "user_id": user.user_id,
                "username": user.username,
                "password": user.password,
                "is_admin": user.is_admin
            }, 200
        return {"Error": "User was not found"}, 404


@api.route("/post")
class PostUser(Resource):
    """Method POST"""

    @staticmethod
    @api.expect(user_model)
    def post() -> tuple:
        """Post data about user to server"""

        try:
            user = models.UserModel(
                username=request.json["username"], password=request.json["password"],
                is_admin=request.json["is_admin"]
            )
            models.db.session.add(user)
            models.db.session.commit()
            return {"message": "User added to database"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/put/<int:user_id>")
class PutUser(Resource):
    """Method PUT"""

    @staticmethod
    @api.expect(user_model)
    def put(user_id: int) -> tuple:
        """Update data about user"""

        try:
            user = models.UserModel.query.get(user_id)
            user.username = request.json["username"]
            user.password = request.json["password"]
            user.is_admin = request.json["is_admin"]
            models.db.session.commit()
            return {"message": "Data updated"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/delete/<int:user_id>")
class DeleteUser(Resource):
    """Method DELETE"""

    @staticmethod
    def delete(user_id: int) -> tuple:
        """Removes a user by his id"""

        user = models.UserModel.query.filter(models.UserModel.user_id == user_id).first()
        models.db.session.delete(user)
        models.db.session.commit()
        return {"message": "data deleted successfully"}, 201
