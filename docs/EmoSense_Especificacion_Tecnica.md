# EmoSense — Especificación Técnica
> Reconocimiento de Emociones Faciales con IA

---

## 1. Descripción general

EmoSense es una aplicación web desarrollada con Python y Flask que utiliza inteligencia artificial para detectar y clasificar emociones humanas a partir del análisis de expresiones faciales. El sistema procesa el rostro del usuario desde una imagen cargada o capturada con la cámara, identifica la emoción predominante y entrega contenido multimedia personalizado (imagen y canción) acorde al estado emocional detectado.

El sistema soporta 7 emociones básicas:

- Felicidad (happy)
- Tristeza (sad)
- Enojo (angry)
- Miedo (fear)
- Sorpresa (surprise)
- Disgusto (disgust)
- Neutralidad (neutral)

---

## 2. Objetivo

### Objetivo principal

Identificar automáticamente el estado emocional de un usuario mediante visión por computadora e IA, entregando contenido personalizado basado en la emoción detectada.

### Objetivos secundarios

- Proveer una interfaz web intuitiva para captura de imagen o uso de cámara en tiempo real.
- Recomendar contenido multimedia (imagen y canción) según la emoción detectada.
- Registrar y consultar el historial de análisis emocionales realizados.
- Garantizar que el sistema maneje errores correctamente (sin rostro, baja confianza, cámara no disponible).

---

## 3. Tecnologías

### Backend

| Librería | Versión | Uso |
|---|---|---|
| Python | 3.10+ | Lenguaje principal |
| Flask | 3.x | Framework web |
| Flask-SQLAlchemy | latest | ORM para base de datos |
| Flask-Migrate | latest | Migraciones de base de datos |
| python-dotenv | latest | Variables de entorno desde .env |

### Inteligencia Artificial y Visión por Computadora

| Librería | Uso |
|---|---|
| DeepFace | Librería principal: detección facial + clasificación de emociones |
| opencv-python | Captura de video, preprocesamiento y manipulación de imágenes |
| NumPy | Operaciones matriciales sobre arrays de imagen |
| Pillow | Carga y conversión de formatos de imagen |

> **¿Por qué DeepFace?** Con una sola llamada `DeepFace.analyze()` entrega las 7 emociones básicas, el score de confianza de cada una y la emoción dominante. No requiere entrenar ningún modelo propio. Internamente usa VGG-Face, Facenet o RetinaFace según se configure. Tiene API simple y es activamente mantenida.

### Base de datos

- **SQLite** — base de datos local sin servidor, ideal para aplicaciones educativas o de escritorio.

### Frontend

- HTML5 + CSS3 + JavaScript (vanilla)
- Jinja2 — motor de plantillas incluido en Flask
- Bootstrap 5 — componentes UI responsivos

---

## 4. Arquitectura

La aplicación sigue el patrón **MVC (Model-View-Controller)** implementado con Flask Blueprints. La lógica de negocio (servicios de IA, recomendaciones) se separa completamente de las rutas HTTP.

### Estructura de carpetas

```
emosense/
├── app/
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuración y variables de entorno
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── emotion.py
│   │   ├── recommendation.py
│   │   └── history.py
│   ├── routes/                  # Blueprints Flask (controladores)
│   │   ├── main.py              # Ruta de inicio
│   │   ├── capture.py           # Captura y análisis
│   │   └── history.py           # Historial
│   ├── services/                # Lógica de negocio (IA)
│   │   ├── face_detector.py
│   │   ├── emotion_analyzer.py
│   │   └── recommender.py
│   ├── static/                  # CSS, JS, imágenes estáticas
│   │   └── captures/            # Imágenes capturadas por el usuario
│   └── templates/               # Plantillas HTML Jinja2
├── ai_models/                   # Pesos de modelos descargados por DeepFace
├── database/
│   └── emosense.db
├── migrations/
├── .env
├── requirements.txt
└── run.py
```

