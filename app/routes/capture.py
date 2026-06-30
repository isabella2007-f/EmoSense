# app/routes/capture.py — Ruta principal de análisis de imágenes
# Este archivo recibe la imagen del usuario, la procesa, y devuelve la emoción detectada

import os       # Para manejar rutas de archivos en el sistema
import uuid     # Para generar nombres únicos de archivo (evita colisiones)
import json     # Para convertir diccionarios a texto JSON (para guardar en BD)
import base64   # Para decodificar imágenes enviadas desde el navegador en formato base64
import cv2      # OpenCV: para decodificar y guardar imágenes
import numpy as np  # NumPy: para manejar imágenes como arrays de números
from flask import Blueprint, request, jsonify, current_app
# Blueprint: organiza las rutas | request: datos recibidos | jsonify: convierte a JSON | current_app: accede a la config

from app import db  # Objeto de conexión a la base de datos
from app.services.face_detector import validate_image_size    # Verifica que la imagen tenga tamaño mínimo
from app.services.emotion_analyzer import analyze_emotion     # Llama a DeepFace para analizar la emoción
from app.services.recommender import get_recommendation       # Busca una recomendación en la BD
from app.models.history import FacialAnalysis, AnalysisHistory  # Modelos para guardar en la BD

capture_bp = Blueprint('capture', __name__)
# Crea el Blueprint 'capture' — agrupa todas las rutas de este archivo

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
# Solo se aceptan estos formatos de imagen


def allowed_file(filename: str) -> bool:
    # Verifica que el archivo tenga una extensión permitida
    # Ejemplo: 'foto.jpg' → True | 'documento.pdf' → False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(img_bgr: np.ndarray, upload_folder: str) -> str:
    # Guarda la imagen en disco con un nombre único generado con UUID
    # Retorna la ruta relativa donde quedó guardada (para mostrarla en el historial)
    filename = f"{uuid.uuid4().hex}.jpg"          # Genera un nombre único como '3f8a29b1c4d5.jpg'
    path = os.path.join(upload_folder, filename)  # Ruta completa en disco
    cv2.imwrite(path, img_bgr)                    # Guarda la imagen en formato JPG
    return f"captures/{filename}"                 # Retorna la ruta relativa (sin la carpeta raíz)


