'use strict';

(function () {

  // ════════════════════════════════════════════════════════════════
  // MODO UPLOAD — subir imagen desde disco
  // ════════════════════════════════════════════════════════════════

  const fileInput   = document.getElementById('file-input');
  const dropZone    = document.getElementById('drop-zone');
  const previewArea = document.getElementById('preview-area');
  const previewImg  = document.getElementById('preview-img');
  const btnConfirm  = document.getElementById('btn-confirm');
  const btnCancel   = document.getElementById('btn-cancel');
  const btnRetry    = document.getElementById('btn-retry');
  const errorMsg    = document.getElementById('error-message');

  let selectedFile = null;

  // ── Drop zone ──────────────────────────────────────────────────
  dropZone.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) loadFile(fileInput.files[0]);
  });

  dropZone.addEventListener('dragover', e => {
    e.preventDefault();
    dropZone.classList.add('drop-zone--active');
  });
  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drop-zone--active');
  });
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('drop-zone--active');
    if (e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
  });

  function loadFile(file) {
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      showInlineAlert('Solo se permiten archivos JPG o PNG.');
      return;
    }
    selectedFile   = file;
    previewImg.src = URL.createObjectURL(file);
    dropZone.classList.add('d-none');
    previewArea.classList.remove('d-none');
  }

  // ── Cancelar / reintentar / nuevo análisis ─────────────────────
  btnCancel.addEventListener('click', resetCapture);
  btnRetry.addEventListener('click', resetCapture);
  document.getElementById('btn-new-analysis').addEventListener('click', resetCapture);

  function resetCapture() {
    selectedFile    = null;
    fileInput.value = '';
    if (previewImg.src.startsWith('blob:')) URL.revokeObjectURL(previewImg.src);
    previewImg.src = '';
    previewArea.classList.add('d-none');
    dropZone.classList.remove('d-none');
    setState('capturing');
  }

  // ── Confirmar y analizar ───────────────────────────────────────
  btnConfirm.addEventListener('click', () => {
    if (!selectedFile) return;
    submitImage();
  });

  async function submitImage() {
    btnConfirm.disabled = true;
    btnCancel.disabled  = true;
    setState('processing');

    const formData = new FormData();
    formData.append('file', selectedFile);

    const controller = new AbortController();
    const tid = setTimeout(() => controller.abort(), 20000);

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      });
      clearTimeout(tid);
      const data = await response.json();

      if (data.success) {
        renderResult(data);       // definida en state.js
        setState('result');
      } else {
        showError(data.error);
      }
    } catch (err) {
      clearTimeout(tid);
      showError(
        err.name === 'AbortError'
          ? 'La solicitud tardó demasiado. Intenta de nuevo.'
          : 'No se pudo conectar con el servidor. Intenta de nuevo.'
      );
    } finally {
      btnConfirm.disabled = false;
      btnCancel.disabled  = false;
    }
  }

  // ── Helpers upload ─────────────────────────────────────────────
  function showError(message) {
    errorMsg.textContent = message;
    setState('error');
  }

  function showInlineAlert(message) {
    const existing = document.getElementById('capture-alert');
    if (existing) existing.remove();
    const el = document.createElement('div');
    el.id        = 'capture-alert';
    el.className = 'alert alert-warning alert-dismissible fade show mt-2';
    el.innerHTML = `${message}<button type="button" class="btn-close"
                    data-bs-dismiss="alert" aria-label="Cerrar"></button>`;
    dropZone.insertAdjacentElement('afterend', el);
  }


  // ════════════════════════════════════════════════════════════════
  // MODO CÁMARA — análisis continuo en tiempo real
  // ════════════════════════════════════════════════════════════════

  const tabCameraBtn   = document.getElementById('tab-camera-btn');
  const camStart       = document.getElementById('cam-start');
  const camActive      = document.getElementById('cam-active');
  const camUnavailable = document.getElementById('cam-unavailable');
  const camVideo       = document.getElementById('cam-video');
  const camIndicator   = document.getElementById('cam-indicator');
  const camWaiting     = document.getElementById('cam-waiting');
  const camResult      = document.getElementById('cam-result');
  const camBadge       = document.getElementById('cam-badge');
  const camIcon        = document.getElementById('cam-icon');
  const camLabel       = document.getElementById('cam-label');
  const camConfidence  = document.getElementById('cam-confidence');
  const camScores      = document.getElementById('cam-scores');
  const camMeme        = document.getElementById('cam-meme');
  const camMemeImg     = document.getElementById('cam-meme-img');
  const camStatus      = document.getElementById('cam-status');
  const btnStartCamera = document.getElementById('btn-start-camera');
  const btnStopCamera  = document.getElementById('btn-stop-camera');
  const btnMute        = document.getElementById('btn-mute-camera');

  const CAMERA_INTERVAL_MS    = 2000;
  const MAX_CONSECUTIVE_FAILS = 5;

  let cameraStream     = null;
  let cameraInterval   = null;
  let isAnalyzing      = false;
  let consecutiveFails = 0;
  let lastEmotion      = null;

  // ── Audio de cámara ────────────────────────────────────────────
  const audioEl = document.getElementById('camera-audio');
  let isMuted   = false;

  btnStartCamera.addEventListener('click', startCamera);
  btnStopCamera.addEventListener('click', stopCamera);

  // Detener la cámara al cambiar a otra pestaña
  tabCameraBtn.addEventListener('hide.bs.tab', stopCamera);
  // Detener la cámara al abandonar la página
  window.addEventListener('pagehide', stopCamera);

  // ── Iniciar cámara ─────────────────────────────────────────────
  async function startCamera() {
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    } catch {
      camStart.classList.add('d-none');
      camUnavailable.classList.remove('d-none');
      return;
    }

    camVideo.srcObject = cameraStream;
    camStart.classList.add('d-none');
    camActive.classList.remove('d-none');

    consecutiveFails = 0;
    lastEmotion      = null;

    // Esperar a que el video tenga frames antes de empezar el polling
    camVideo.addEventListener('loadeddata', function onReady() {
      camVideo.removeEventListener('loadeddata', onReady);
      cameraTick();
      cameraInterval = setInterval(cameraTick, CAMERA_INTERVAL_MS);
    });
  }

  // ── Detener cámara ─────────────────────────────────────────────
  function stopCamera() {
    clearInterval(cameraInterval);
    cameraInterval = null;
    audioEl.pause();
    audioEl.currentTime = 0;
    // isAnalyzing NO se resetea aquí: el tick en vuelo (si lo hay) lo
    // reseteará él mismo en su finally. Resetear aquí permitiría que el
    // siguiente setInterval arrancase concurrente con ese tick fantasma.

    if (cameraStream) {
      cameraStream.getTracks().forEach(t => t.stop());
      cameraStream = null;  // los ticks en vuelo verán !cameraStream y abortarán su resultado
    }
    if (camVideo) camVideo.srcObject = null;

    // Restablecer UI del tab de cámara al estado inicial
    if (camActive)      camActive.classList.add('d-none');
    if (camUnavailable) camUnavailable.classList.add('d-none');
    if (camStart)       camStart.classList.remove('d-none');
    if (camWaiting) {
      camWaiting.classList.remove('d-none');
      // Restaurar el mensaje original por si fue reemplazado
      camWaiting.querySelector('p').textContent = 'Apunta tu rostro a la cámara…';
    }
    if (camMeme)    camMeme.classList.add('d-none');
    if (camResult)  camResult.classList.add('d-none');
    if (camStatus)  camStatus.textContent = '';

    lastEmotion      = null;
    consecutiveFails = 0;
  }

  // ── Tick de análisis (cada 2 s) ────────────────────────────────
  async function cameraTick() {
    if (isAnalyzing || !cameraStream) return;
    if (!camVideo || camVideo.readyState < 2) return;

    isAnalyzing = true;
    camIndicator.classList.remove('d-none');

    try {
      // Capturar frame a máx. 640 px de ancho para reducir payload
      const srcW  = camVideo.videoWidth  || 640;
      const srcH  = camVideo.videoHeight || 480;
      const scale = Math.min(1, 640 / srcW);
      const canvas = document.createElement('canvas');
      canvas.width  = Math.round(srcW * scale);
      canvas.height = Math.round(srcH * scale);
      canvas.getContext('2d').drawImage(camVideo, 0, 0, canvas.width, canvas.height);
      const base64 = canvas.toDataURL('image/jpeg', 0.8);

      const response = await fetch('/analyze', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ image: base64, save: false }),
      });
      const data = await response.json();

      if (data.success && cameraStream) {   // cameraStream=null si la cámara fue detenida
        consecutiveFails      = 0;
        camStatus.textContent = '';
        updateCameraResult(data);
      } else if (!cameraStream) {
        // tick fantasma de una sesión anterior — descartarlo silenciosamente
      } else {
        // Error de negocio por frame (sin rostro, baja confianza…) — no es fatal
        consecutiveFails++;
        camStatus.textContent = 'Buscando rostro…';
        if (consecutiveFails >= MAX_CONSECUTIVE_FAILS) {
          stopCamera();
          showError(data.error || 'No se detectó un rostro de forma continua. Intenta de nuevo.');
        }
      }
    } catch {
      consecutiveFails++;
      if (consecutiveFails >= MAX_CONSECUTIVE_FAILS) {
        stopCamera();
        showError('No se pudo conectar con el servidor. Intenta de nuevo.');
      }
    } finally {
      isAnalyzing = false;
      camIndicator.classList.add('d-none');
    }
  }

  // ── Actualizar resultados en vivo ──────────────────────────────
  function updateCameraResult(data) {
    const emotion = (data.emotion || '').toLowerCase();
    const meta    = EMOTION_MAP[emotion] ||
                    { label: data.emotion, color: '#9E9E9E', icon: 'bi-emoji-neutral-fill' };

    // Badge + confianza
    camBadge.style.backgroundColor = meta.color;
    camIcon.className               = 'bi ' + meta.icon;
    camLabel.textContent            = meta.label;
    // String() explícito: textContent=null daría "" vacío (DOM spec), no "null"
    camConfidence.textContent       = data.confidence != null ? String(data.confidence) : '—';

    // Barras de scores (se actualizan en cada tick)
    const sorted = Object.entries(data.all_scores || {}).sort((a, b) => b[1] - a[1]);
    camScores.innerHTML = sorted.map(([key, value]) => {
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

    // Meme + música: solo actualiza cuando cambia la emoción dominante
    if (emotion !== lastEmotion) {
      const isFirst = (lastEmotion === null);
      lastEmotion   = emotion;

      const fallback = `/static/img/memes/${emotion}.jpg`;
      const src = (data.recommendation && data.recommendation.image_url)
                  ? data.recommendation.image_url
                  : fallback;

      if (isFirst) {
        camMemeImg.src     = src;
        camMemeImg.onerror = function () { this.onerror = null; this.src = fallback; };
        camWaiting.classList.add('d-none');
        camMeme.classList.remove('d-none');
      } else {
        camMemeImg.style.transition = 'opacity 0.3s';
        camMemeImg.style.opacity    = '0';
        setTimeout(() => {
          camMemeImg.src     = src;
          camMemeImg.onerror = function () { this.onerror = null; this.src = fallback; };
          camMemeImg.style.opacity = '1';
        }, 300);
      }

      playForEmotion(emotion);
    }

    // Badge + confianza + barras: visibles desde la primera detección
    camResult.classList.remove('d-none');
  }

  // ── Helpers de reproducción ────────────────────────────────────
  function playForEmotion(emotion) {
    const src = EMOTION_AUDIO[emotion];  // definido en state.js
    if (!src) return;                    // emoción sin audio (ej. surprise) — silencio
    audioEl.src    = src;
    audioEl.muted  = isMuted;
    audioEl.play().catch(function () {}); // silenciar rechazo de autoplay — no rompe la UI
  }

  function updateMuteButton() {
    if (isMuted) {
      btnMute.innerHTML = '<i class="bi bi-volume-mute-fill me-1"></i>Activar sonido';
    } else {
      btnMute.innerHTML = '<i class="bi bi-volume-up-fill me-1"></i>Silenciar';
    }
  }

  btnMute.addEventListener('click', function () {
    isMuted        = !isMuted;
    audioEl.muted  = isMuted;
    if (!isMuted && audioEl.src && audioEl.paused) {
      audioEl.play().catch(function () {}); // recupera si el autoplay fue bloqueado
    }
    updateMuteButton();
  });

})();

// renderResult, renderRecCard y EMOTION_MAP están en state.js (compartidos con history.js)
