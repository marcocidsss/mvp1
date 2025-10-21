import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

    # Configuración de la base de datos (MySQL)
    DB_USER = "root"           # Usuario MySQL
    DB_PASS = "12345"          # Contraseña MySQL
    DB_HOST = "127.0.0.1"      # Host MySQL
    DB_NAME = "venue"          # Nombre de la base de datos

    app.config.from_mapping(
        SECRET_KEY='change-me',   # Cambia si quieres
        SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='change-me-too'  # Cambia si quieres
    )

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)

    # Mostrar la URI de la base de datos para debug
    print("Conectando a:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Registrar rutas
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
