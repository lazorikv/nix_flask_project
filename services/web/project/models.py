"""Module with models of film library"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class FilmModel(db.Model):
    """Model of film essence"""

    __tablename__ = "film"

    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, nullable=False)
    year_release = db.Column(db.Date, nullable=False)
    director_id = db.Column(
        db.Integer,
        db.ForeignKey("director.director_id", ondelete="CASCADE"),
        nullable=True,
    )
    description = db.Column(db.Text())
    rating = db.Column(db.Integer, db.CheckConstraint("1 <= rating AND rating<= 10"),
                       nullable=False, )
    poster = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE",), nullable=True)
    genres = db.relationship("GenreModel", secondary='filmgenre')

    def __init__(
            self, title, year_release, director_id, description, rating, poster, user_id
    ):
        self.title = title
        self.year_release = year_release
        self.director_id = director_id
        self.description = description
        self.rating = rating
        self.poster = poster
        self.user_id = user_id

    def __repr__(self):
        return f"<Film {self.title}>"


class UserModel(UserMixin, db.Model):
    """Model of user essence"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    films = db.relationship("FilmModel", backref="film")

    def get_id(self):
        """Get user_id from table Users"""
        return self.user_id

    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User {self.username}>"


class GenreModel(db.Model):
    """Model of genre essence"""

    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)

    def __init__(self, genre_name):
        self.genre_name = genre_name

    def __repr__(self):
        return f"Genre {self.genre_name}"

    @classmethod
    def genre_in(cls, genre_name: str):
        """Returns the genre query"""
        return GenreModel.query.filter(GenreModel.genre_name == genre_name).first()

    @classmethod
    def genre_post(cls, list_genre: list):
        """Adding genres to the database"""

        count_films = FilmModel.query.order_by(FilmModel.film_id.desc()).first()
        for genre in list_genre:
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


class Director(db.Model):
    """Model of director essence"""

    __tablename__ = "director"

    director_id = db.Column(db.Integer, primary_key=True, )
    director_name = db.Column(db.String(100), index=True, nullable=False)
    directed_film = db.relationship("FilmModel", backref="directed_film")

    def __init__(self, director_name):
        self.director_name = director_name

    def __repr__(self):
        return f"<Director {self.director_name}>"

    @classmethod
    def director_in(cls, director_name: str):
        """Returns the director query"""
        return Director.query.filter(Director.director_name == director_name).first()


class FilmGenre(db.Model):
    """Model of film genre essence"""

    __tablename__ = 'filmgenre'

    filmgenre_id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(
        db.Integer, db.ForeignKey("genre.genre_id", ondelete="CASCADE")
    )
    film_id = db.Column(db.Integer, db.ForeignKey("film.film_id"))