> **NUEVO** — Se agregó la carpeta `services/` para separar la lógica de IA de las rutas HTTP. Sin esta separación, los controladores se vuelven imposibles de probar y mantener.

---

## 5. Módulos

### Módulo 1 — Captura (`routes/capture.py`)
Gestiona la recepción de imágenes: upload de archivo o fotograma de webcam enviado por JavaScript. Valida formato y tamaño mínimo antes de pasar al pipeline de IA.

### Módulo 2 — Detección facial (`services/face_detector.py`)
Verifica que la imagen contenga al menos un rostro válido usando OpenCV o DeepFace. Si hay múltiples rostros, selecciona el de mayor área. Si no hay ninguno, retorna un error controlado.

### Módulo 3 — Análisis de emociones (`services/emotion_analyzer.py`)
Recibe la imagen preprocesada y ejecuta `DeepFace.analyze()` con la acción `emotion`. Retorna la emoción dominante, su score de confianza y el diccionario completo de scores.

### Módulo 4 — Recomendaciones (`services/recommender.py`)
Consulta la base de datos y retorna aleatoriamente una imagen y una canción de entre las precargadas para la emoción detectada.

### Módulo 5 — Historial (`routes/history.py`)
Permite listar, ver el detalle y eliminar registros de análisis anteriores almacenados en la base de datos.

### Módulo 6 — Configuración (`config.py` + `.env`)
Centraliza todos los parámetros configurables: umbral de confianza, máximo de registros en historial, directorio de capturas, modo debug.

---

## 6. Entidades principales

### Emotion (tabla: `emotions`)

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Clave primaria |
| name | String | Nombre en inglés (happy, sad, angry, fear, surprise, disgust, neutral) |
| label_es | String | Etiqueta en español para mostrar en UI |
| color_hex | String | Color de acento en la interfaz |

### FacialAnalysis (tabla: `facial_analyses`)

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Clave primaria |
| image_path | String | Ruta relativa de la imagen procesada |
| detected_emotion | String | Emoción dominante detectada |
| confidence_score | Float | Valor entre 0.0 y 1.0 |
| all_scores | JSON | Scores de las 7 emociones (guardado como texto JSON) |
| analyzed_at | DateTime | Marca de tiempo del análisis |

### Recommendation (tabla: `recommendations`)

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Clave primaria |
| emotion_id | Integer | FK a Emotion |
| image_url | String | URL o ruta de la imagen recomendada |
| song_title | String | Título de la canción |
| song_artist | String | Artista |
| song_url | String | URL a la canción (YouTube, Spotify, etc.) |

### AnalysisHistory (tabla: `analysis_history`)

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Clave primaria |
| analysis_id | Integer | FK a FacialAnalysis |
| recommendation_id | Integer | FK a Recommendation |
| created_at | DateTime | Fecha de creación del registro |

> **NUEVO** — Se agregó el campo `all_scores` en `FacialAnalysis` para guardar los scores de las 7 emociones, no solo la dominante. Esto permite mostrar gráficas de distribución emocional en el historial.

---

## 7. Funcionalidades

- Capturar imagen desde webcam en tiempo real mediante el navegador.
- Subir imagen estática desde el dispositivo (JPG, PNG).
- Preprocesar la imagen: conversión BGR a RGB, redimensionado mínimo a 200×200 px.
- Detectar si hay un rostro válido en la imagen.
- Clasificar la emoción dominante con DeepFace y obtener su score de confianza.
- Mostrar la emoción detectada con su porcentaje de confianza.
- Mostrar los scores de las 7 emociones en forma de barra de progreso.
- Recomendar una imagen y una canción según la emoción detectada.
- Guardar el análisis y la recomendación en el historial local.
- Consultar el historial paginado de análisis anteriores.
- Eliminar registros individuales del historial.
- Manejar errores sin bloquear la aplicación: sin rostro, baja confianza, cámara no disponible.

