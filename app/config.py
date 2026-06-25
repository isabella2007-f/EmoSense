import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-fallback-secret')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'emosense.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.50))
    MAX_HISTORY = int(os.getenv('MAX_HISTORY', 100))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv('UPLOAD_FOLDER', 'app/static/captures'))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'

    DEEPFACE_HOME = os.path.join(BASE_DIR, 'ai_models')
