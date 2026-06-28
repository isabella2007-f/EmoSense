# EmoSense — Especificación de Frontend
> Implementación visual e interactiva sobre el backend ya existente

---

## 0. Contexto y alcance

Este documento complementa `EmoSense_Especificacion_Tecnica.md` (especificación general del proyecto, ya implementada por el backend). **Aquí solo se especifica la capa de frontend**: plantillas Jinja2, CSS y JavaScript dentro de `app/templates/` y `app/static/`.

**No tocar:** `app/models/`, `app/services/`, `app/routes/` salvo que falte una ruta o un campo de contexto que el frontend necesite consumir (en ese caso, señalarlo en vez de modificarlo directamente).

**Restricción de stack:** HTML5 + CSS3 + JavaScript vanilla + Jinja2 + Bootstrap 5. No usar React, Vue, ni ningún framework adicional. No usar frameworks de CSS distintos a Bootstrap 5.

---

## 1. Estructura de archivos a crear

```
app/
├── templates/
│   ├── base.html              # Layout base: navbar, footer, bloques Jinja2
│   ├── index.html             # Pantalla de Inicio (/)
│   ├── capture.html           # Pantalla de Captura (/capture)
│   ├── result.html            # Pantalla de Resultados (/result/<id>)
│   ├── history.html           # Pantalla de Historial (/history)
│   └── error.html             # Pantalla de Error (/error)
├── static/
│   ├── css/
│   │   └── styles.css         # Estilos propios sobre Bootstrap
│   ├── js/
│   │   ├── capture.js         # Lógica de cámara/upload + fetch al backend
│   │   ├── state.js           # Gestión de estados de la UI
│   │   └── history.js         # Paginación y eliminación de historial
│   └── img/
│       ├── emotions/          # Iconos por emoción (happy.svg, sad.svg, etc.)
│       └── memes/             # Memes locales de respaldo (ver sección 6)
```

Todas las plantillas (excepto `base.html`) deben extender `base.html` con `{% extends "base.html" %}` y usar `{% block content %}`.

---

## 2. Layout base (`base.html`)

- Navbar Bootstrap (`navbar navbar-expand-lg`) con: logo/nombre "EmoSense", enlaces a Inicio, Captura, Historial.
- Contenedor principal `<main class="container py-4">{% block content %}{% endblock %}</main>`.
- Footer simple con nombre del proyecto.
- Carga de Bootstrap 5 vía CDN (CSS + JS bundle) en `<head>` y antes de `</body>` respectivamente.
- `<link>` a `static/css/styles.css` y `<script>` a los archivos JS correspondientes por bloque (`{% block scripts %}{% endblock %}`).
- Meta viewport para responsive (`width=device-width, initial-scale=1`).

---

## 3. Mapeo de emociones (usar en todas las pantallas)

Esta tabla debe reflejarse consistentemente en iconos, colores y textos. Usar los campos `label_es` y `color_hex` ya definidos en el modelo `Emotion`; si no hay seed con esos valores, usar esta referencia:

| name (en) | label_es | color_hex sugerido | icono sugerido |
|---|---|---|---|
| happy | Felicidad | `#FFC107` | cara feliz |
| sad | Tristeza | `#2196F3` | cara triste |
| angry | Enojo | `#F44336` | cara enojada |
| fear | Miedo | `#9C27B0` | cara asustada |
| surprise | Sorpresa | `#FF9800` | cara sorprendida |
| disgust | Disgusto | `#4CAF50` | cara con disgusto |
| neutral | Neutralidad | `#9E9E9E` | cara neutral |

El color de cada emoción se usa para: el fondo del badge de emoción detectada, el borde del widget de canción/meme (sección 6), y las barras de progreso de scores.

---

## 4. Pantallas

### 4.1 Inicio (`index.html` → `/`)

- Hero section centrado: título "EmoSense", subtítulo breve (descripción del objetivo principal del documento técnico).
- Dos botones grandes (`btn btn-lg`): "Comenzar análisis" → `/capture`, "Ver historial" → `/history`.
- Opcional: 7 iconos pequeños de las emociones soportadas, en fila, decorativos.

### 4.2 Captura (`capture.html` → `/capture`)

