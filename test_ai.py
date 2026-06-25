"""
Script de prueba independiente para face_detector y emotion_analyzer.
Uso: python test_ai.py <ruta_imagen>
"""
import sys
import cv2
from app.services.face_detector import validate_image_size
from app.services.emotion_analyzer import analyze_emotion


def test(image_path: str):
    print(f"\nProbando con: {image_path}")

    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print("ERROR: No se pudo cargar la imagen. Verifica la ruta.")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w = img_rgb.shape[:2]
    print(f"Tamaño: {w}x{h} px")

    if not validate_image_size(img_rgb):
        print("ERROR: Imagen muy pequeña. Mínimo 200x200 px.")
        return

    print("Analizando emoción...")
    ok, result, err = analyze_emotion(img_rgb)

    if not ok:
        print(f"FALLÓ — {err}")
        return

    print(f"\nEmoción dominante : {result['dominant_emotion']}")
    print(f"Confianza         : {result['confidence']*100:.1f}%")
    print("\nScores completos:")
    for emotion, score in sorted(result['all_scores'].items(), key=lambda x: -x[1]):
        bar = '█' * int(score * 30)
        print(f"  {emotion:<10} {score*100:5.1f}%  {bar}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python test_ai.py <ruta_imagen>")
    else:
        test(sys.argv[1])
