import random
from app.models.recommendation import Recommendation
from app.models.emotion import Emotion


def get_recommendation(emotion_name: str) -> Recommendation | None:
    emotion = Emotion.query.filter_by(name=emotion_name).first()
    if not emotion:
        return None

    candidates = Recommendation.query.filter_by(emotion_id=emotion.id).all()
    if not candidates:
        return None

    return random.choice(candidates)
