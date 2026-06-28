from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/capture')
def capture_page():
    return render_template('capture.html')


@main_bp.route('/history/page')
def history_page():
    return render_template('history.html')


@main_bp.app_errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404,
                           error_message='Página no encontrada.'), 404


@main_bp.app_errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500,
                           error_message='Error interno del servidor.'), 500
