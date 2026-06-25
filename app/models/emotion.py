from app import db


class Emotion(db.Model):
    __tablename__ = 'emotions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    label_es = db.Column(db.String(30), nullable=False)
    color_hex = db.Column(db.String(7), nullable=False)

    recommendations = db.relationship('Recommendation', backref='emotion', lazy=True)

    def __repr__(self):
        return f'<Emotion {self.name}>'
