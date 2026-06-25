import cv2
import numpy as np


def validate_image_size(img: np.ndarray) -> bool:
    h, w = img.shape[:2]
    return h >= 200 and w >= 200


def detect_largest_face(img: np.ndarray) -> tuple[bool, np.ndarray | None, str]:
    """
    Returns (success, face_img, error_message).
    If multiple faces, returns the one with the largest area.
    """
    if not validate_image_size(img):
        return False, None, "La imagen es demasiado pequeña. Mínimo 200x200 px."

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    if len(faces) == 0:
        return False, None, "No se detectó ningún rostro en la imagen."

    # Select face with largest area
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    face_img = img[y:y+h, x:x+w]

    return True, face_img, ""
