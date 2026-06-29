'use strict';

// Audio fijo por emoción para modo cámara — desacoplado de recommendation
const EMOTION_AUDIO = {
  happy:   '/static/audio/happy.mp3',
  sad:     '/static/audio/sad.mp3',
  angry:   '/static/audio/angry.mp3',
  fear:    '/static/audio/fear.mp3',
  disgust:  '/static/audio/disgust.mp3',
  neutral:  '/static/audio/neutral.mp3',
  surprise: '/static/audio/surprise.mp3',
};

// Mapeo canónico de emociones — usado en todas las pantallas
const EMOTION_MAP = {
  happy:    { label: 'Felicidad',   color: '#FFC107', icon: 'bi-emoji-laughing-fill' },
  sad:      { label: 'Tristeza',    color: '#2196F3', icon: 'bi-emoji-frown-fill' },
  angry:    { label: 'Enojo',       color: '#F44336', icon: 'bi-emoji-angry-fill' },
  fear:     { label: 'Miedo',       color: '#9C27B0', icon: 'bi-emoji-dizzy-fill' },
  surprise: { label: 'Sorpresa',    color: '#FF9800', icon: 'bi-emoji-surprise-fill' },
  disgust:  { label: 'Disgusto',    color: '#4CAF50', icon: 'bi-emoji-expressionless-fill' },
  neutral:  { label: 'Neutralidad', color: '#9E9E9E', icon: 'bi-emoji-neutral-fill' },
};

// Único punto de control de visibilidad para los estados de capture.html
function setState(newState) {
  ['capturing', 'processing', 'result', 'error'].forEach(function (s) {
    const el = document.getElementById('section-' + s);
    if (el) el.classList.toggle('d-none', s !== newState);
  });
}

// ── renderRecCard ─────────────────────────────────────────────────────────────
// Rellena una tarjeta de recomendación dado su elemento contenedor.
// Usada por renderResult (upload/history) y por el modo cámara en capture.js.
// Usa querySelector relativo al contenedor, no getElementById, para soportar
// múltiples tarjetas en el mismo DOM sin conflicto de IDs.
function renderRecCard(cardEl, emotion, rec) {
  const meta = EMOTION_MAP[emotion] || { color: '#9E9E9E' };
  cardEl.style.borderColor = meta.color;

  if (!rec) {
    cardEl.innerHTML = `
      <div class="card-body d-flex flex-column align-items-center justify-content-center
                  text-center text-secondary py-5">
        <i class="bi bi-music-note-beamed fs-1 mb-3"></i>
        <p class="mb-0">Aún no hay recomendación para esta emoción.</p>
      </div>`;
    return;
  }

  const fallback = `/static/img/memes/${emotion}.jpg`;
  cardEl.innerHTML = `
    <div class="card-body p-3 d-flex flex-column">
      <p class="small text-secondary text-uppercase mb-2">
        <i class="bi bi-stars me-1"></i>Recomendación para ti
      </p>
      <img class="rec-img w-100 rounded-2 mb-3" alt=""
           style="height:200px;object-fit:cover;">
      <p class="small text-secondary mb-1">
        <i class="bi bi-music-note-beamed me-1"></i>Canción
      </p>
      <p class="rec-title fw-semibold text-white mb-0"></p>
      <p class="rec-artist text-secondary small mb-3"></p>
      <a class="rec-link btn btn-sm btn-outline-warning mt-auto d-none"
         href="#" target="_blank" rel="noopener noreferrer">
        <i class="bi bi-box-arrow-up-right me-1"></i>Escuchar
      </a>
    </div>`;

  cardEl.querySelector('.rec-title').textContent  = rec.song_title  || '';
  cardEl.querySelector('.rec-artist').textContent = rec.song_artist || '';

  const recImg = cardEl.querySelector('.rec-img');
  recImg.src     = rec.image_url || fallback;
  recImg.onerror = function () { this.onerror = null; this.src = fallback; };

  if (rec.song_url) {
    const link = cardEl.querySelector('.rec-link');
    link.href = rec.song_url;
    link.classList.remove('d-none');
  }
}

// ── renderResult ─────────────────────────────────────────────────────────────
// Compartida entre capture.html (POST /analyze) e history.html (GET /history/<id>).
// Pobla los elementos con IDs result-* que deben existir en el DOM de la página.
function renderResult(data) {
  const emotion = (data.emotion || '').toLowerCase();
  const meta = EMOTION_MAP[emotion] || { label: data.emotion, color: '#9E9E9E', icon: 'bi-emoji-neutral-fill' };

  // image_path es null cuando save:false (modo cámara) — no tocar el elemento
  if (data.image_path) {
    document.getElementById('result-img').src = '/static/' + data.image_path;
  }

  const badge = document.getElementById('result-badge');
  badge.style.backgroundColor = meta.color;
  document.getElementById('result-icon').className    = 'bi ' + meta.icon;
  document.getElementById('result-label').textContent = meta.label;
  document.getElementById('result-confidence').textContent = data.confidence != null ? String(data.confidence) : '—';

  // Barras ordenadas de mayor a menor; la dominante resaltada
  const scoresEl = document.getElementById('result-scores');
  const sorted   = Object.entries(data.all_scores || {}).sort((a, b) => b[1] - a[1]);
  scoresEl.innerHTML = sorted.map(([key, value]) => {
    const m        = EMOTION_MAP[key] || { label: key, color: '#9E9E9E' };
    const dominant = key === emotion;
    return `
      <div class="mb-2">
        <div class="d-flex justify-content-between small mb-1">
          <span class="${dominant ? 'fw-bold text-white' : 'text-secondary'}">${m.label}</span>
          <span class="${dominant ? 'fw-bold text-white' : 'text-secondary'}">${value}%</span>
        </div>
        <div class="progress" style="height:${dominant ? 8 : 5}px;">
          <div class="progress-bar" role="progressbar"
               style="width:${value}%;background-color:${m.color};"
               aria-valuenow="${value}" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
      </div>`;
  }).join('');

  renderRecCard(document.getElementById('result-rec-card'), emotion, data.recommendation);
}