- Dos pestañas o dos columnas (Bootstrap `nav-tabs` o `row`):
  - **Cámara**: `<video>` para preview en vivo, botón "Tomar foto" (activa `getUserMedia`), botón "Capturar" (toma el frame y lo pasa a un `<canvas>` oculto, luego se convierte a base64 con `canvas.toDataURL('image/jpeg')`).
  - **Subir imagen**: input file con drag & drop visual (zona punteada `border-dashed`), acepta solo `.jpg/.jpeg/.png`.
- Una vez hay imagen (de cámara o archivo), mostrar **vista previa** (`<img>`) con botón "Confirmar y analizar" y botón "Cancelar".
- Validación en cliente antes de enviar: tamaño mínimo aproximado (no se puede medir px reales del archivo sin cargarlo, pero si es por cámara se puede forzar resolución del `<video>` ≥ 200×200).
- Al confirmar: estado pasa a `processing` y se hace `fetch(POST)` a `/analyze`:
  - Si la imagen viene de **archivo**: enviar `FormData` con key `file`.
  - Si la imagen viene de **cámara**: enviar JSON `{ "image": "data:image/jpeg;base64,...." }` (el backend ya recorta el prefijo `data:...,` si viene incluido).

### 4.3 Pantalla de carga (estado `processing`, no es ruta propia)

- No es una plantilla aparte: es un overlay o sección que se muestra/oculta vía JS dentro de `capture.html` mientras se espera la respuesta del fetch.
- Spinner Bootstrap (`spinner-border`) + texto "Analizando tu expresión...".
- Bloquear los botones de la pantalla de captura mientras está en este estado (deshabilitar, no ocultar el formulario completo).

### 4.4 Resultados (estado `result`, **no es una ruta propia**)

> **Importante:** el backend no tiene una ruta `/result/<id>`. La respuesta de `POST /analyze` ya incluye todo lo necesario para mostrar el resultado. Por eso "Resultados" es un **estado dentro de `capture.html`** (igual que `processing`), no una plantilla ni ruta separada. La única forma de ver un resultado por URL/ruta propia es desde el Historial, vía `GET /history/<history_id>`.
>
> Para evitar duplicar código, conviene escribir una sola función JS `renderResult(data)` que reciba un objeto normalizado y pinte el bloque de resultados, alimentada por dos fuentes distintas:
> - Respuesta de `POST /analyze`: `{ success, analysis_id, emotion, confidence, all_scores, image_path, recommendation }`
> - Respuesta de `GET /history/<history_id>`: `{ history_id, emotion, confidence, all_scores, image_path, analyzed_at, recommendation }`
>
> Ambas comparten `emotion`, `confidence`, `all_scores`, `image_path` y `recommendation` con el mismo formato, así que `renderResult()` puede ser idéntica para los dos casos.

Estructura en dos columnas (`row`):

**Columna izquierda:**
- Imagen analizada (thumbnail, `src="/static/" + image_path`).
- Badge grande con emoción detectada — el backend manda `emotion` en inglés (ej. `"happy"`); el frontend traduce a `label_es` y aplica `color_hex` usando la tabla de la sección 3 (el backend no manda esos dos campos).
- Porcentaje de confianza grande (el campo `confidence` ya viene listo, ej. `87.5`, solo agregar el símbolo "%").
- 7 barras de progreso (`progress-bar`), una por cada clave de `all_scores` (ya viene en porcentaje, no hay que multiplicar). La emoción dominante resaltada (borde o negrita).

**Columna derecha:**
- **Widget de recomendación emocional** (ver sección 6 — canción + meme en una esquina). Si `recommendation` llega como `null`, mostrar un estado vacío amigable en vez de romper el layout (ver sección 6).

Debajo, centrado: botón "Nuevo análisis" (limpia el estado y vuelve a `capturing` sin recargar la página) y botón "Ir al historial" → `/history`.

### 4.5 Historial (`history.html` → `/history`)

