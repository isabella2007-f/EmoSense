# app/__init__.py — Fábrica de la aplicación Flask
# Aquí se ensamblan todas las piezas: base de datos, rutas y configuración

import os
from flask import Flask                        # Framework web principal
from flask_sqlalchemy import SQLAlchemy        # ORM para conectar Python con la base de datos
from flask_migrate import Migrate              # Maneja los cambios en la estructura de la base de datos

db = SQLAlchemy()       # Objeto global de conexión a la base de datos (se usa en todos los modelos)
migrate = Migrate()     # Objeto global para gestionar migraciones de la base de datos


def create_app():
    # Función que crea y configura la app — patrón "App Factory"
    app = Flask(__name__)                                    # Crea la instancia de Flask
    app.config.from_object('app.config.Config')             # Carga la configuración desde config.py

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) # Crea la carpeta de capturas si no existe

    db.init_app(app)        # Conecta SQLAlchemy con esta app (le da acceso a la configuración)
    migrate.init_app(app, db)  # Conecta Flask-Migrate para poder usar "flask db upgrade"

    # Importa los modelos para que SQLAlchemy los registre (necesario para las migraciones)
    from app.models import Emotion, Recommendation, FacialAnalysis, AnalysisHistory  # noqa: F401

    # Importa e registra los blueprints (grupos de rutas)
    from app.routes.main import main_bp         # Rutas de páginas principales (inicio, captura, historial)
    from app.routes.capture import capture_bp   # Ruta de análisis de imagen (/analyze)
    from app.routes.history import history_bp   # Rutas del historial (listar, detalle, eliminar)

    app.register_blueprint(main_bp)      # Registra las rutas principales en la app
    app.register_blueprint(capture_bp)   # Registra la ruta de análisis en la app
    app.register_blueprint(history_bp)   # Registra las rutas del historial en la app

    return app  # Devuelve la app completamente configurada
