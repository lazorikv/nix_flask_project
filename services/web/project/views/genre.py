"""Genre methods CRUD"""

from flask import request
from project.models import db, GenreModel
from flask_restplus import fields, Resource, Namespace
from project.app import ma

api = Namespace('genres', description='Film genres')

genre_model = api.model('Genre', {
    'genre_name': fields.String('Enter Genre'),
})


class UserSchema(ma.Schema):
    """Create a UserSchema by defining a class with
       variables mapping attribute names to Field objects"""
    class Meta:
        fields = ('genre_id', 'genre_name')


genre_schema = UserSchema()
genres_schema = UserSchema(many=True)


@api.route('/get')
class GetGenre(Resource):
    """Method GET"""

    @staticmethod
    def get() -> tuple:
        """Get data about all genres
        Format: json
        """

        genres = GenreModel.query.all()
        if genres:
            genre_list = [
                {
                    "genre_id": genre.genre_id,
                    "genre_name": genre.genre_name,
                } for genre in genres]
            return {'genres': genre_list}, 200
        else:
            return {"Error": "Genres was not found"}, 404


@api.route('/get/<int:genre_id>')
class GetOneGenre(Resource):
    """Method GET one genre"""

    @staticmethod
    def get(genre_id: int) -> tuple:
        """Get data about one genre
        Format: json
        """
        genre = db.session.query(GenreModel).filter_by(genre_id=genre_id).first()
        if genre:
            return {'Genre': genre.genre_id,
                    'genre_id': genre.user_id,
                    'genre_name': genre.genre_name}, 200
        else:
            return {"Error": "Genre was not found"}, 404


@api.route('/post')
class PostGenre(Resource):
    """Method POST"""
    @api.expect(genre_model)
    def post(self) -> tuple:
        """Post data about genre to server
        """
        genre = GenreModel(genre_name=request.json['genre_name'])
        db.session.add(genre)
        db.session.commit()
        return {'message': 'Genre added to database'}, 201


@api.route('/put/<int:genre_id>')
class PutGenre(Resource):
    """Method PUT"""
    @api.expect(genre_model)
    def put(self, genre_id):
        """Update data about genre"""
        genre = GenreModel.query.get(genre_id)
        genre.genre_name = request.json['genre_name']
        db.session.commit()
        return {'message': 'data updated'}, 201


@api.route('/delete/<int:genre_id>')
class DeleteGenre(Resource):
    """Method DELETE"""
    def delete(self, genre_id) -> tuple:
        """Removes a genre by id"""
        genre = GenreModel.query.get(genre_id)
        db.session.delete(genre)
        db.session.commit()
        return {'message': 'data deleted successfully'}, 201
