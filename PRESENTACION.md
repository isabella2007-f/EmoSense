# EmoSense — Guía completa para la presentación

---

## ¿Qué es EmoSense?

EmoSense es una aplicación web que usa inteligencia artificial para detectar cómo te sientes mirándote la cara, y luego te recomienda una canción y un meme acorde a tu emoción.

**Frase para la presentación:**
> "EmoSense es una aplicación que usa cámaras e inteligencia artificial para analizar tu expresión facial y recomendarte música según cómo te sientes en ese momento."

---

## ¿Cómo funciona? (explicado simple)

Imagina que la app es como un espejo inteligente:

1. **Tú le muestras tu cara** — subes una foto, tomas un snapshot, o abres la cámara en vivo
2. **La IA la estudia** — analiza los músculos de tu cara: si sonríes, si frunces el ceño, si tus ojos están abiertos de par en par
3. **La IA decide** — dice algo como "esta cara está 87% feliz"
4. **La app recomienda** — busca en su lista y te da una canción + un meme para esa emoción

---

## Las 7 emociones que detecta

| Inglés | Español | Color |
|--------|---------|-------|
| happy | Felicidad | Amarillo |
| sad | Tristeza | Azul |
| angry | Enojo | Rojo |
| fear | Miedo | Morado |
| surprise | Sorpresa | Naranja |
| disgust | Disgusto | Verde |
| neutral | Neutral | Gris |

---

## Qué decir en la presentación (diapositiva por diapositiva)

### Slide 1 — Portada
> "Hoy les voy a presentar EmoSense, una aplicación web que detecta emociones faciales usando inteligencia artificial y recomienda música según cómo te sientes."

### Slide 2 — El problema / motivación
> "¿Cuántas veces has entrado a Spotify sin saber qué escuchar porque no sabías cómo te sentías? EmoSense automatiza eso: solo te miras a la cámara y la app detecta tu estado emocional."

### Slide 3 — ¿Qué hace la app?
> "La app tiene tres modos: puedes subir una foto, tomar un snapshot con la cámara, o dejar la cámara activa para análisis continuo. Detecta tu emoción, te muestra el resultado con un porcentaje de confianza, y te recomienda una canción y un meme."

### Slide 4 — La IA (cómo funciona la magia)
> "Usamos una librería llamada DeepFace, que es básicamente un cerebro de inteligencia artificial ya entrenado. Alguien entrenó esta IA con millones de fotos de caras con diferentes emociones durante meses. Nosotros simplemente la usamos: le damos una foto y nos dice qué emoción ve. Es como tener un detector de mentiras, pero para emociones."

> "DeepFace usa un modelo llamado RetinaFace para encontrar el rostro en la imagen, y luego analiza las expresiones musculares del rostro."

### Slide 5 — Tecnologías usadas
> "El proyecto usa:
> - **Python** como lenguaje principal
> - **Flask** para el servidor web (el que responde cuando el navegador pide algo)
> - **DeepFace** para la inteligencia artificial de emociones
> - **OpenCV** para procesar las imágenes antes de dárselas a la IA
> - **SQLite** como base de datos para guardar el historial
> - **Bootstrap** para que la interfaz se vea bien
> - **JavaScript** para la cámara en tiempo real en el navegador"

### Slide 6 — La base de datos
> "Tenemos una base de datos con tres tipos de información: las 7 emociones con sus colores, las recomendaciones de canciones y memes (3 por emoción, para que no sea siempre la misma), y el historial de todos los análisis hechos."

### Slide 7 — El historial
> "Cada vez que analizas una foto, se guarda en la base de datos: qué emoción se detectó, con qué porcentaje de confianza, cuándo fue, y qué canción se recomendó. Hay un límite de 100 análisis para no llenar el almacenamiento."

### Slide 8 — Modos de captura
> "Implementamos tres modos de captura:
> - Subir imagen: el usuario sube un archivo JPG o PNG
> - Snapshot: abre la cámara, tomas la foto, la cámara se cierra automáticamente, y luego se analiza
> - Cámara en vivo: analiza cada 2 segundos automáticamente mientras está activa"

### Slide 9 — Modo oscuro / claro
> "La app tiene modo oscuro y modo claro. Se activa con el botón del ojo en la barra de navegación. La preferencia se guarda localmente en el navegador, así que si cierras y vuelves a abrir, recuerda tu elección."

