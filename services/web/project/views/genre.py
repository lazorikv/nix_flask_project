"""Genre methods CRUD"""

from flask import request
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError
from services.web.project.models import db, GenreModel


api = Namespace("genres", description="Film genres")


genre_model = api.model(
    "Genre",
    {
        "genre_name": fields.String("Enter Genre"),
    },
)


@api.route("/get")
class GetGenre(Resource):
    """Method GET"""

    @staticmethod
    def get() -> tuple:
        """
        Get data about all genres
        Format: json
        :returns genre_list: list with get genres from db

        """

        genres = GenreModel.query.all()
        if genres:
            genre_list = [
                {
                    "genre_id": genre.genre_id,
                    "genre_name": genre.genre_name,
                }
                for genre in genres
            ]
            return {"Genres": genre_list}, 200
        return {"Error": "Genres not found"}, 404


@api.route("/get/<int:genre_id>")
class GetOneGenre(Resource):
    """Method GET one genre"""

    @staticmethod
    def get(genre_id: int) -> tuple:
        """
        Get data about one genre
        Format: json
        :return json with data about genre by genre_id
        """

        genre = db.session.query(GenreModel).filter_by(genre_id=genre_id).first()

        if genre:
            return {
                "genre_id": genre.genre_id,
                "genre_name": genre.genre_name,
            }, 200
        return {"Error": "Genre not found"}, 404


@api.route("/post")
class PostGenre(Resource):
    """Method POST"""

    @staticmethod
    @api.expect(genre_model)
    def post() -> tuple:
        """
        Post data about genre to db
        :return json message
        """

        try:
            data = request.json["genre_name"]
            if GenreModel.genre_in(data):
                return {"Error": "Genre is already exist"}, 409
            genre = GenreModel(genre_name=data)
            db.session.add(genre)
            db.session.commit()
            return {"Message": "Genre added to database"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/put/<int:genre_id>")
class PutGenre(Resource):
    """Method PUT """

    @staticmethod
    @api.expect(genre_model)
    def put(genre_id: int) -> tuple:
        """
        Update data about genre
        :return json message
        """
        try:
            genre = GenreModel.query.get(genre_id)
            genre.genre_name = request.json["genre_name"]
            db.session.commit()
            return {"Message": "Data updated"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/delete/<int:genre_id>")
class DeleteGenre(Resource):
    """Method DELETE"""

    @staticmethod
    def delete(genre_id: int) -> tuple:
        """
        Removes a genre by id
        :return json message
        """
        genre = GenreModel.query.get(genre_id)
        if genre:
            db.session.delete(genre)
            db.session.commit()
            return {"Message": "Data deleted successfully"}, 201
        return {"Error": "Genre not found"}, 404