- Al cargar la página, hacer `fetch(GET, '/history?page=1')`. El backend responde `{ items: [...], total, pages, current_page }`. Cada item tiene: `history_id`, `analysis_id`, `emotion`, `confidence`, `image_path`, `analyzed_at`, `recommendation` (puede ser `null`).
- Tabla o grid de tarjetas (`card`), una por registro: miniatura (`/static/` + `image_path`), emoción detectada (badge con color vía la tabla de la sección 3, ya que el backend solo manda `emotion` en inglés), fecha (`analyzed_at`, formatear en JS con `Date` o `toLocaleDateString`), botón "Ver detalle" (abre el resultado usando `history_id` — ver sección 4.4), botón "Eliminar" (ícono de basura).
- Eliminar: `fetch(DELETE, '/history/' + history_id)`. El backend responde `{ success: true }`. Quitar la tarjeta del DOM solo si `success` es `true`. Pedir confirmación con un modal Bootstrap simple antes de eliminar.
- Paginación Bootstrap (`pagination`), usando los campos `total`, `pages` y `current_page` ya devueltos por el backend; al cambiar de página, volver a hacer `fetch` con el nuevo `?page=N` (sin recargar la página completa).
- "Ver detalle" usa `GET /history/<history_id>` para traer `all_scores` y el resto de datos completos, y los pinta con la misma función `renderResult()` de la sección 4.4.

### 4.6 Error (`error.html` → `/error`)

- Mensaje descriptivo (recibido por contexto Jinja2 desde el backend, ej. `{{ error_message }}`).
- Ícono o ilustración simple de error.
- Botón "Reintentar" → `/capture`.
- Esta plantilla también debe poder reutilizarse como **estado** dentro de `capture.html` (sin redirigir) cuando el error ocurre tras un fetch fallido — mostrar el mismo mensaje sin abandonar la pantalla de captura, para no perder el contexto de cámara activa. Confirmar con el backend si los errores llegan como JSON (preferible para este caso) o como redirect a `/error`.

---

## 5. Gestión de estados (`state.js`)

Implementar como un objeto simple de máquina de estados con las 6 fases ya definidas en el documento técnico:

```
idle → capturing → processing → result
                       ↓
                     error → (reintentar) → capturing
history (independiente, accesible desde cualquier punto vía navbar)
```

- Cada estado corresponde a mostrar/ocultar secciones del DOM mediante clases CSS (`d-none` de Bootstrap es suficiente, no usar `display` inline).
- Un solo punto de control: una función `setState(nuevoEstado)` que oculta todo y muestra solo el bloque correspondiente. Evitar lógica de visibilidad repartida en varios lugares del código.

---

## 6. Widget de recomendación emocional (canción + meme en una esquina)

Este es el componente distintivo que pediste agregar:

- **Ubicación:** esquina fija dentro de la columna derecha de la pantalla de Resultados (no flotante sobre toda la página, para no tapar contenido en otras pantallas). Tarjeta (`card`) con borde de color según la emoción detectada (usar `color_hex`).
- **Contenido:**
  - Imagen tipo *meme* relacionada con la emoción (`image_url` del modelo `Recommendation`), mostrada con `object-fit: cover` en un tamaño moderado (ej. 250×250px) para que no domine la pantalla.
  - Debajo: título y artista de la canción (`song_title`, `song_artist`) y un enlace/botón "Escuchar" (`song_url`, `target="_blank"`).
- **Comportamiento:** estos datos llegan ya resueltos en el JSON de `/analyze` o `/history/<history_id>` (el backend ya selecciona aleatoriamente la recomendación según la emoción, según el módulo `recommender.py`). El frontend **no decide** la recomendación, solo la presenta.
- **Si `recommendation` es `null`** (puede pasar si no hay recomendaciones cargadas en la base de datos para esa emoción): no mostrar el widget roto ni vacío — mostrar un mensaje breve tipo "Aún no hay recomendación para esta emoción" dentro de la misma tarjeta, sin imagen ni enlace.
- **Fallback de imagen:** si `recommendation.image_url` no carga (404, vacío, o `null` dentro de un objeto `recommendation` existente), mostrar una imagen de respaldo local desde `static/img/memes/` según la emoción (`{{ emotion }}.jpg`) usando el evento `onerror` de la etiqueta `<img>`, para que la pantalla nunca se vea rota.

---

## 7. Contrato confirmado con el backend

Confirmado directamente leyendo `app/routes/capture.py` y `app/routes/history.py`. **Toda la comunicación es JSON, no hay renderizado por Jinja2 de datos dinámicos** — las plantillas son solo el cascarón estático, el contenido lo llena JavaScript.

### `POST /analyze`

Dos formas de enviar la imagen:

- **Archivo:** `FormData` con key `file` (acepta `.jpg/.jpeg/.png`).
- **Cámara:** JSON con key `image`, valor en base64 (puede incluir el prefijo `data:image/jpeg;base64,` o no, el backend lo recorta).

