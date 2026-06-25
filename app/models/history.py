from datetime import datetime, timezone
from app import db


class FacialAnalysis(db.Model):
    __tablename__ = 'facial_analyses'

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(300), nullable=False)
    detected_emotion = db.Column(db.String(20), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    all_scores = db.Column(db.Text, nullable=False)
    analyzed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    history = db.relationship('AnalysisHistory', backref='analysis', lazy=True)

    def __repr__(self):
        return f'<FacialAnalysis {self.detected_emotion} {self.confidence_score:.2f}>'


class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('facial_analyses.id'), nullable=False)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendations.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    recommendation = db.relationship('Recommendation', backref='history_entries', lazy=True)

    def __repr__(self):
        return f'<AnalysisHistory analysis={self.analysis_id}>'
