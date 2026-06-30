# run.py — Punto de entrada de la aplicación
# Este es el primer archivo que Python ejecuta cuando escribes "python run.py"

from app import create_app  # Importa la función que ensambla toda la app

app = create_app()  # Crea y configura la aplicación Flask completa

if __name__ == '__main__':
    # Solo se ejecuta si corres este archivo directamente (no en producción)
    app.run(debug=app.config['DEBUG'])  # Arranca el servidor; debug=True muestra errores detallados
