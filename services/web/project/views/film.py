"""Film methods CRUD"""

from flask import request
from project.models import FilmModel, GenreModel, Director, UserModel, db, FilmGenre
from flask_restplus import fields, Resource, Namespace, reqparse
from marshmallow import ValidationError
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import ARRAY
from project.paginate import get_paginated_list

api = Namespace("films", description="Films in library")

pagination = reqparse.RequestParser()
pagination.add_argument('page', type=int, required=False,
                        default=1, help='Page number')
pagination.add_argument('per_page', type=int, required=False,
                        choices=[10, 20, 30, 40, 50])

film_model = api.model(
    "Film",
    {
        "title": fields.String("Enter title"),
        "year_release": fields.String("Enter release film year"),
        "director_id": fields.String("Enter director_id"),
        "genres": fields.List(fields.String("Enter")),
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
            result = [
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
            return result, 200
        return {"Error": "Film was not found"}, 404


@api.route("/get/")
class GetOneGenre(Resource):
    """Method GET all films"""

    @staticmethod
    def get() -> tuple:
        """Get data about all films
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
        if films:
            result = [
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
            return (
                get_paginated_list(
                    result,
                    "",
                    start=request.args.get("start", 1),
                    limit=request.args.get("limit", 20),
                ),
                200,
            )

        return {"Error": "Films was not found"}, 404


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
            genres = request.json["genres"]
            count_films = FilmModel.query.order_by(FilmModel.film_id.desc()).first()
            for genre in genres:
                sm_genre = GenreModel.genre_in(genre)
                if sm_genre:
                    filmgenre = FilmGenre(
                        genre_id=sm_genre.genre_id, film_id=int(count_films.film_id)
                    )
                    db.session.add(filmgenre)
                    db.session.commit()
                else:

                    genre_add = GenreModel(genre_name=genre)
                    db.session.add(genre_add)
                    db.session.commit()

                    sm_genre = GenreModel.genre_in(genre)
                    filmgenre = FilmGenre(
                        genre_id=sm_genre.genre_id, film_id=int(count_films.film_id)
                    )
                    db.session.add(filmgenre)
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
        film = FilmModel.query.get(film_id)
        db.session.delete(film)
        db.session.commit()
        return {"message": "data deleted successfully"}, 201