Respuesta éxito (200):
```json
{
  "success": true,
  "analysis_id": 12,
  "emotion": "happy",
  "confidence": 87.5,
  "all_scores": { "happy": 87.5, "sad": 2.1, "...": "..." },
  "image_path": "captures/a3f2bc91.jpg",
  "recommendation": {
    "image_url": "...",
    "song_title": "...",
    "song_artist": "...",
    "song_url": "..."
  }
}
```
`recommendation` puede ser `null`. `confidence` y `all_scores` ya vienen en **porcentaje** (0–100), no normalizar.

Respuesta error (400 o 422):
```json
{ "success": false, "error": "mensaje legible en español" }
```
El mensaje ya viene listo desde el backend (ej. validación de tamaño, formato no permitido, sin rostro detectado, baja confianza). El frontend solo debe mostrarlo tal cual, no necesita hardcodear sus propios textos de error de negocio.

### `GET /history?page=N`

Respuesta:
```json
{
  "items": [
    {
      "history_id": 5,
      "analysis_id": 12,
      "emotion": "happy",
      "confidence": 87.5,
      "image_path": "captures/a3f2bc91.jpg",
      "analyzed_at": "2026-06-20T14:32:00",
      "recommendation": { "song_title": "...", "song_artist": "...", "song_url": "...", "image_url": "..." }
    }
  ],
  "total": 23,
  "pages": 3,
  "current_page": 1
}
```

### `GET /history/<history_id>`

Igual que un item de arriba, pero además incluye `all_scores` (dict completo).

### `DELETE /history/<history_id>`

Respuesta: `{ "success": true }`.

### Notas para el frontend

- **No existe** `/result/<id>` ni ninguna ruta que renderice HTML con datos. Ver sección 4.4.
- `image_path` se sirve como archivo estático: usar `src="/static/" + image_path` para mostrar las imágenes.
- El backend nunca manda `label_es` ni `color_hex` — el frontend debe mapearlos con la tabla de la sección 3 a partir del campo `emotion` (en inglés).
- **Pendiente de verificar al implementar:** si `recommendation.image_url` es una ruta local (`/static/...`) o una URL externa completa. Si al probarlo la imagen no carga con la ruta tal cual viene, probar agregando el prefijo `/static/` antes de aplicar el fallback de la sección 6.

---

## 8. Manejo de errores en frontend (JavaScript)

- Cámara no disponible (`getUserMedia` rechazada): mostrar mensaje claro y ocultar la opción de cámara, dejando solo la de subir archivo.
- Archivo con extensión no permitida: validar antes de enviar, mostrar alerta Bootstrap (`alert alert-warning`) sin llamar al backend.
- **Errores de negocio del backend** (status 400 o 422 con `{success: false, error: "..."}`): el backend ya manda el mensaje en español listo para mostrar (sin rostro, baja confianza, formato no permitido, imagen muy pequeña). El frontend solo lo despliega en el estado `error`, no debe redefinir esos textos.
- **Fetch fallido por red o backend caído** (sin respuesta JSON válida, timeout, o error de conexión): este caso sí lo controla el frontend con `try/catch`, mostrando un mensaje genérico propio (ej. "No se pudo conectar con el servidor. Intenta de nuevo."). Usar un timeout razonable (ej. 15s) antes de mostrar este error, para no dejar el spinner girando indefinidamente.
- En ambos casos, el estado pasa a `error` dentro de la misma pantalla de captura (no hay redirect a una ruta `/error` separada, ya que todo es JSON — ver sección 4.4), con un botón "Reintentar" que vuelve al estado `capturing`.

---

## 9. Modo cámara en tiempo real (reemplaza el paso 9 original "snapshot único")

> **Cambio de alcance confirmado:** la cámara ya no funciona por snapshot único (tomar una foto y analizarla una vez). Funciona en **modo continuo**: mientras la cámara está activa, se analiza un frame cada cierto intervalo y la pantalla se actualiza sola, sin que el usuario tenga que presionar "Capturar" cada vez.

### 9.1 Mecánica de polling

