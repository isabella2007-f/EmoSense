from app import create_app, db
from app.models.emotion import Emotion
from app.models.recommendation import Recommendation

EMOTIONS = [
    {'name': 'happy',    'label_es': 'Felicidad', 'color_hex': '#FFD700'},
    {'name': 'sad',      'label_es': 'Tristeza',  'color_hex': '#4A90D9'},
    {'name': 'angry',    'label_es': 'Enojo',     'color_hex': '#E74C3C'},
    {'name': 'fear',     'label_es': 'Miedo',     'color_hex': '#8E44AD'},
    {'name': 'surprise', 'label_es': 'Sorpresa',  'color_hex': '#F39C12'},
    {'name': 'disgust',  'label_es': 'Disgusto',  'color_hex': '#27AE60'},
    {'name': 'neutral',  'label_es': 'Neutral',   'color_hex': '#95A5A6'},
]

RECOMMENDATIONS = {
    'happy': [
        {'image_url': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400', 'song_title': 'Happy', 'song_artist': 'Pharrell Williams', 'song_url': 'https://www.youtube.com/watch?v=ZbZSe6N_BXs'},
        {'image_url': 'https://images.unsplash.com/photo-1516802273409-68526ee1bdd6?w=400', 'song_title': 'Good as Hell', 'song_artist': 'Lizzo', 'song_url': 'https://www.youtube.com/watch?v=SmbmeOgWsqE'},
        {'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400', 'song_title': 'Can\'t Stop the Feeling', 'song_artist': 'Justin Timberlake', 'song_url': 'https://www.youtube.com/watch?v=ru0K8uYEZWw'},
    ],
    'sad': [
        {'image_url': 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=400', 'song_title': 'The Night We Met', 'song_artist': 'Lord Huron', 'song_url': 'https://www.youtube.com/watch?v=KtlgYxa6BMU'},
        {'image_url': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=400', 'song_title': 'Someone Like You', 'song_artist': 'Adele', 'song_url': 'https://www.youtube.com/watch?v=hLQl3WQQoQ0'},
        {'image_url': 'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=400', 'song_title': 'Fix You', 'song_artist': 'Coldplay', 'song_url': 'https://www.youtube.com/watch?v=k4V3Mo61fJM'},
    ],
    'angry': [
        {'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400', 'song_title': 'Break Stuff', 'song_artist': 'Limp Bizkit', 'song_url': 'https://www.youtube.com/watch?v=ZpUYjpKg9KY'},
        {'image_url': 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=400', 'song_title': 'In The End', 'song_artist': 'Linkin Park', 'song_url': 'https://www.youtube.com/watch?v=eVTXPUF4Oz4'},
        {'image_url': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400', 'song_title': 'Killing in the Name', 'song_artist': 'Rage Against the Machine', 'song_url': 'https://www.youtube.com/watch?v=bWXazVhlyxQ'},
    ],
    'fear': [
        {'image_url': 'https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=400', 'song_title': 'Breathe (2 AM)', 'song_artist': 'Anna Nalick', 'song_url': 'https://www.youtube.com/watch?v=F-vne8LDSEo'},
        {'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400', 'song_title': 'Don\'t Panic', 'song_artist': 'Coldplay', 'song_url': 'https://www.youtube.com/watch?v=yNMoFbFpBkE'},
        {'image_url': 'https://images.unsplash.com/photo-1519834785169-98be25ec3f84?w=400', 'song_title': 'Safe & Sound', 'song_artist': 'Taylor Swift', 'song_url': 'https://www.youtube.com/watch?v=igSL0DFO4CE'},
    ],
    'surprise': [
        {'image_url': 'https://images.unsplash.com/photo-1513151233558-d860c5398176?w=400', 'song_title': 'Surprise Yourself', 'song_artist': 'Jack Garratt', 'song_url': 'https://www.youtube.com/watch?v=0_l7HkY8jTM'},
        {'image_url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400', 'song_title': 'Dancing Queen', 'song_artist': 'ABBA', 'song_url': 'https://www.youtube.com/watch?v=xFrGuyw1V8s'},
        {'image_url': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400', 'song_title': 'Uptown Funk', 'song_artist': 'Mark Ronson ft. Bruno Mars', 'song_url': 'https://www.youtube.com/watch?v=OPf0YbXqDm0'},
    ],
    'disgust': [
        {'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400', 'song_title': 'Let It Be', 'song_artist': 'The Beatles', 'song_url': 'https://www.youtube.com/watch?v=QDYfEBY9NM4'},
        {'image_url': 'https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=400', 'song_title': 'Here Comes the Sun', 'song_artist': 'The Beatles', 'song_url': 'https://www.youtube.com/watch?v=KQetemT1sWc'},
        {'image_url': 'https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07?w=400', 'song_title': 'What a Wonderful World', 'song_artist': 'Louis Armstrong', 'song_url': 'https://www.youtube.com/watch?v=CWzrABouyeE'},
    ],
    'neutral': [
        {'image_url': 'https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?w=400', 'song_title': 'Lo-Fi Study Beats', 'song_artist': 'ChilledCow', 'song_url': 'https://www.youtube.com/watch?v=5qap5aO4i9A'},
        {'image_url': 'https://images.unsplash.com/photo-1477346611705-65d1883cee1e?w=400', 'song_title': 'Clair de Lune', 'song_artist': 'Debussy', 'song_url': 'https://www.youtube.com/watch?v=CvFH_6DNRCY'},
        {'image_url': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=400', 'song_title': 'Experience', 'song_artist': 'Ludovico Einaudi', 'song_url': 'https://www.youtube.com/watch?v=hN_q-_nGv4U'},
    ],
}


def run_seed():
    app = create_app()
    with app.app_context():
        if Emotion.query.count() > 0:
            print("La base de datos ya tiene datos. Seed omitido.")
            return

        for e in EMOTIONS:
            emotion = Emotion(**e)
            db.session.add(emotion)
        db.session.flush()

        for emotion_name, recs in RECOMMENDATIONS.items():
            emotion = Emotion.query.filter_by(name=emotion_name).first()
            for r in recs:
                rec = Recommendation(emotion_id=emotion.id, **r)
                db.session.add(rec)

        db.session.commit()
        print(f"Seed completado: {len(EMOTIONS)} emociones, {sum(len(v) for v in RECOMMENDATIONS.values())} recomendaciones.")


if __name__ == '__main__':
    run_seed()
