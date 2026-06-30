# app/services/emotion_analyzer.py — El cerebro de la IA
# Este archivo es el más importante del proyecto: aquí DeepFace analiza las emociones

import os           # Para manejar rutas del sistema de archivos
import cv2          # OpenCV: para procesar la imagen antes de pasarla a DeepFace
import numpy as np  # NumPy: para manejar la imagen como array de números
from deepface import DeepFace  # La librería de IA que detecta emociones faciales

os.environ.setdefault('DEEPFACE_HOME', os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'ai_models')
))
# Le dice a DeepFace dónde guardar los modelos descargados (carpeta ai_models/)
# La primera vez que se usa, descarga ~500 MB de modelos de IA automáticamente

CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.50))
# Umbral mínimo de confianza: si la IA no está al menos 50% segura, rechaza el resultado


def analyze_emotion(img: np.ndarray) -> tuple[bool, dict, str]:
    # Función principal: recibe una imagen RGB y retorna la emoción detectada
    # Retorna: (éxito, diccionario_con_resultados, mensaje_de_error)

    try:
        result = DeepFace.analyze(
            img_path=img,                    # La imagen como array NumPy (RGB)
            actions=['emotion'],             # Solo analizar emociones (no edad, género ni raza)
            detector_backend='opencv',       # Algoritmo para detectar el rostro
            enforce_detection=True,          # Si no hay rostro → lanza excepción (no devuelve basura)
            silent=True                      # No imprime mensajes en la consola
        )
        # result es una lista de diccionarios, uno por cada rostro detectado
        # Ejemplo: [{'dominant_emotion': 'happy', 'emotion': {'happy': 87.3, 'sad': 3.1, ...}}]

        best = max(result, key=lambda r: r['emotion'][r['dominant_emotion']])
        # Si hay varios rostros en la imagen, selecciona el más confiable
        # (el que tiene el porcentaje más alto en su emoción dominante)

        dominant = best['dominant_emotion']
        # La emoción con el porcentaje más alto — ejemplo: 'happy'

        all_scores = best['emotion']
        # Diccionario con los 7 porcentajes — ejemplo: {'happy': 87.3, 'sad': 3.1, 'angry': 2.0, ...}

        confidence = all_scores[dominant] / 100.0
        # Normaliza la confianza de 0-100 a 0.0-1.0 — ejemplo: 87.3 → 0.873

        if confidence < CONFIDENCE_THRESHOLD:
            # Si la IA no está suficientemente segura, rechaza el resultado
            return False, {}, (
                "No se pudo determinar la emoción con certeza. "
                "Intenta en mejor iluminación."
            )

        return True, {
            'dominant_emotion': dominant,                                    # Emoción ganadora
            'confidence': float(confidence),                                 # Confianza en 0.0-1.0
            'all_scores': {k: round(float(v) / 100.0, 4) for k, v in all_scores.items()}
            # Todos los scores normalizados a 0.0-1.0 con 4 decimales
        }, ""  # Sin mensaje de error

    except Exception as e:
        # Captura cualquier error que lance DeepFace
        msg = str(e).lower()  # Convierte el mensaje a minúsculas para comparar
        if 'face' in msg or 'detection' in msg or 'cannot' in msg:
            # Si el error menciona "face" o "detection", probablemente no hay rostro
            return False, {}, "No se detectó ningún rostro en la imagen."
        # Para cualquier otro error inesperado
        return False, {}, "Error al analizar la imagen. Intenta con otra foto."
