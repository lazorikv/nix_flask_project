"""Film methods CRUD"""

from flask import request
from flask_login import current_user, login_required
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import ARRAY
from services.web.project.args import sorting
from services.web.project.models import FilmModel, GenreModel, Director, UserModel, db, FilmGenre
from services.web.project.paginate import get_paginated_list


api = Namespace("films", description="Films in library")


film_model = api.model(
    "Film",
    {
        "title": fields.String("Enter title"),
        "year_release": fields.String("Enter release film year"),
        "director_name": fields.String("Enter director_id"),
        "genres": fields.List(fields.String("Enter")),
        "description": fields.String("Enter description of film"),
        "rating": fields.String("Enter film rating"),
        "poster": fields.String("Enter link to poster"),
    },
)


@api.route("/get/<int:film_id>")
class GetFilms(Resource):
    """Method GET"""

    @staticmethod
    def get(film_id: int) -> tuple:
        """Get data about one film
        Format: json
        :return json with data about film by film_id
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
            for i in result:
                return i, 200
        return {"Error": "Film was not found"}, 404


@api.route("/get/")
class GetOneGenre(Resource):
    """Method GET all films"""

    @staticmethod
    @api.expect(sorting, validate=True)
    def get() -> tuple:
        """Get data about all films
        Format: json
        :return json list of films
        """

        args = sorting.parse_args()
        start = args["start"]
        limit = args["limit"]
        sorting_data = args["sort_data"]
        from_film = args["from"]
        to_film = args["to"]
        sort_by = args["sort_by"]
        genre_film = args["genre_film"]
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
        )
        director_film = args["Director"]
        search_film = args["search"]

        # partial match search
        if search_film:
            films = films.filter(FilmModel.title.ilike(f"%{search_film}%"))
        # search by director name
        if director_film:
            films = films.filter(Director.director_name == director_film)
        # sorting by rating
        if sorting_data == "Rating":
            if sort_by == "Ascending":
                films = films.order_by(FilmModel.rating.asc())
            films = films.order_by(FilmModel.rating.desc())
        # sorting by data release
        elif sorting_data == "Date Release":
            if sort_by == "Ascending":
                films = films.order_by(FilmModel.year_release.asc())
            films = films.order_by(FilmModel.year_release.desc())
        # search by date range
        if from_film and to_film:
            films = films.filter(FilmModel.year_release.between(from_film, to_film))
        # search by genre
        if genre_film:
            films = films.filter(GenreModel.genre_name == genre_film)
        if films:
            result = [
                {
                    "title": film[0].title,
                    "release": str(film[0].year_release),
                    "genre": film.genres,
                    "director": film[1].director_name,
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
                    start=request.args.get("start", start),
                    limit=request.args.get("limit", limit),
                ),
                200,
            )
        return {"Error": "Films not found"}, 404


@api.route("/post")
class PostGenre(Resource):
    """Method POST"""

    @api.expect(film_model)
    @login_required
    def post(self) -> tuple:
        """
        Post data about film to db
        :return json message
        """

        try:
            if current_user.user_id:
                director_in = request.json["director_name"]
                if director_in == "":
                    director_in = "unknown"
                sm_director = Director.director_in(director_in)
                if sm_director:
                    director_sp_id = sm_director.director_id
                else:
                    dir_name = Director(director_name=director_in)
                    db.session.add(dir_name)
                    db.session.commit()
                    sm_director = Director.director_in(director_in)
                    director_sp_id = sm_director.director_id
                film = FilmModel(
                    title=request.json["title"],
                    year_release=request.json["year_release"],
                    director_id=director_sp_id,
                    description=request.json["description"],
                    rating=request.json["rating"],
                    poster=request.json["poster"],
                    user_id=current_user.user_id,
                )
                db.session.add(film)
                db.session.commit()
                genres = request.json["genres"]
                GenreModel.genre_post(genres)
                return {"Message": "Film added to database"}, 201
            return {"Error": "Access to the requested resource is forbidden"}, 403
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/put/<int:film_id>")
class PutGenre(Resource):
    """Method PUT"""

    @staticmethod
    @api.expect(film_model)
    @login_required
    def put(film_id: int) -> tuple:
        """Update data about film"""
        try:
            film = FilmModel.query.get(film_id)
            if current_user.user_id:
                director_in = request.json["director_name"]
                if director_in == "":
                    director_in = "unknown"
                sm_director = Director.director_in(director_in)
                if sm_director:
                    director_sp_id = sm_director.director_id
                else:
                    dir_name = Director(director_name=director_in)
                    db.session.add(dir_name)
                    db.session.commit()
                    sm_director = Director.director_in(director_in)
                    director_sp_id = sm_director.director_id
                if film.user_id == current_user.user_id or current_user.is_admin is True:
                    film.title = request.json["title"]
                    film.year_release = request.json["year_release"]
                    film.director_id = director_sp_id
                    film.description = request.json["description"]
                    film.rating = request.json["rating"]
                    film.poster = request.json["poster"]
                    film.user_id = current_user.user_id
                    db.session.commit()
                    genres = request.json["genres"]
                    GenreModel.genre_post(genres)
                    return {"Message": "Data updated"}, 201
                return {"Error": "Access to the requested resource is forbidden"}, 403
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/delete/<int:film_id>")
class DeleteGenre(Resource):
    """Method DELETE"""

    @staticmethod
    @login_required
    def delete(film_id: int) -> tuple:
        """
        Removes a film by id
        :return json message or error
        """
        film = FilmModel.query.filter(FilmModel.film_id == film_id).first()
        if film:
            if film.user_id == current_user.user_id or current_user.is_admin is True:
                db.session.delete(film)
                db.session.commit()
                return {"Message": "Data deleted successfully"}, 201
            return {"Error": "Access to the requested resource is forbidden"}, 403
        return {"Error": "Films not found"}, 404
