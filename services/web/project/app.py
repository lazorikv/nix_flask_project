from flask_migrate import Migrate
from flask import request
from project import models
from flask import Flask, send_from_directory

app = Flask(__name__)
migrate = Migrate(app, models.db)
models.db.init_app(app)

app.config.from_object("project.config.Config")

if __name__ == '__main__':
    app.debug = True
    app.run()

