# app/models/recommendation.py — Define la tabla 'recommendations' en la base de datos
# Cada fila es una recomendación (imagen + canción) asociada a una emoción

from app import db  # Importa el objeto de conexión a la base de datos


class Recommendation(db.Model):
    # Clase que representa la tabla 'recommendations'

    __tablename__ = 'recommendations'  # Nombre exacto de la tabla en SQLite

    id = db.Column(db.Integer, primary_key=True)
    # Columna 'id': clave primaria autoincremental

    emotion_id = db.Column(db.Integer, db.ForeignKey('emotions.id'), nullable=False)
    # Columna 'emotion_id': clave foránea que apunta a la tabla 'emotions'
    # Indica a qué emoción pertenece esta recomendación (ej: id=1 → happy)

    image_url = db.Column(db.String(300), nullable=False)
    # Columna 'image_url': ruta o URL de la imagen (meme) a mostrar
    # Ejemplo: '/static/img/memes/feliz1.jpg'

    song_title = db.Column(db.String(100), nullable=False)
    # Columna 'song_title': título de la canción recomendada
    # Ejemplo: 'Happy'

    song_artist = db.Column(db.String(100), nullable=False)
    # Columna 'song_artist': nombre del artista de la canción
    # Ejemplo: 'Pharrell Williams'

    song_url = db.Column(db.String(300), nullable=False)
    # Columna 'song_url': enlace a la canción en YouTube u otra plataforma
    # Ejemplo: 'https://www.youtube.com/watch?v=ZbZSe6N_BXs'

    def __repr__(self):
        # Representación en texto del objeto (útil para debug en consola)
        return f'<Recommendation {self.song_title} - {self.song_artist}>'