### Slide 10 — Demo
> "Ahora les muestro cómo funciona en vivo." [Abres la app, pones la cámara o subes una foto, muestras el resultado]

---

## Cómo funciona cada archivo (de cabeza a pies)

### El flujo completo cuando analizas una foto:

```
TÚ abres la cámara o subes una foto
        ↓
[Navegador / JavaScript]
  capture.js captura el frame y lo convierte a base64
        ↓
[Servidor / Python - capture.py]
  Recibe la imagen base64 o el archivo
  OpenCV la decodifica (base64 → array de números)
  Convierte BGR → RGB (crítico para la IA)
  Valida que sea al menos 200x200 píxeles
        ↓
[IA / Python - emotion_analyzer.py]
  DeepFace.analyze() detecta el rostro
  Analiza los músculos faciales
  Devuelve: happy=87%, sad=3%, angry=2%...
        ↓
[Base de datos / Python - recommender.py]
  Busca recomendaciones para 'happy' en SQLite
  Elige una de las 3 opciones al azar
        ↓
[Base de datos / Python - capture.py]
  Guarda la foto en disco (captures/)
  Guarda el análisis en la tabla facial_analyses
  Guarda el historial en la tabla analysis_history
        ↓
[Respuesta JSON al navegador]
  emotion: 'happy', confidence: 87.3, meme, canción
        ↓
[Navegador / JavaScript - state.js]
  Muestra el resultado en pantalla con colores y el meme
```

---

## Cada archivo y para qué sirve

### Archivos de configuración y arranque

**`run.py`** — El interruptor de luz
- Es el archivo que arrancas para iniciar la app
- Solo hace una cosa: crear la app y encenderla
- Cuando corres `python run.py`, el servidor empieza a escuchar

**`app/__init__.py`** — El ensamblador
- Construye la aplicación Flask completa
- Conecta todos los módulos: base de datos, rutas, configuración
- Sin este archivo, nada funcionaría junto

**`app/config.py`** — El tablero de control
- Guarda todas las configuraciones: dónde está la BD, cuánto historial guardar, etc.
- Lee variables de entorno (del archivo `.env`) para que no tengas contraseñas en el código

**`seed.py`** — El que pone los datos iniciales
- Se ejecuta una sola vez al instalar la app
- Inserta las 7 emociones y las 21 recomendaciones en la base de datos
- Sin esto, la app no tendría canciones ni memes que recomendar

### Modelos (la estructura de la base de datos)

**`app/models/emotion.py`** — Define la tabla `emotions`
- 7 filas, una por emoción
- Guarda: nombre en inglés, nombre en español, color hex

**`app/models/recommendation.py`** — Define la tabla `recommendations`
- 21 filas (3 por emoción)
- Guarda: qué emoción le corresponde, URL del meme, título de la canción, artista, link de YouTube

**`app/models/history.py`** — Define las tablas del historial
- `facial_analyses`: cada análisis hecho (foto, emoción, confianza, fecha)
- `analysis_history`: une cada análisis con su recomendación

### Servicios (la lógica)

**`app/services/face_detector.py`** — El validador
- Verifica que la imagen sea grande suficiente (mínimo 200x200 píxeles)
- Tiene también una función de respaldo para detectar rostros con OpenCV

**`app/services/emotion_analyzer.py`** — El cerebro de la IA ⭐
- Aquí vive DeepFace
- Recibe la imagen y devuelve los porcentajes de las 7 emociones
- Si la confianza es menor al 50%, rechaza el resultado
- Es el archivo más importante del proyecto

**`app/services/recommender.py`** — El que recomienda
- Busca en la base de datos las 3 recomendaciones de la emoción detectada
- Elige una al azar
- Así cada vez puede salir una canción o meme diferente

### Rutas (lo que responde el servidor)

**`app/routes/main.py`** — Las páginas HTML
- `/` → página de inicio
- `/capture` → página de captura
- `/history/page` → página del historial

**`app/routes/capture.py`** — El endpoint de análisis ⭐
- Recibe la imagen del navegador
- Coordina todo el proceso: validar → analizar → recomendar → guardar → responder
- Es el "director de orquesta" del análisis

