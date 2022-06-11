from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api

from project.setup_db import db
from project.views import genres_ns, directors_ns, movies_ns, auth_ns, users_ns

api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Flask Course Project 4",
    doc="/docs",
)

# Resource sharing for frontend needs
cors = CORS()


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route("/")
    def index_page():
        return render_template("index.html")

    cors.init_app(app)
    db.init_app(app)
    api.init_app(app)

    # Namespaces registration
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)

    return app
