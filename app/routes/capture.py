import os
import uuid
import json
import base64
import cv2
import numpy as np
from flask import Blueprint, request, jsonify, current_app

from app import db
from app.services.face_detector import validate_image_size
from app.services.emotion_analyzer import analyze_emotion
from app.services.recommender import get_recommendation
from app.models.history import FacialAnalysis, AnalysisHistory

capture_bp = Blueprint('capture', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(img_bgr: np.ndarray, upload_folder: str) -> str:
    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(upload_folder, filename)
    cv2.imwrite(path, img_bgr)
    return f"captures/{filename}"


@capture_bp.route('/analyze', methods=['POST'])
def analyze():
    img_bgr = None

    # Handle webcam frame sent as base64
    if request.is_json and 'image' in request.json:
        try:
            data = request.json['image']
            if ',' in data:
                data = data.split(',')[1]
            img_bytes = base64.b64decode(data)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except Exception:
            return jsonify({'success': False, 'error': 'Imagen inválida.'}), 400

    # Handle file upload
    elif 'file' in request.files:
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Formato no permitido. Usa JPG o PNG.'}), 400
        np_arr = np.frombuffer(file.read(), np.uint8)
        img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    else:
        return jsonify({'success': False, 'error': 'No se recibió ninguna imagen.'}), 400

    if img_bgr is None:
        return jsonify({'success': False, 'error': 'No se pudo procesar la imagen.'}), 400

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    if not validate_image_size(img_rgb):
        return jsonify({'success': False, 'error': 'La imagen es muy pequeña. Mínimo 200x200 px.'}), 400

    ok, result, error = analyze_emotion(img_rgb)
    if not ok:
        return jsonify({'success': False, 'error': error}), 422

    image_path = save_image(img_bgr, current_app.config['UPLOAD_FOLDER'])

    analysis = FacialAnalysis(
        image_path=image_path,
        detected_emotion=result['dominant_emotion'],
        confidence_score=result['confidence'],
        all_scores=json.dumps(result['all_scores'])
    )
    db.session.add(analysis)
    db.session.flush()

    recommendation = get_recommendation(result['dominant_emotion'])

    history_entry = AnalysisHistory(
        analysis_id=analysis.id,
        recommendation_id=recommendation.id if recommendation else None
    )
    db.session.add(history_entry)

    # Enforce max history limit (FIFO)
    max_history = current_app.config['MAX_HISTORY']
    count = AnalysisHistory.query.count()
    if count > max_history:
        oldest = AnalysisHistory.query.order_by(AnalysisHistory.created_at.asc()).first()
        db.session.delete(oldest)

    db.session.commit()

    return jsonify({
        'success': True,
        'analysis_id': analysis.id,
        'emotion': result['dominant_emotion'],
        'confidence': round(result['confidence'] * 100, 1),
        'all_scores': {k: round(v * 100, 1) for k, v in result['all_scores'].items()},
        'image_path': image_path,
        'recommendation': {
            'image_url': recommendation.image_url,
            'song_title': recommendation.song_title,
            'song_artist': recommendation.song_artist,
            'song_url': recommendation.song_url,
        } if recommendation else None
    })
