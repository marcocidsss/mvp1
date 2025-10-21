import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

    # Configuración de base de datos y JWT
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASS = os.environ.get("DB_PASS", "")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "venue")

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'change-me'),
        SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'change-me-too')
    )

    db.init_app(app)
    jwt.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