**`app/routes/history.py`** — La API del historial
- `GET /history` → lista paginada del historial
- `GET /history/<id>` → detalle de un análisis específico
- `DELETE /history/<id>` → elimina un análisis del historial

### Interfaz (lo que ve el usuario)

**`app/templates/base.html`** — La plantilla base
- El navbar siempre presente con el logo y los links
- El botón del ojo para cambiar entre modo claro/oscuro
- Todo el resto de las páginas "hereda" de esta

**`app/templates/capture.html`** — La página de captura
- Las 3 pestañas: subir imagen, snapshot, cámara en vivo
- Las secciones: capturando → procesando → resultado → error

**`app/static/js/capture.js`** — La cámara en el navegador
- Maneja la cámara del dispositivo con `getUserMedia`
- Para snapshot: abre cámara → captura un frame → cierra cámara → envía al servidor
- Para cámara en vivo: envía un frame al servidor cada 2 segundos automáticamente

**`app/static/js/state.js`** — El que dibuja los resultados
- Tiene los colores e iconos de cada emoción
- `renderResult()`: muestra la emoción, confianza y barra de progreso
- `renderRecCard()`: muestra el meme y la canción recomendada

**`app/static/css/styles.css`** — Los estilos visuales
- Personaliza colores y espaciados
- Define cómo se ve en modo claro vs oscuro

---

## Cómo funciona la IA (para explicar sin tecnicismos)

Cuando le das una foto a DeepFace, internamente hace esto:

1. **Encuentra la cara**: Busca un óvalo en la imagen que tenga ojos, nariz y boca
2. **Recorta la cara**: Se queda solo con esa parte de la imagen
3. **La convierte a números**: Cada píxel se convierte en números (rojo, verde, azul de 0 a 255)
4. **Pasa los números por la red neuronal**: Una red neuronal es como miles de capas de matemáticas que transforman esos números
5. **Sale un resultado**: Al final de todas esas capas matemáticas, sale un porcentaje para cada emoción

La red neuronal fue entrenada así: alguien reunió millones de fotos de personas haciendo cada expresión, las etiquetó ("esta foto es happy", "esta es sad"), y dejó que el sistema de IA ajustara sus matemáticas internas hasta que aprendió a distinguirlas. Ese entrenamiento duró semanas en computadoras muy potentes. Nosotros simplemente descargamos ese resultado (los modelos, ~500 MB) y lo usamos.

---

## Posibles preguntas y respuestas

**¿Por qué a veces no detecta bien la emoción?**
> "La IA fue entrenada principalmente con fotos de alta calidad bien iluminadas. Si la iluminación es mala, si la cara está tapada, o si la expresión es muy sutil, la confianza baja del 50% y la app rechaza el resultado para no dar información incorrecta."

**¿Los datos se guardan en la nube?**
> "No, todo se guarda localmente. La base de datos es un archivo SQLite en la misma computadora donde corre la app. No mandamos imágenes a ningún servidor externo."

**¿Puede detectar varias caras?**
> "Sí, DeepFace puede detectar múltiples rostros en una imagen. En ese caso, la app analiza todos y se queda con el que tenga mayor confianza en su emoción dominante."

**¿Qué pasa si hay 100 análisis guardados?**
> "La app tiene un sistema FIFO (primero en entrar, primero en salir): cuando se llega a 100 registros, el más antiguo se elimina automáticamente al agregar uno nuevo."

**¿Por qué usaron Flask y no otra cosa?**
> "Flask es un framework de Python ligero, fácil de aprender y perfecto para proyectos de este tamaño. Python también era necesario porque DeepFace solo funciona en Python."

---

## Resumen de lo que debes decir (versión corta)

1. **¿Qué es?** → App que detecta emociones con la cámara y recomienda música
2. **¿Cómo funciona?** → IA (DeepFace) analiza tu cara → detecta emoción → busca canción en BD → muestra resultado
3. **¿Qué tecnologías?** → Python, Flask, DeepFace, OpenCV, SQLite, JavaScript, Bootstrap
4. **¿Cómo está organizado?** → Modelos (BD), Servicios (lógica), Rutas (API), Templates (HTML), JavaScript (cámara)
5. **Lo más difícil** → Hacer que la cámara en tiempo real funcione + conversión BGR→RGB para la IA
6. **Demo en vivo** → Mostrar los 3 modos de captura + historial + modo claro/oscuro
