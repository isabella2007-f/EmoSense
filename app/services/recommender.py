# app/services/recommender.py — Selecciona una recomendación para la emoción detectada
# Dado el nombre de una emoción, busca en la base de datos y retorna una recomendación al azar

import random  # Para elegir aleatoriamente entre las opciones disponibles
from app.models.recommendation import Recommendation  # Modelo de la tabla recommendations
from app.models.emotion import Emotion                # Modelo de la tabla emotions


def get_recommendation(emotion_name: str) -> Recommendation | None:
    # Función principal: recibe el nombre de la emoción (ej: 'happy') y retorna una recomendación
    # Retorna None si no se encuentra la emoción o no tiene recomendaciones

    emotion = Emotion.query.filter_by(name=emotion_name).first()
    # Busca en la tabla 'emotions' la fila con ese nombre
    # filter_by(name='happy') → SELECT * FROM emotions WHERE name='happy' LIMIT 1

    if not emotion:
        # Si la emoción no existe en la base de datos, retorna None
        return None

    candidates = Recommendation.query.filter_by(emotion_id=emotion.id).all()
    # Obtiene todas las recomendaciones de esa emoción
    # filter_by(emotion_id=1) → SELECT * FROM recommendations WHERE emotion_id=1
    # Devuelve una lista con las 3 opciones disponibles para esa emoción

    if not candidates:
        # Si no hay recomendaciones para esa emoción, retorna None
        return None

    return random.choice(candidates)
    # Elige una recomendación aleatoria de la lista y la retorna
    # Esto hace que cada vez que detectas la misma emoción, pueda salir un meme o canción diferente
