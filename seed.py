# seed.py — Rellena la base de datos con los datos iniciales
# Se ejecuta UNA SOLA VEZ antes de usar la app por primera vez

from app import create_app, db                    # Importa la app y el objeto de base de datos
from app.models.emotion import Emotion            # Modelo de la tabla de emociones
from app.models.recommendation import Recommendation  # Modelo de la tabla de recomendaciones

# Lista de las 7 emociones básicas que detecta DeepFace
EMOTIONS = [
    {'name': 'happy',    'label_es': 'Felicidad', 'color_hex': '#FFD700'},  # Amarillo
    {'name': 'sad',      'label_es': 'Tristeza',  'color_hex': '#4A90D9'},  # Azul
    {'name': 'angry',    'label_es': 'Enojo',     'color_hex': '#E74C3C'},  # Rojo
    {'name': 'fear',     'label_es': 'Miedo',     'color_hex': '#8E44AD'},  # Morado
    {'name': 'surprise', 'label_es': 'Sorpresa',  'color_hex': '#F39C12'},  # Naranja
    {'name': 'disgust',  'label_es': 'Disgusto',  'color_hex': '#27AE60'},  # Verde
    {'name': 'neutral',  'label_es': 'Neutral',   'color_hex': '#95A5A6'},  # Gris
]

# Diccionario de recomendaciones: 3 opciones de imagen + canción por cada emoción
# La app elige una al azar cada vez que detecta esa emoción
RECOMMENDATIONS = {
    'happy': [
        {'image_url': '/static/img/memes/feliz1.jpg', 'song_title': 'Happy', 'song_artist': 'Pharrell Williams', 'song_url': 'https://www.youtube.com/watch?v=ZbZSe6N_BXs'},
        {'image_url': '/static/img/memes/feliz2.png', 'song_title': 'Good as Hell', 'song_artist': 'Lizzo', 'song_url': 'https://www.youtube.com/watch?v=SmbmeOgWsqE'},
        {'image_url': '/static/img/memes/feliz3.jpg', 'song_title': 'Can\'t Stop the Feeling', 'song_artist': 'Justin Timberlake', 'song_url': 'https://www.youtube.com/watch?v=ru0K8uYEZWw'},
    ],
    'sad': [
        {'image_url': '/static/img/memes/triste1.jpg', 'song_title': 'The Night We Met', 'song_artist': 'Lord Huron', 'song_url': 'https://www.youtube.com/watch?v=KtlgYxa6BMU'},
        {'image_url': '/static/img/memes/triste2.jpg', 'song_title': 'Someone Like You', 'song_artist': 'Adele', 'song_url': 'https://www.youtube.com/watch?v=hLQl3WQQoQ0'},
        {'image_url': '/static/img/memes/triste3.jpg', 'song_title': 'Fix You', 'song_artist': 'Coldplay', 'song_url': 'https://www.youtube.com/watch?v=k4V3Mo61fJM'},
    ],
    'angry': [
        {'image_url': '/static/img/memes/enojo1.jpg', 'song_title': 'Break Stuff', 'song_artist': 'Limp Bizkit', 'song_url': 'https://www.youtube.com/watch?v=ZpUYjpKg9KY'},
        {'image_url': '/static/img/memes/enojo2.jpg', 'song_title': 'In The End', 'song_artist': 'Linkin Park', 'song_url': 'https://www.youtube.com/watch?v=eVTXPUF4Oz4'},
        {'image_url': '/static/img/memes/enojo3.jpg', 'song_title': 'Killing in the Name', 'song_artist': 'Rage Against the Machine', 'song_url': 'https://www.youtube.com/watch?v=bWXazVhlyxQ'},
    ],
    'fear': [
        {'image_url': '/static/img/memes/miedo1.jpg', 'song_title': 'Breathe (2 AM)', 'song_artist': 'Anna Nalick', 'song_url': 'https://www.youtube.com/watch?v=F-vne8LDSEo'},
        {'image_url': '/static/img/memes/miedo2.jpg', 'song_title': 'Don\'t Panic', 'song_artist': 'Coldplay', 'song_url': 'https://www.youtube.com/watch?v=yNMoFbFpBkE'},
        {'image_url': '/static/img/memes/miedo3.jpg', 'song_title': 'Safe & Sound', 'song_artist': 'Taylor Swift', 'song_url': 'https://www.youtube.com/watch?v=igSL0DFO4CE'},
    ],
    'surprise': [
        {'image_url': '/static/img/memes/sorpresa1.jpg', 'song_title': 'Surprise Yourself', 'song_artist': 'Jack Garratt', 'song_url': 'https://www.youtube.com/watch?v=0_l7HkY8jTM'},
        {'image_url': '/static/img/memes/sorpresa2.jpg', 'song_title': 'Dancing Queen', 'song_artist': 'ABBA', 'song_url': 'https://www.youtube.com/watch?v=xFrGuyw1V8s'},
        {'image_url': '/static/img/memes/sorpresa3.jpg', 'song_title': 'Uptown Funk', 'song_artist': 'Mark Ronson ft. Bruno Mars', 'song_url': 'https://www.youtube.com/watch?v=OPf0YbXqDm0'},
    ],
    'disgust': [
        {'image_url': '/static/img/memes/disgusto1.jpg', 'song_title': 'Let It Be', 'song_artist': 'The Beatles', 'song_url': 'https://www.youtube.com/watch?v=QDYfEBY9NM4'},
        {'image_url': '/static/img/memes/disgusto2.jpg', 'song_title': 'Here Comes the Sun', 'song_artist': 'The Beatles', 'song_url': 'https://www.youtube.com/watch?v=KQetemT1sWc'},
        {'image_url': '/static/img/memes/disgusto3.jpg', 'song_title': 'What a Wonderful World', 'song_artist': 'Louis Armstrong', 'song_url': 'https://www.youtube.com/watch?v=CWzrABouyeE'},
    ],
    'neutral': [
        {'image_url': '/static/img/memes/lobo1.jpg', 'song_title': 'Lo-Fi Study Beats', 'song_artist': 'ChilledCow', 'song_url': 'https://www.youtube.com/watch?v=5qap5aO4i9A'},
        {'image_url': '/static/img/memes/lobo2.jpg', 'song_title': 'Clair de Lune', 'song_artist': 'Debussy', 'song_url': 'https://www.youtube.com/watch?v=CvFH_6DNRCY'},
        {'image_url': '/static/img/memes/neutral.jpg', 'song_title': 'Experience', 'song_artist': 'Ludovico Einaudi', 'song_url': 'https://www.youtube.com/watch?v=hN_q-_nGv4U'},
    ],
}


