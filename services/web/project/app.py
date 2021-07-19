"""Main module"""

import logging.config
import yaml
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restplus import Api
from services.web.project import models
from services.web.project.views.director import api as director_namespace
from services.web.project.views.film import api as film_namespace
from services.web.project.views.genre import api as genre_namespace
from services.web.project.views.user import api as user_namespace
from services.web.project.views.logining import api as auth_namespace


#  init app
def create_app():
    """Create application"""
    m_app = Flask(__name__)
    m_app.config.from_object("services.web.project.config.Config")
    return m_app


app = create_app()
app.secret_key = "MY_SECRET_KEY"

# init logging
logging.basicConfig(filename="error.log", level=logging.DEBUG)
logging.config.dictConfig(yaml.load(open("services/web/logging.conf")))
logfile = logging.getLogger("file")
logconsole = logging.getLogger("console")
logfile.debug("Debug FILE")
logconsole.debug("Debug CONSOLE")

# init db
migrate = Migrate(app, models.db)
models.db.init_app(app)

# init restplus
api = Api(
    version="1.0",
    title="REST-API service",
    description="API service for managing the film library",
    prefix="/api/v1",
)
api.init_app(app)
api.add_namespace(user_namespace)
api.add_namespace(genre_namespace)
api.add_namespace(film_namespace)
api.add_namespace(director_namespace)
api.add_namespace(auth_namespace)

# init flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_login"


@login_manager.user_loader
def load_user(user_id):
    """Reloading the user object from the user ID stored in the session"""
    return models.UserModel.query.get(int(user_id))


if __name__ == "__main__":
    app.debug = True
    app.run()
