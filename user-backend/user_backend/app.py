import os
import time

import schedule
import sentry_sdk
from flask_cors import CORS
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from endpoints.user import user_blueprint
from endpoints.achievement import achievement_blueprint
from endpoints.competitor import competitor_blueprint

import config
from models import db


def create_app():
    sentry_sdk.init(
        dsn="https://c9afad850e5f46a6aa5ab228a8fea082@o1288571.ingest.sentry.io/6505644",
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
    flask_app = Flask(__name__)
    CORS(flask_app, origins=['*', 'http://localhost:3000'], allow_headers=['*'], supports_credentials=False)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.url_map.strict_slashes = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    flask_app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
    return flask_app


app = create_app()
salt = os.urandom(32)


app.register_blueprint(user_blueprint)
app.register_blueprint(achievement_blueprint)
app.register_blueprint(competitor_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
