from app import db


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    emotion_id = db.Column(db.Integer, db.ForeignKey('emotions.id'), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    song_title = db.Column(db.String(100), nullable=False)
    song_artist = db.Column(db.String(100), nullable=False)
    song_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Recommendation {self.song_title} - {self.song_artist}>'
