# app/services/face_detector.py — Validación y detección de rostros
# Funciones auxiliares para verificar que la imagen es válida antes de pasarla a la IA

import cv2      # OpenCV: librería de visión por computadora para procesar imágenes
import numpy as np  # NumPy: para manipular la imagen como array de números


def validate_image_size(img: np.ndarray) -> bool:
    # Verifica que la imagen tenga al menos 200x200 píxeles
    # La IA necesita cierta resolución mínima para detectar correctamente los rasgos faciales

    h, w = img.shape[:2]    # Extrae alto (h) y ancho (w) de las dimensiones de la imagen
    return h >= 200 and w >= 200  # Retorna True si cumple el mínimo, False si es muy pequeña


def detect_largest_face(img: np.ndarray) -> tuple[bool, np.ndarray | None, str]:
    # Detecta rostros en la imagen usando el clasificador de OpenCV (Haar Cascade)
    # Si hay múltiples rostros, retorna el más grande (el más cercano a la cámara)
    # Retorna: (éxito, imagen_del_rostro, mensaje_de_error)
    # NOTA: Esta función existe como respaldo; el análisis principal usa DeepFace directamente

    if not validate_image_size(img):
        # Si la imagen es muy pequeña, no tiene sentido buscar rostros
        return False, None, "La imagen es demasiado pequeña. Mínimo 200x200 px."

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Convierte la imagen a escala de grises — el detector Haar trabaja mejor en grises

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Carga el clasificador preentrenado de OpenCV para detectar caras frontales

    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    # Busca rostros en la imagen
    # scaleFactor=1.1: reduce la imagen 10% en cada escala para detectar caras de distintos tamaños
    # minNeighbors=5: cuántas detecciones vecinas se necesitan para confirmar un rostro (evita falsos positivos)
    # minSize=(60,60): tamaño mínimo del rostro a detectar en píxeles

    if len(faces) == 0:
        # Si no se encontró ningún rostro, retorna error
        return False, None, "No se detectó ningún rostro en la imagen."

    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    # De todos los rostros encontrados, selecciona el de mayor área (ancho * alto)
    # x, y: coordenadas de la esquina superior izquierda del rostro
    # w, h: ancho y alto del recuadro del rostro

    face_img = img[y:y+h, x:x+w]
    # Recorta solo la región del rostro de la imagen original

    return True, face_img, ""  # Retorna éxito, imagen del rostro recortado, sin error
