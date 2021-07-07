"""User methods CRUD"""

from flask import request
from project import models
from flask_restplus import fields, Resource, Namespace
from project.app import ma

api = Namespace('users', description='User Registration')

user_model = api.model('User', {
    'username': fields.String('Enter Name'),
    'password': fields.String('Enter Password')
})


class UserSchema(ma.Schema):
    """Create a UserSchema by defining a class with
       variables mapping attribute names to Field objects"""
    class Meta:
        fields = ('id', 'username', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route('/get')
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
                } for user in users]
            return {'users': user_list}, 200
        else:
            return {"Error": "Users was not found"}, 404


@api.route('/get/<int:user_id>')
class GetOneUser(Resource):
    """Method GET one user"""

    @staticmethod
    def get(user_id: int) -> tuple:
        """Get data about one user
        Format: json
        """
        user = models.db.session.query(models.UserModel).filter_by(user_id=user_id).first()
        if user:
            return {'User': user.user_id,
                    'user_id': user.user_id,
                    'username': user.username,
                    'password': user.password}, 200
        else:
            return {"Error": "User was not found"}, 404


@api.route('/post')
class PostUser(Resource):
    """Method POST"""
    @api.expect(user_model)
    def post(self) -> tuple:
        """Post data about user to server
        """
        user = models.UserModel(username=request.json['username'], password=request.json['password'])
        models.db.session.add(user)
        models.db.session.commit()
        return {'message': 'User added to database'}, 201


@api.route('/put/<int:user_id>')
class PutUser(Resource):
    """Method PUT"""
    @api.expect(user_model)
    def put(self, user_id):
        """Update data about user"""
        user = models.UserModel.query.get(user_id)
        user.username = request.json['username']
        user.password = request.json['password']
        models.db.session.commit()
        return {'message': 'data updated'}, 201


@api.route('/delete/<int:user_id>')
class DeleteUser(Resource):
    """Method DELETE"""
    def delete(self, user_id) -> tuple:
        """Removes a user by his id"""
        user = models.UserModel.query.get(user_id)
        models.db.session.delete(user)
        models.db.session.commit()
        return {'message': 'data deleted successfully'}, 201

