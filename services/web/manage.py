from flask.cli import FlaskGroup

from project.app import app
from project import models


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    models.db.drop_all()
    models.db.create_all()
    models.db.session.commit()


@cli.command("add_user")
def add_user():
    models.db.session.add(models.UserModel(username="vlad@gmail.org", password='qwerty123'))
    models.db.session.commit()


if __name__ == "__main__":
    cli()
