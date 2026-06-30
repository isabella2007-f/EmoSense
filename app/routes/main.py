# app/routes/main.py — Rutas de las páginas HTML
# Define qué página HTML mostrar cuando el usuario navega a cada URL

from flask import Blueprint, render_template  # Blueprint para organizar rutas; render_template para cargar HTML

main_bp = Blueprint('main', __name__)
# Crea un Blueprint llamado 'main' — como un mini-router independiente


@main_bp.route('/')
def index():
    # Ruta raíz: cuando el usuario entra a http://localhost:5000/ muestra index.html
    return render_template('index.html')


@main_bp.route('/capture')
def capture_page():
    # Ruta de captura: cuando el usuario va a /capture muestra capture.html
    # Aquí está la cámara y el analizador de emociones
    return render_template('capture.html')


@main_bp.route('/history/page')
def history_page():
    # Ruta del historial: cuando el usuario va a /history/page muestra history.html
    # La página HTML luego llama a /history (API) para obtener los datos
    return render_template('history.html')


@main_bp.app_errorhandler(404)
def not_found(e):
    # Manejador de error 404 (Página no encontrada)
    # Si el usuario entra a una URL que no existe, muestra la página de error con código 404
    return render_template('error.html', error_code=404,
                           error_message='Página no encontrada.'), 404


@main_bp.app_errorhandler(500)
def server_error(e):
    # Manejador de error 500 (Error interno del servidor)
    # Si algo falla inesperadamente en el servidor, muestra la página de error con código 500
    return render_template('error.html', error_code=500,
                           error_message='Error interno del servidor.'), 500
