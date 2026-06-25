import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Emotion, Recommendation, FacialAnalysis, AnalysisHistory  # noqa: F401

    from app.routes.main import main_bp
    from app.routes.capture import capture_bp
    from app.routes.history import history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(capture_bp)
    app.register_blueprint(history_bp)

    return app
