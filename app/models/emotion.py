# app/models/emotion.py — Define la tabla 'emotions' en la base de datos
# Esta tabla almacena las 7 emociones que puede detectar el sistema

from app import db  # Importa el objeto de conexión a la base de datos


class Emotion(db.Model):
    # Clase que representa la tabla 'emotions'
    # Cada instancia de esta clase = una fila en la tabla

    __tablename__ = 'emotions'  # Nombre exacto de la tabla en SQLite

    id = db.Column(db.Integer, primary_key=True)
    # Columna 'id': número entero, clave primaria (se autoincrementa: 1, 2, 3...)

    name = db.Column(db.String(20), unique=True, nullable=False)
    # Columna 'name': texto de máx 20 caracteres, único y obligatorio
    # Valores: 'happy', 'sad', 'angry', 'fear', 'surprise', 'disgust', 'neutral'

    label_es = db.Column(db.String(30), nullable=False)
    # Columna 'label_es': etiqueta en español para mostrar en la interfaz
    # Valores: 'Felicidad', 'Tristeza', 'Enojo', etc.

    color_hex = db.Column(db.String(7), nullable=False)
    # Columna 'color_hex': color en formato hexadecimal para el badge de la UI
    # Ejemplo: '#FFD700' (amarillo para felicidad)

    recommendations = db.relationship('Recommendation', backref='emotion', lazy=True)
    # Relación con la tabla Recommendation: permite acceder a emotion.recommendations
    # backref='emotion' crea el acceso inverso: recommendation.emotion

    def __repr__(self):
        # Representación en texto del objeto (útil para debug en consola)
        return f'<Emotion {self.name}>'
