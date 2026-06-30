# app/models/history.py — Define las tablas de análisis e historial
# Contiene DOS modelos: FacialAnalysis (cada análisis) y AnalysisHistory (el historial)

from datetime import datetime, timezone  # Para registrar la fecha y hora del análisis
from app import db                       # Importa el objeto de conexión a la base de datos


class FacialAnalysis(db.Model):
    # Tabla 'facial_analyses': guarda cada análisis de imagen realizado
    # Una fila nueva se crea cada vez que el usuario analiza una foto

    __tablename__ = 'facial_analyses'  # Nombre exacto de la tabla en SQLite

    id = db.Column(db.Integer, primary_key=True)
    # Columna 'id': clave primaria autoincremental

    image_path = db.Column(db.String(300), nullable=False)
    # Columna 'image_path': ruta relativa de la foto guardada en disco
    # Ejemplo: 'captures/a3f2bc91d4e5.jpg'

    detected_emotion = db.Column(db.String(20), nullable=False)
    # Columna 'detected_emotion': emoción dominante detectada por DeepFace
    # Ejemplo: 'happy', 'sad', 'angry'...

    confidence_score = db.Column(db.Float, nullable=False)
    # Columna 'confidence_score': porcentaje de confianza normalizado entre 0.0 y 1.0
    # Ejemplo: 0.873 significa 87.3% de confianza

    all_scores = db.Column(db.Text, nullable=False)
    # Columna 'all_scores': JSON con los porcentajes de las 7 emociones guardado como texto
    # Ejemplo: '{"happy": 0.873, "sad": 0.031, "angry": 0.02, ...}'

    analyzed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Columna 'analyzed_at': fecha y hora del análisis en UTC
    # Se asigna automáticamente al crear el registro

    history = db.relationship('AnalysisHistory', backref='analysis', lazy=True)
    # Relación con AnalysisHistory: permite acceder a analysis.history

    def __repr__(self):
        # Representación en texto del objeto (útil para debug en consola)
        return f'<FacialAnalysis {self.detected_emotion} {self.confidence_score:.2f}>'


class AnalysisHistory(db.Model):
    # Tabla 'analysis_history': une cada análisis con su recomendación
    # Es la tabla que representa el "historial" que ve el usuario en la pantalla

    __tablename__ = 'analysis_history'  # Nombre exacto de la tabla en SQLite

    id = db.Column(db.Integer, primary_key=True)
    # Columna 'id': clave primaria autoincremental

    analysis_id = db.Column(db.Integer, db.ForeignKey('facial_analyses.id'), nullable=False)
    # Columna 'analysis_id': FK que apunta al análisis de imagen correspondiente

    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendations.id'), nullable=False)
    # Columna 'recommendation_id': FK que apunta a la recomendación que se mostró al usuario

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Columna 'created_at': fecha y hora en que se creó este registro de historial

    recommendation = db.relationship('Recommendation', backref='history_entries', lazy=True)
    # Relación con Recommendation: permite acceder a history_entry.recommendation directamente

    def __repr__(self):
        # Representación en texto del objeto (útil para debug en consola)
        return f'<AnalysisHistory analysis={self.analysis_id}>'
