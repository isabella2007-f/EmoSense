import os
import cv2
import numpy as np
from deepface import DeepFace

os.environ.setdefault('DEEPFACE_HOME', os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'ai_models')
))

CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.50))


def analyze_emotion(img: np.ndarray) -> tuple[bool, dict, str]:
    """
    Receives a full RGB image array (not pre-cropped).
    DeepFace handles face detection internally.
    Returns (success, result_dict, error_message).
    """
    try:
        result = DeepFace.analyze(
            img_path=img,
            actions=['emotion'],
            detector_backend='retinaface',
            enforce_detection=True,
            silent=True
        )

        # If multiple faces, take the one with highest dominant emotion confidence
        best = max(result, key=lambda r: r['emotion'][r['dominant_emotion']])

        dominant = best['dominant_emotion']
        all_scores = best['emotion']
        confidence = all_scores[dominant] / 100.0

        if confidence < CONFIDENCE_THRESHOLD:
            return False, {}, (
                "No se pudo determinar la emoción con certeza. "
                "Intenta en mejor iluminación."
            )

        return True, {
            'dominant_emotion': dominant,
            'confidence': float(confidence),
            'all_scores': {k: round(float(v) / 100.0, 4) for k, v in all_scores.items()}
        }, ""

    except Exception as e:
        msg = str(e).lower()
        if 'face' in msg or 'detection' in msg or 'cannot' in msg:
            return False, {}, "No se detectó ningún rostro en la imagen."
        return False, {}, "Error al analizar la imagen. Intenta con otra foto."