> **NUEVO** — Se agregó mostrar los scores de las 7 emociones. En sistemas de ML es importante que el usuario vea el nivel de certeza del modelo, no solo un resultado único.

---

## 8. Gestión de estado

El estado de la aplicación se gestiona en el frontend con JavaScript (manipulación de clases CSS + fetch API para llamadas AJAX al backend).

| Estado | Descripción |
|---|---|
| `idle` | Pantalla de inicio, esperando acción del usuario |
| `capturing` | Cámara activada o área de upload visible |
| `processing` | Imagen enviada al backend, IA en proceso. Mostrar spinner |
| `result` | Análisis completado. Mostrar emoción, confianza y recomendación |
| `error` | Fallo en detección. Mostrar mensaje y botón de reintentar |
| `history` | Consultando registros del historial |

> **NUEVO** — Sección necesaria porque la app tiene operaciones asíncronas (cámara, llamada a IA). Sin una gestión explícita de estados, la interfaz puede quedar bloqueada o mostrar datos inconsistentes durante el procesamiento.

---

## 9. Reglas de negocio

- Solo se detecta **una emoción principal** por análisis (la de mayor score de DeepFace).
- **Umbral mínimo de confianza: 50%.** Si ninguna emoción supera ese valor, el sistema rechaza el análisis y muestra: _"No se pudo determinar la emoción con certeza. Intenta en mejor iluminación."_
- Si la imagen contiene **múltiples rostros**, se procesa el de mayor área (rostro más cercano). Si no hay ningún rostro, se retorna un error al usuario.
- La imagen de entrada debe tener un **mínimo de 200×200 px**. Imágenes más pequeñas se rechazan.
- Las recomendaciones son **precargadas en la base de datos** (seed). Se elige una aleatoriamente entre las disponibles para la emoción detectada.
- El historial almacena un **máximo de 100 registros**. Al superarse ese límite, se elimina automáticamente el registro más antiguo (política FIFO).
- Las imágenes capturadas se guardan con **nombre UUID** para evitar colisiones.

> **NUEVO** — El umbral del 50% es crítico: sin él, el sistema mostraría emociones incorrectas con baja certeza. El límite de 100 registros evita que la base de datos local crezca sin control.

---

## 10. Pantallas

### Inicio (`/`)
Presentación del proyecto, descripción breve y botones para iniciar captura o ver historial.

### Captura (`/capture`)
Dos opciones: activar cámara con botón "Tomar foto" o arrastrar/subir imagen. Muestra vista previa de la imagen seleccionada antes de enviar al análisis.

### Análisis — pantalla de carga
Pantalla intermedia con spinner visible mientras el backend procesa la imagen. Se activa automáticamente al enviar la imagen.

### Resultados (`/result/<id>`)
Muestra: emoción detectada con ícono y etiqueta, porcentaje de confianza, barras de scores de las 7 emociones, imagen recomendada y canción recomendada con enlace. Botones: "Nuevo análisis" e "Ir al historial".

### Historial (`/history`)
Lista paginada de análisis anteriores (miniatura, emoción, fecha, botón eliminar). Paginación de 10 registros por página.

### Error (`/error`)
Pantalla genérica de error con mensaje descriptivo y botón de reintentar.

---

## 11. Navegación

```
Inicio → Captura → (procesando) → Resultados
                                       ↓
                              Nueva captura | Historial
Historial → Detalle de resultado anterior
Error (desde cualquier punto) → Reintentar → Captura
```

---

## 12. Persistencia local

- Base de datos SQLite en `database/emosense.db`, gestionada con Flask-SQLAlchemy.
- Imágenes capturadas guardadas en `app/static/captures/` con nombre UUID (ej: `a3f2bc91.jpg`).
- Parámetros configurables en `.env`:

```
CONFIDENCE_THRESHOLD=0.50
MAX_HISTORY=100
UPLOAD_FOLDER=app/static/captures
DEBUG=True
```