def run_seed():
    app = create_app()              # Crea la app para tener acceso a la base de datos
    with app.app_context():         # Activa el contexto de Flask (necesario para usar db)

        if Emotion.query.count() > 0:
            # Si ya hay emociones en la base de datos, no vuelve a insertar
            print("La base de datos ya tiene datos. Seed omitido.")
            return

        # Inserta las 7 emociones en la tabla 'emotions'
        for e in EMOTIONS:
            emotion = Emotion(**e)      # Crea un objeto Emotion con los datos del diccionario
            db.session.add(emotion)     # Lo agrega a la sesión (aún no se guarda en disco)
        db.session.flush()              # Asigna IDs a las emociones sin hacer commit todavía

        # Inserta las recomendaciones vinculadas a cada emoción
        for emotion_name, recs in RECOMMENDATIONS.items():
            emotion = Emotion.query.filter_by(name=emotion_name).first()  # Busca la emoción por nombre
            for r in recs:
                rec = Recommendation(emotion_id=emotion.id, **r)  # Crea la recomendación con el FK
                db.session.add(rec)     # La agrega a la sesión

        db.session.commit()  # Guarda todo en la base de datos de una sola vez
        print(f"Seed completado: {len(EMOTIONS)} emociones, {sum(len(v) for v in RECOMMENDATIONS.values())} recomendaciones.")


if __name__ == '__main__':
    run_seed()  # Ejecuta el seed solo si corres "python seed.py" directamente
