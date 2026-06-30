# app/routes/history.py — API del historial de análisis
# Define los endpoints para consultar y eliminar el historial de emociones detectadas

import json  # Para convertir el texto JSON de la BD en un diccionario Python
from flask import Blueprint, jsonify, request  # Blueprint, jsonify para respuestas JSON, request para parámetros
from app import db  # Objeto de conexión a la base de datos
from app.models.history import FacialAnalysis, AnalysisHistory  # Modelos del historial
from app.models.recommendation import Recommendation             # Modelo de recomendaciones

history_bp = Blueprint('history', __name__)
# Crea el Blueprint 'history' — agrupa las rutas de este archivo


@history_bp.route('/history', methods=['GET'])
def get_history():
    # Endpoint GET /history — retorna el historial paginado
    # La página de historial llama a esta URL para obtener los datos que muestra

    page = request.args.get('page', 1, type=int)
    # Lee el parámetro 'page' de la URL — ejemplo: /history?page=2
    # Si no se especifica, asume la página 1

    per_page = 10
    # Muestra 10 registros por página

    entries = (AnalysisHistory.query
               .order_by(AnalysisHistory.created_at.desc())
               .paginate(page=page, per_page=per_page, error_out=False))
    # Consulta los registros del historial ordenados del más reciente al más antiguo
    # .paginate() divide los resultados en páginas de 10

    items = []  # Lista vacía donde se acumularán los datos de cada entrada
    for entry in entries.items:
        # Itera sobre cada entrada de historial en la página actual
        analysis = FacialAnalysis.query.get(entry.analysis_id)
        # Obtiene el análisis de imagen asociado a esta entrada (usando FK analysis_id)

        recommendation = Recommendation.query.get(entry.recommendation_id)
        # Obtiene la recomendación asociada a esta entrada (usando FK recommendation_id)

        items.append({
            'history_id': entry.id,                               # ID del registro de historial
            'analysis_id': analysis.id,                           # ID del análisis de imagen
            'emotion': analysis.detected_emotion,                 # Emoción detectada
            'confidence': round(analysis.confidence_score * 100, 1),  # Confianza como porcentaje
            'image_path': analysis.image_path,                    # Ruta de la foto guardada
            'analyzed_at': analysis.analyzed_at.isoformat(),      # Fecha y hora en formato ISO
            'recommendation': {
                'song_title': recommendation.song_title,   # Título de la canción recomendada
                'song_artist': recommendation.song_artist, # Artista
                'song_url': recommendation.song_url,       # Enlace a la canción
                'image_url': recommendation.image_url,     # URL del meme
            } if recommendation else None  # Si no hay recomendación, envía null
        })

    return jsonify({
        'items': items,           # Lista de entradas de la página actual
        'total': entries.total,   # Total de registros en toda la BD
        'pages': entries.pages,   # Número total de páginas
        'current_page': page      # Página actual solicitada
    })


@history_bp.route('/history/<int:history_id>', methods=['GET'])
def get_history_detail(history_id):
    # Endpoint GET /history/<id> — retorna el detalle de una entrada específica del historial
    # Incluye los 7 scores de emoción (útil para la vista de detalle)

    entry = AnalysisHistory.query.get_or_404(history_id)
    # Busca la entrada por ID; si no existe, retorna automáticamente error 404

    analysis = FacialAnalysis.query.get(entry.analysis_id)
    # Obtiene el análisis de imagen asociado

    recommendation = Recommendation.query.get(entry.recommendation_id)
    # Obtiene la recomendación asociada

    return jsonify({
        'history_id': entry.id,                                    # ID del historial
        'emotion': analysis.detected_emotion,                      # Emoción detectada
        'confidence': round(analysis.confidence_score * 100, 1),  # Confianza como porcentaje
        'all_scores': json.loads(analysis.all_scores),             # Los 7 scores (texto JSON → diccionario)
        'image_path': analysis.image_path,                         # Ruta de la foto
        'analyzed_at': analysis.analyzed_at.isoformat(),           # Fecha y hora
        'recommendation': {
            'song_title': recommendation.song_title,   # Título de la canción
            'song_artist': recommendation.song_artist, # Artista
            'song_url': recommendation.song_url,       # Enlace
            'image_url': recommendation.image_url,     # Meme
        } if recommendation else None
    })


@history_bp.route('/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    # Endpoint DELETE /history/<id> — elimina una entrada del historial
    # El usuario puede borrar análisis individuales desde la página de historial

    entry = AnalysisHistory.query.get_or_404(history_id)
    # Busca la entrada; si no existe, retorna 404 automáticamente

    db.session.delete(entry)  # Marca la entrada para eliminar
    db.session.commit()       # Ejecuta la eliminación en la base de datos
    return jsonify({'success': True})  # Confirma que se eliminó correctamente