- Los pesos del modelo de DeepFace se descargan automáticamente en `ai_models/` en el primer uso (~500 MB).

> **NUEVO** — El archivo `.env` permite cambiar el umbral de confianza o el máximo del historial sin modificar el código fuente.

---

## 13. Criterios de aceptación

- El sistema detecta correctamente al menos 5 de las 7 emociones básicas en condiciones normales de iluminación.
- El tiempo de análisis **no supera los 5 segundos** en hardware convencional (CPU, sin GPU).
- La interfaz responde correctamente en Chrome, Firefox y Edge modernos.
- El historial persiste correctamente entre sesiones.
- El sistema maneja sin bloqueos los errores: imagen sin rostro, imagen corrupta, cámara no disponible, confianza por debajo del umbral.
- Pruebas con al menos **20 imágenes distintas** muestran una precisión de clasificación **≥ 70%**.
- No existe ninguna pantalla que muestre errores HTTP 500 no controlados al usuario.

> **NUEVO** — Los criterios numéricos (70% precisión, 5 segundos) son necesarios para saber objetivamente cuándo el proyecto está terminado.

---

## 14. Instrucciones para la IA

### Configuración recomendada de DeepFace

```python
from deepface import DeepFace
import cv2

img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # CRÍTICO: convertir BGR -> RGB

result = DeepFace.analyze(
    img_path=img_rgb,
    actions=['emotion'],
    detector_backend='opencv',   # Más rápido; usar 'retinaface' para más precisión
    enforce_detection=True        # Lanza excepción si no hay rostro
)

dominant = result[0]['dominant_emotion']    # Emoción con mayor score
all_scores = result[0]['emotion']           # Dict con los 7 scores
confidence = all_scores[dominant] / 100     # Normalizar a 0.0–1.0
```

### Reglas de uso del modelo

- **Siempre convertir BGR → RGB** antes de pasar a DeepFace. OpenCV carga en BGR por defecto; DeepFace espera RGB. Sin esta conversión los resultados son incorrectos.
- Si `enforce_detection=True` lanza una excepción, no hay rostro en la imagen. Capturar esa excepción y retornar un error controlado al usuario.
- Usar `detector_backend='opencv'` para desarrollo (rápido). Para mayor precisión, usar `'retinaface'`.
- Si `confidence < CONFIDENCE_THRESHOLD`, no mostrar el resultado y pedir al usuario que reintente con mejor iluminación o encuadre.
- El primer análisis descarga los pesos automáticamente (~500 MB). Advertir al usuario si es la primera ejecución.

> **NUEVO** — Los errores más comunes en proyectos con DeepFace son omitir la conversión BGR/RGB y no manejar la excepción de rostro no detectado. Documentarlo aquí ahorra horas de debug.

---

## 15. Orden recomendado de implementación

1. Crear entorno virtual, instalar dependencias y verificar que DeepFace funciona con una imagen de prueba en script independiente.
2. Definir modelos SQLAlchemy y ejecutar las migraciones iniciales.
3. Implementar `face_detector.py` y `emotion_analyzer.py`. Probar con imágenes estáticas antes de integrar con Flask.
4. Crear la ruta `/capture` con soporte de upload de imagen. Conectar con los servicios de IA.
5. Implementar la pantalla de resultados `/result/<id>` mostrando emoción y confianza.
6. Poblar la base de datos con recomendaciones iniciales (seed de imágenes y canciones para las 7 emociones).
7. Implementar `recommender.py` y conectarlo con la pantalla de resultados.
8. Implementar el módulo de historial (guardar análisis, listar, eliminar).
9. Agregar captura desde webcam en tiempo real con JavaScript (`getUserMedia` + envío por fetch API).
10. Implementar gestión de errores: estados de carga, mensajes al usuario, pantalla de error.
11. Realizar pruebas con 20+ imágenes, ajustar el umbral de confianza si es necesario.
12. Revisar criterios de aceptación y cerrar el proyecto.