- Al activar la cámara (`getUserMedia` concedido y `<video>` reproduciendo), iniciar un `setInterval` que dispara un análisis **cada 2 segundos**. No usar un intervalo menor: con `detector_backend='opencv'` cada análisis tarda ~0.5–1s, así que 2s deja margen de sobra sin saturar el backend.
- Cada disparo: capturar el frame actual del `<video>` en un `<canvas>` oculto → `canvas.toDataURL('image/jpeg')` → enviar como JSON `{ "image": "..." }` a `POST /analyze`, igual que el envío de cámara ya documentado en la sección 4.2.
- **Control de solapamiento obligatorio:** mantener una bandera `isAnalyzing` (booleano). Si ya hay una petición en curso, el siguiente tick del intervalo se omite por completo (no se encola, no se acumulan peticiones). Esto evita que, si el backend tarda más de lo esperado en un momento dado, se disparen varias peticiones simultáneas.
- Al detener la cámara (botón "Detener" o el usuario navega fuera de `/capture`), limpiar el intervalo con `clearInterval` y liberar el stream de la cámara (`track.stop()` sobre cada track del `MediaStream`). Sin esto, la cámara queda encendida en segundo plano.

### 9.2 Actualización visual sin parpadeo

- **No usar el estado `processing` de pantalla completa** (spinner que tapa todo, sección 4.3) en modo continuo — eso parpadearía cada 2 segundos y se vería mal. En su lugar, mostrar un indicador pequeño y discreto junto al video (ej. un punto pulsante o texto pequeño "Analizando...") que aparece solo mientras `isAnalyzing` es `true`, sin ocultar nada más.
- El badge de emoción, el porcentaje de confianza y las barras de score sí se actualizan en cada respuesta exitosa, reemplazando los valores anteriores directamente (reutilizar la misma `renderResult()` ya construida, pero sin tocar la imagen analizada — en modo cámara no hace falta mostrar la miniatura de cada frame).
- Si una petición individual falla (ej. el backend devuelve error porque no detectó rostro en ese frame puntual — esto pasará seguido si el usuario se mueve o hay mala luz), **no mostrar la pantalla de error completa**. Simplemente ignorar esa respuesta y seguir con el siguiente intervalo; opcionalmente mostrar un texto discreto como "Buscando rostro..." en vez del badge de emoción mientras no haya una detección válida reciente.
- Solo mostrar el estado de `error` de pantalla completa si fallan **varias peticiones consecutivas seguidas** (ej. 5 seguidas, lo que indicaría un problema real de conexión, no solo un frame sin rostro).

### 9.3 Layout del panel de cámara y recomendación visual

- **Layout revisado** (reemplaza el diseño inicial de dos columnas iguales):
  - El `<video>` ocupa la mayoría del ancho (`col-md-8` o similar) — es el protagonista de la pantalla en modo cámara.
  - A la derecha (`col-md-4`), se muestra **solo la imagen del meme** según la emoción detectada (`recommendation.image_url`, con el mismo fallback local de la sección 6 si no carga). Aquí **no** se muestra título de canción, artista, ni botón "Escuchar" — eso se reemplaza por la reproducción automática (sección 9.5).
  - Debajo del bloque video+meme, en ancho completo: badge de emoción, porcentaje de confianza y las 7 barras de score.
- El meme (igual que antes) solo se reemplaza cuando `data.emotion` cambia respecto a `lastEmotion`, con transición de opacidad — no en cada tick.
- Esta sección 9.3 aplica **solo al modo cámara**. La tarjeta de recomendación completa (imagen + canción + botón "Escuchar") sigue existiendo sin cambios en la pantalla de resultado por archivo (sección 4.4) y en el detalle del historial (sección 4.5) — ahí no hay reproducción automática, solo el link como ya está.

### 9.4 ✅ Punto ya resuelto con el backend — parámetro `save`

Cada llamada a `POST /analyze` (sección 7) guardaba un registro nuevo en el historial por defecto. **Esto ya se resolvió:** `capture.py` ahora acepta un parámetro opcional `save` en el body JSON (`{"image": "...", "save": false}`). Si se omite o es `true`, el comportamiento es igual que antes (guarda en `FacialAnalysis`/`AnalysisHistory`). Si es `false`, analiza y devuelve el resultado normal, pero no escribe nada en la base de datos — `analysis_id` e `image_path` llegan como `null` en ese caso.

**En modo cámara, cada tick del intervalo debe mandar siempre `save: false`**, para que la cámara en vivo nunca llene el historial. El `renderResult()`/`updateCameraResult()` debe manejar `image_path: null` sin romperse (no intentar poner `src` en la miniatura cuando es `null`).

### 9.5 Reproducción automática de audio (solo en modo cámara)

