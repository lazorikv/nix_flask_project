from flask.cli import FlaskGroup

from project.app import app
from project import models
from random import randint, uniform

from faker import Factory


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    models.db.drop_all()
    models.db.create_all()
    models.db.session.commit()


@cli.command("insert_db")
def insert_data():
    """Create test input data in database"""
    faker = Factory.create()
    count = 0
    while count <= 100:
        user_in = models.UserModel(
            username=faker.first_name(),
            password=faker.password(),
        )
        count += 1
        models.db.session.add(user_in)
        models.db.session.commit()

    genres = ["action", "fighting", "comedy", "kids-movie", "drama", "horror",]
    for i in range(len(genres)):
        genre_in = models.GenreModel(
            genre_name=genres[i]
        )
        models.db.session.add(genre_in)
        models.db.session.commit()

    count = 0
    while count <= 50:
        director_in = models.Director(
            director_name=faker.name(),
        )
        count += 1
        models.db.session.add(director_in)
        models.db.session.commit()

    count_directors = models.Director.query.order_by(models.Director.director_id.desc()).first()
    count_users = models.UserModel.query.order_by(models.UserModel.user_id.desc()).first()

    count = 0
    while count <= 150:
        film_in = models.FilmModel(
            title=faker.currency_name(),
            year_release=faker.date(),
            director_id=randint(1, int(count_directors.director_id)),
            description=faker.paragraph(
                nb_sentences=5, variable_nb_sentences=False
            ),
            rating=round(uniform(1, 10), 2),
            poster=faker.image_url(),
            user_id=randint(1, int(count_users.user_id)),
        )
        count += 1
        models.db.session.add(film_in)
        models.db.session.commit()

    count = 0

    while count <= 300:
        filmgenre_in = models.FilmGenre(
            film_id=randint(1, 150),
            genre_id=randint(1, len(genres))
        )
        models.db.session.add(filmgenre_in)
        models.db.session.commit()
        count += 1

    models.db.session.commit()


if __name__ == "__main__":
    cli()
