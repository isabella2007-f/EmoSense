import cv2
from deepface import DeepFace

img = cv2.imread('foto.jpg')
if img is None:
    print("ERROR: No se encontro foto.jpg")
    exit()

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print('Tamaño:', img.shape[1], 'x', img.shape[0])

for backend in ['opencv', 'ssd', 'mtcnn', 'retinaface']:
    try:
        r = DeepFace.analyze(img_rgb, actions=['emotion'], detector_backend=backend, enforce_detection=True, silent=True)
        print(f'{backend}: OK -> {r[0]["dominant_emotion"]} ({r[0]["emotion"][r[0]["dominant_emotion"]]:.1f}%)')
    except Exception as e:
        print(f'{backend}: FALLO -> {e}')
