import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY','change-me'),
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','mysql+pymysql://user:pass@db:3306/venue'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY','change-me-too')
    )
    db.init_app(app)
    jwt.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
