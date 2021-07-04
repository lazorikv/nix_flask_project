from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FilmModel(db.Model):


    __tablename__ = 'film'

    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    year_release = db.Column(db.Date, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id'), nullable=True)
    description = db.Column(db.Text())
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    film_sm = db.relationship('FilmGenreModel', backref='film_sm')

    def __init__(self, title, year_release, director, description, rating,
                 poster, user_id):
        self.title = title
        self.year_release = year_release
        self.director = director
        self.description = description
        self.rating = rating
        self.poster = poster
        self.user_id = user_id

    def __repr__(self):
        return f"<Film {self.title}>"


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    films = db.relationship('FilmModel', backref='film')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'


class GenreModel(db.Model):
    __tablename__ = 'genre'

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)
    filmgenre = db.relationship('FilmGenreModel', backref='filmgenre')

    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return f"Genre {self.genre}"


class FilmGenreModel(db.Model):

    __tablename__ = 'filmgenre'

    filmgenre_id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'))
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'))


class Director(db.Model):

    __tablename__ = 'director'

    director_id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(100), nullable=False)
    directed_film = db.relationship('FilmModel', backref='directed_film')

    def __init__(self, director_name):
        self.director_name = director_name

    def __repr__(self):
        return f'<Director {self.director_name}>'

