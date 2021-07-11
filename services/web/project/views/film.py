"""Film methods CRUD"""

from flask import request
from project.models import FilmModel, GenreModel, Director, UserModel, db, FilmGenre
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import ARRAY

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


@api.route("/get/<int:film_id>")
class GetFilms(Resource):
    """Method GET"""

    @staticmethod
    def get(film_id: int) -> tuple:
        """Get data about one film
        Format: json
        """

        genre_agg = func.array_agg(GenreModel.genre_name, type_=ARRAY(String)).label(
            "genres"
        )

        films = (
            db.session.query(FilmModel, Director, UserModel.username, genre_agg)
            .select_from(FilmModel)
            .join(FilmGenre)
            .join(GenreModel)
            .join(UserModel)
            .join(Director)
            .group_by(FilmModel.film_id, Director.director_id, UserModel.username)
            .filter(FilmModel.film_id == film_id)
            .all()
        )
        if films:
            serialized_data = [
                {
                    "title": film[0].title,
                    "release": str(film[0].year_release),
                    "genre": film.genres,
                    "director": f"{film[1].director_name}",
                    "description": film[0].description,
                    "rating": film[0].rating,
                    "poster": film[0].poster,
                    "user": film.username,
                }
                for film in films
            ]
            return serialized_data, 200
        return {"Error": "Film was not found"}, 404


@api.route("/get/")
class GetOneGenre(Resource):
    """Method GET all films"""

    @staticmethod
    def get() -> tuple:
        """Get data about one film
        Format: json
        """

        genre_agg = func.array_agg(GenreModel.genre_name, type_=ARRAY(String)).label(
            "genres"
        )

        films = (
            db.session.query(FilmModel, Director, UserModel.username, genre_agg)
            .select_from(FilmModel)
            .join(FilmGenre)
            .join(GenreModel)
            .join(UserModel)
            .join(Director)
            .group_by(FilmModel.film_id, Director.director_id, UserModel.username)
            .all()
        )
        serialized_data = [
            {
                "title": film[0].title,
                "release": str(film[0].year_release),
                "genre": film.genres,
                "director": f"{film[1].director_name}",
                "description": film[0].description,
                "rating": film[0].rating,
                "poster": film[0].poster,
                "user": film.username,
            }
            for film in films
        ]
        return serialized_data, 200


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
