# app/config.py — Configuración central de la aplicación
# Lee los valores del archivo .env y los expone como atributos de la clase Config

import os                       # Para leer variables del sistema operativo
from dotenv import load_dotenv  # Para cargar el archivo .env automáticamente

load_dotenv()  # Lee el archivo .env y carga sus variables en el entorno

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# BASE_DIR = ruta absoluta a la carpeta raíz del proyecto (donde está run.py)


class Config:
    # Clase que agrupa toda la configuración de la app

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-fallback-secret')
    # Clave secreta para firmar sesiones y tokens de seguridad de Flask
    # Si no está en .env, usa 'dev-fallback-secret' (solo para desarrollo)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'emosense.db')
    # Ruta completa al archivo de base de datos SQLite
    # Ejemplo: sqlite:///C:/Users/.../EmoSense/database/emosense.db

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Desactiva el sistema de eventos de SQLAlchemy que no usamos (ahorra memoria)

    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.50))
    # Confianza mínima que debe tener la IA para aceptar un resultado (0.50 = 50%)

    MAX_HISTORY = int(os.getenv('MAX_HISTORY', 100))
    # Máximo de registros permitidos en el historial antes de borrar el más antiguo

    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv('UPLOAD_FOLDER', 'app/static/captures'))
    # Carpeta donde se guardan las fotos capturadas por los usuarios

    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    # Modo debug: muestra errores detallados en el navegador (solo para desarrollo)

    DEEPFACE_HOME = os.path.join(BASE_DIR, 'ai_models')
    # Carpeta donde DeepFace descarga y guarda los modelos de IA (~500 MB la primera vez)
