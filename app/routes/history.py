import json
from flask import Blueprint, jsonify, request
from app import db
from app.models.history import FacialAnalysis, AnalysisHistory
from app.models.recommendation import Recommendation

history_bp = Blueprint('history', __name__)


@history_bp.route('/history', methods=['GET'])
def get_history():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    entries = (AnalysisHistory.query
               .order_by(AnalysisHistory.created_at.desc())
               .paginate(page=page, per_page=per_page, error_out=False))

    items = []
    for entry in entries.items:
        analysis = FacialAnalysis.query.get(entry.analysis_id)
        recommendation = Recommendation.query.get(entry.recommendation_id)
        items.append({
            'history_id': entry.id,
            'analysis_id': analysis.id,
            'emotion': analysis.detected_emotion,
            'confidence': round(analysis.confidence_score * 100, 1),
            'image_path': analysis.image_path,
            'analyzed_at': analysis.analyzed_at.isoformat(),
            'recommendation': {
                'song_title': recommendation.song_title,
                'song_artist': recommendation.song_artist,
                'song_url': recommendation.song_url,
                'image_url': recommendation.image_url,
            } if recommendation else None
        })

    return jsonify({
        'items': items,
        'total': entries.total,
        'pages': entries.pages,
        'current_page': page
    })


@history_bp.route('/history/<int:history_id>', methods=['GET'])
def get_history_detail(history_id):
    entry = AnalysisHistory.query.get_or_404(history_id)
    analysis = FacialAnalysis.query.get(entry.analysis_id)
    recommendation = Recommendation.query.get(entry.recommendation_id)

    return jsonify({
        'history_id': entry.id,
        'emotion': analysis.detected_emotion,
        'confidence': round(analysis.confidence_score * 100, 1),
        'all_scores': json.loads(analysis.all_scores),
        'image_path': analysis.image_path,
        'analyzed_at': analysis.analyzed_at.isoformat(),
        'recommendation': {
            'song_title': recommendation.song_title,
            'song_artist': recommendation.song_artist,
            'song_url': recommendation.song_url,
            'image_url': recommendation.image_url,
        } if recommendation else None
    })


@history_bp.route('/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    entry = AnalysisHistory.query.get_or_404(history_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'success': True})