@capture_bp.route('/analyze', methods=['POST'])
def analyze():
    # Endpoint principal: recibe una imagen y retorna la emoción detectada
    # Acepta dos formatos: JSON con imagen en base64 (cámara) o archivo subido (upload)

    img_bgr = None   # Variable que contendrá la imagen como array NumPy en formato BGR
    save = True      # Por defecto, guarda el análisis en la base de datos

    if request.is_json and 'image' in request.json:
        # CASO 1: La imagen llega como texto base64 dentro de un JSON
        # Esto es lo que usa la cámara en vivo y el modo snapshot del navegador
        save = bool(request.json.get('save', True))  # Lee si se debe guardar (por defecto sí)
        try:
            data = request.json['image']   # El texto base64 de la imagen
            if ',' in data:
                data = data.split(',')[1]  # Elimina el prefijo 'data:image/jpeg;base64,' si existe
            img_bytes = base64.b64decode(data)             # Convierte base64 → bytes
            np_arr = np.frombuffer(img_bytes, np.uint8)    # Convierte bytes → array NumPy
            img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decodifica el array → imagen BGR
        except Exception:
            return jsonify({'success': False, 'error': 'Imagen inválida.'}), 400

    elif 'file' in request.files:
        # CASO 2: La imagen llega como archivo subido por el formulario
        # Esto es lo que usa el modo "Subir imagen"
        file = request.files['file']  # Obtiene el archivo del formulario HTML
        if not file or not allowed_file(file.filename):
            # Verifica que el archivo exista y tenga extensión permitida
            return jsonify({'success': False, 'error': 'Formato no permitido. Usa JPG o PNG.'}), 400
        np_arr = np.frombuffer(file.read(), np.uint8)    # Lee los bytes del archivo → array NumPy
        img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decodifica → imagen BGR

    else:
        # Si no llegó ni base64 ni archivo, retorna error
        return jsonify({'success': False, 'error': 'No se recibió ninguna imagen.'}), 400

    if img_bgr is None:
        # Si la decodificación falló por cualquier razón
        return jsonify({'success': False, 'error': 'No se pudo procesar la imagen.'}), 400

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # CONVERSIÓN CRÍTICA: OpenCV lee imágenes en BGR (azul-verde-rojo)
    # DeepFace espera imágenes en RGB (rojo-verde-azul)
    # Sin esta conversión, los colores estarían invertidos y la IA detectaría mal

    if not validate_image_size(img_rgb):
        # Verifica que la imagen sea al menos 200x200 píxeles
        return jsonify({'success': False, 'error': 'La imagen es muy pequeña. Mínimo 200x200 px.'}), 400

    ok, result, error = analyze_emotion(img_rgb)
    # Llama a DeepFace para analizar la emoción
    # ok=True si tuvo éxito, result=diccionario con emoción y confianza, error=mensaje si falló
    if not ok:
        return jsonify({'success': False, 'error': error}), 422

    recommendation = get_recommendation(result['dominant_emotion'])
    # Busca en la base de datos una recomendación aleatoria para esa emoción

    if save:
        # Guarda el análisis y el historial en la base de datos
        image_path = save_image(img_bgr, current_app.config['UPLOAD_FOLDER'])
        # Guarda la imagen en disco y obtiene su ruta relativa

        analysis = FacialAnalysis(
            image_path=image_path,                          # Dónde quedó guardada la foto
            detected_emotion=result['dominant_emotion'],    # Emoción detectada
            confidence_score=result['confidence'],          # Porcentaje de confianza
            all_scores=json.dumps(result['all_scores'])     # Los 7 scores como texto JSON
        )
        db.session.add(analysis)  # Agrega el análisis a la sesión (pendiente de guardar)
        db.session.flush()        # Asigna un ID al análisis sin hacer commit todavía

        history_entry = AnalysisHistory(
            analysis_id=analysis.id,                                      # FK al análisis
            recommendation_id=recommendation.id if recommendation else None  # FK a la recomendación
        )
        db.session.add(history_entry)  # Agrega la entrada de historial a la sesión

        max_history = current_app.config['MAX_HISTORY']  # Límite máximo del historial (ej: 100)
        count = AnalysisHistory.query.count()             # Cuenta cuántos registros hay actualmente
        if count > max_history:
            # Si se superó el límite, elimina el registro más antiguo (FIFO: primero en entrar, primero en salir)
            oldest = AnalysisHistory.query.order_by(AnalysisHistory.created_at.asc()).first()
            db.session.delete(oldest)

        db.session.commit()      # Guarda todo en la base de datos de una sola vez
        analysis_id = analysis.id  # Guarda el ID para incluirlo en la respuesta
    else:
        # Si save=False, no guarda nada en la base de datos (modo sin persistencia)
        image_path = None
        analysis_id = None

    return jsonify({
        'success': True,                                              # Indica que todo salió bien
        'analysis_id': analysis_id,                                   # ID del análisis guardado
        'emotion': result['dominant_emotion'],                        # Emoción detectada (en inglés)
        'confidence': round(result['confidence'] * 100, 1),          # Confianza como porcentaje (ej: 87.3)
        'all_scores': {k: round(v * 100, 1) for k, v in result['all_scores'].items()},
        # Los 7 scores como porcentajes — el JavaScript los usa para la barra de progreso
        'image_path': image_path,  # Ruta de la imagen guardada
        'recommendation': {
            'image_url': recommendation.image_url,     # URL del meme
            'song_title': recommendation.song_title,   # Título de la canción
            'song_artist': recommendation.song_artist, # Artista
            'song_url': recommendation.song_url,       # Enlace a YouTube
        } if recommendation else None  # Si no hay recomendación, envía null
    })
