"""Film methods CRUD"""

from flask import request
from project.models import FilmModel, db
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError

api = Namespace("films", description="Films in library")

film_model = api.model(
    "Film",
    {
        "title": fields.String("Enter title"),
        "year_release": fields.String("Enter release film year"),
        "director_id": fields.String("Enter director_id"),
        "description": fields.String("Enter description of film"),
        "rating": fields.String("Enter film rating"),
        "poster": fields.String("Enter link to poster"),
        "user_id": fields.String("Enter user_id"),
    },
)


@api.route("/get")
class GetFilms(Resource):
    """Method GET"""

    @staticmethod
    def get() -> tuple:
        """Get data about all films
        Format: json
        """

        films = FilmModel.query.all()

        if films:
            films_list = [
                {
                    "film_id": film.film_id,
                    "title": film.title,
                    "year_release": film.year_release,
                    "director_id": film.director_id,
                    "description": film.description,
                    "rating": film.rating,
                    "poster": film.poster,
                    "user_id": film.user_id,
                }
                for film in films
            ]
            return {"films": films_list}, 200
        return {"Error": "Films was not found"}, 404


@api.route("/get/<int:film_id>")
class GetOneGenre(Resource):
    """Method GET one film"""

    @staticmethod
    def get(film_id: int) -> tuple:
        """Get data about one film
        Format: json
        """

        film = db.session.query(FilmModel).filter_by(film_id=film_id).first()
        if film:
            return {
                "film_id": film.film_id,
                "title": film.title,
                "year_release": film.year_release,
                "director_id": film.director_id,
                "description": film.description,
                "rating": film.rating,
                "poster": film.poster,
                "user_id": film.user_id,
            }, 200
        return {"Error": "Film was not found"}, 404


@api.route("/post")
class PostGenre(Resource):
    """Method POST"""

    @staticmethod
    @api.expect(film_model)
    def post() -> tuple:
        """Post data about film to db"""

        try:
            film = FilmModel(
                title=request.json["title"],
                year_release=request.json["year_release"],
                director_id=request.json["director_id"],
                description=request.json["description"],
                rating=request.json["rating"],
                poster=request.json["poster"],
                user_id=request.json["user_id"],
            )
            db.session.add(film)
            db.session.commit()
            return {"message": "Film added to database"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/put/<int:film_id>")
class PutGenre(Resource):
    """Method PUT"""

    @staticmethod
    @api.expect(film_model)
    def put(film_id):
        """Update data about film"""
        try:
            film = FilmModel.query.get(film_id)
            film.title = request.json["title"]
            film.year_release = request.json["year_release"]
            film.director_id = request.json["director_id"]
            film.description = request.json["description"]
            film.rating = request.json["rating"]
            film.poster = request.json["poster"]
            film.user_id = request.json["user_id"]
            db.session.commit()
            return {"message": "data updated"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/delete/<int:film_id>")
class DeleteGenre(Resource):
    """Method DELETE"""

    @staticmethod
    def delete(film_id) -> tuple:
        """Removes a film by id"""
        genre = FilmModel.query.get(film_id)
        db.session.delete(genre)
        db.session.commit()
        return {"message": "data deleted successfully"}, 201
