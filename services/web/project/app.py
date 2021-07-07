from flask_migrate import Migrate
from project import models
from flask import Flask
from flask_login import LoginManager
from project import auth
from flask_restplus import Api
from flask_marshmallow import Marshmallow


app = Flask(__name__)
migrate = Migrate(app, models.db)
models.db.init_app(app)
app.register_blueprint(auth.auth, url_prefix='/auth')
app.secret_key = 'ksdmflaskdmflsakdfml'
app.config.from_object("project.config.Config")
api = Api(version='1.0', title='REST-API service',
          description='API service for managing the film library',)
api.init_app(app)
ma = Marshmallow(app)
from project.views.user import api as np1
api.add_namespace(np1)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login_post'


@login_manager.user_loader
def load_user(user_id):
    return models.UserModel.query.get(int(user_id))


if __name__ == "__main__":
    app.debug = True
    app.run()
