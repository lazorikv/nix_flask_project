from flask_migrate import Migrate
from project import models
from flask import Flask, request
from flask_login import LoginManager, login_required
from project import auth

app = Flask(__name__)
migrate = Migrate(app, models.db)
models.db.init_app(app)
app.register_blueprint(auth.auth, url_prefix='/auth')
app.secret_key = 'ksdmflaskdmflsakdfml'
app.config.from_object("project.config.Config")

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'auth.login'
login_manager.login_view = 'auth.login_post'


@login_manager.user_loader
def load_user(user_id):
    return models.UserModel.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    return 'hello'


if __name__ == '__main__':

    app.debug = True
    app.run()

