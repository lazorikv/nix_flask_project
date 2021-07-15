"""Director methods CRUD"""

from flask import request
from project.models import db, Director
from flask_restplus import fields, Resource, Namespace
from marshmallow import ValidationError


api = Namespace("directors", description="Film director")


director_model = api.model(
    "Director",
    {
        "director_name": fields.String("Enter director"),
    },
)


@api.route("/get")
class GetDirector(Resource):
    """Method GET"""

    @staticmethod
    def get() -> tuple:
        """Get data about all directors
        Format: json
        """

        directors = Director.query.all()

        if directors:
            director_list = [
                {
                    "director_id": director.director_id,
                    "director_name": director.director_name,
                }
                for director in directors
            ]
            return {"genres": director_list}, 200
        return {"Error": "Directors not found"}, 404


@api.route("/get/<int:director_id>")
class GetOneDirector(Resource):
    """Method GET one director"""

    @staticmethod
    def get(director_id: int) -> tuple:
        """Get data about one director
        Format: json
        """

        director = db.session.query(Director).filter_by(director_id=director_id).first()
        if director:
            return {
                "Director": director.director_id,
                "director_id": director.director_id,
                "director_name": director.director_name,
            }, 200
        return {"Error": "Director not found"}, 404


@api.route("/post")
class PostDirector(Resource):
    """Method POST"""

    @staticmethod
    @api.expect(director_model)
    def post() -> tuple:
        """Post data about director to db"""

        try:
            director = Director(director_name=request.json["director_name"])
            db.session.add(director)
            db.session.commit()
            return {"message": "Director added to database"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/put/<int:director_id>")
class PutDirector(Resource):
    """Method PUT"""

    @staticmethod
    @api.expect(director_model)
    def put(director_id):
        """Update data about director"""

        try:
            director = Director.query.get(director_id)
            director.director_name = request.json["director_name"]
            db.session.commit()
            return {"message": "data updated"}, 201
        except ValidationError as err:
            return {"Error ": str(err)}, 400


@api.route("/delete/<int:director_id>")
class DeleteDirector(Resource):
    """Method DELETE"""

    @staticmethod
    def delete(director_id) -> tuple:
        """Removes a director by id"""

        director = Director.query.get(director_id)
        if director:
            db.session.delete(director)
            db.session.commit()
            return {"message": "data deleted successfully"}, 201
        return {"Error": "Director not found"}, 404