> **Cambio de enfoque:** el audio en modo cámara ya **no** viene de `recommendation.song_url` (que tiene 2-3 opciones aleatorias por emoción, pensadas para la tarjeta de recomendación normal de las secciones 4.4/4.5). En modo cámara se usa un **único audio fijo por emoción** (frases tipo "hopecore"), desacoplado por completo de la recomendación del backend — es una tabla nueva que vive solo en el frontend, no requiere tocar `seed.py` ni el backend.

**Tabla de audio por emoción** (agregar junto a `EMOTION_MAP` en `state.js`, o como tabla separada):

```js
const EMOTION_AUDIO = {
  happy:    '/static/audio/happy.mp3',
  sad:      '/static/audio/sad.mp3',
  angry:    '/static/audio/angry.mp3',
  fear:     '/static/audio/fear.mp3',
  surprise: '/static/audio/surprise.mp3',
  disgust:  '/static/audio/disgust.mp3',
  neutral:  '/static/audio/neutral.mp3',
};
```

(Ajustar las rutas/nombres exactos a los archivos que ya están en `app/static/audio/` — un solo archivo por emoción, sin aleatoriedad.)

**Cómo implementarlo:**

1. Un único elemento `<audio id="camera-audio">` oculto (sin `controls`) dentro del panel de cámara.
2. **Cada vez que cambia la emoción dominante** (mismo trigger que el meme — comparar `data.emotion` contra `lastEmotion`): tomar el archivo de `EMOTION_AUDIO[data.emotion]` y hacer:
   ```js
   audioEl.src = EMOTION_AUDIO[data.emotion];
   audioEl.play().catch(() => {});
   ```
3. El **meme sigue viniendo de `recommendation.image_url`** (eso no cambia) — solo el audio se desacopló de la recomendación del backend.
4. Si por alguna razón `EMOTION_AUDIO[data.emotion]` no existe (no debería pasar si las 7 emociones tienen su archivo), no reproducir nada y no romper la pantalla.
5. **Al detener la cámara**: `audioEl.pause(); audioEl.currentTime = 0;`.
6. Botón de silenciar/activar: igual que antes, solo alterna `audioEl.muted`.

**Ya no aplica:** todo lo que dependía de `recommendation.song_url` para el audio en modo cámara (la lógica de `playForEmotion(rec)` que leía `rec.song_url` se reemplaza por una que lee directamente `EMOTION_AUDIO[data.emotion]`, sin pasar por `recommendation` en absoluto).

---

## 10. Criterios de aceptación del frontend

- Las 6 pantallas/estados funcionan sin recargar la página de forma inesperada (SPA-like dentro de `/capture` para los estados `capturing/processing/error`; navegación normal entre rutas para el resto).
- La interfaz es responsive y se ve correctamente en móvil y escritorio (usar las clases de grilla de Bootstrap, no medidas fijas en px salvo para imágenes pequeñas).
- Ningún estado deja botones activos que generen una doble petición (deshabilitar botones durante `processing`).
- El widget de canción/meme siempre muestra algo (nunca un espacio roto o vacío), gracias al fallback de la sección 6.
- Los colores de emoción son consistentes entre la pantalla de Resultados y la de Historial.
- No se usa ningún framework de JS además de vanilla; no se usa ningún framework CSS además de Bootstrap 5.

---

## 11. Orden recomendado de implementación

1. `base.html` con navbar y carga de Bootstrap, sin contenido todavía.
2. `index.html` (la más simple, sirve para validar que el layout base funciona).
3. `capture.html` con upload de archivo (sin cámara todavía) + `state.js` básico (`idle`/`capturing`/`processing`).
4. Conectar el fetch real al endpoint de captura, confirmando contrato con el backend (sección 7).
5. `result.html` con los datos de la emoción y scores, sin el widget de canción/meme todavía.
6. Agregar el widget de canción/meme (sección 6) con su fallback.
7. `history.html` con paginación y eliminación AJAX.
8. `error.html` + manejo de errores embebido en `capture.html` (sección 8).
9. Agregar cámara en **modo continuo** (sección 9) — **antes de empezar este paso, resolver primero el punto 9.4 con tu compañera** (parámetro `save` o equivalente en el backend), o el historial se va a llenar de registros basura apenas se pruebe.
10. Pulir estilos en `styles.css`, revisar responsive y colores por emoción en todas las pantallas.
