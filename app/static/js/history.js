'use strict';

(function () {
  const sectionList   = document.getElementById('section-list');
  const sectionDetail = document.getElementById('section-detail');
  const historyList   = document.getElementById('history-list');
  const paginationEl  = document.getElementById('pagination');
  const emptyState    = document.getElementById('history-empty');
  const btnBack       = document.getElementById('btn-back');
  const detailLoading = document.getElementById('detail-loading');
  const detailContent = document.getElementById('detail-content');
  const btnConfirmDel = document.getElementById('btn-confirm-delete');

  let currentPage      = 1;
  let pendingDeleteId  = null;
  let pendingDeleteCol = null;
  let deleteModal      = null;

  // ── Inicialización ───────────────────────────────────────────
  fetchPage(1);

  // ── Cargar una página del historial ─────────────────────────
  async function fetchPage(page) {
    historyList.innerHTML = `
      <div class="col-12 text-center py-5 text-secondary">
        <div class="spinner-border text-warning" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
      </div>`;
    paginationEl.innerHTML = '';
    emptyState.classList.add('d-none');

    try {
      const response = await fetch(`/history?page=${page}`);
      const data     = await response.json();
      currentPage    = data.current_page;
      renderCards(data.items);
      renderPagination(data.pages, data.current_page);
    } catch {
      historyList.innerHTML = `
        <div class="col-12 text-center py-4">
          <p class="text-danger mb-0">Error al cargar el historial.</p>
        </div>`;
    }
  }

  // ── Renderizar tarjetas ──────────────────────────────────────
  function renderCards(items) {
    historyList.innerHTML = '';

    if (!items || items.length === 0) {
      emptyState.classList.remove('d-none');
      return;
    }

    items.forEach(item => {
      const meta = EMOTION_MAP[item.emotion] || { label: item.emotion, color: '#9E9E9E' };
      const date = new Date(item.analyzed_at).toLocaleString('es-ES', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
      });

      const col = document.createElement('div');
      col.className = 'col';
      col.dataset.historyId = item.history_id;

      col.innerHTML = `
        <div class="card bg-dark border-secondary h-100">
          <img src="/static/${item.image_path}"
               alt="Análisis ${meta.label}"
               class="card-img-top"
               style="height:160px;object-fit:cover;"
               onerror="this.closest('.card').querySelector('.card-img-top').style.display='none'">
          <div class="card-body d-flex flex-column">
            <span class="badge rounded-pill mb-2 align-self-start px-3 py-1"
                  style="background-color:${meta.color};">${meta.label}</span>
            <p class="text-white fw-semibold small mb-0">${item.confidence}% de confianza</p>
            <p class="text-secondary small mb-3">
              <i class="bi bi-calendar3 me-1"></i>${date}
            </p>
            <div class="d-flex gap-2 mt-auto">
              <button class="btn btn-sm btn-outline-warning flex-grow-1 btn-detail">
                <i class="bi bi-eye me-1"></i>Ver detalle
              </button>
              <button class="btn btn-sm btn-outline-danger btn-delete" title="Eliminar">
                <i class="bi bi-trash3"></i>
              </button>
            </div>
          </div>
        </div>`;

      col.querySelector('.btn-detail').addEventListener('click', () => openDetail(item.history_id));
      col.querySelector('.btn-delete').addEventListener('click', () => confirmDelete(item.history_id, col));

      historyList.appendChild(col);
    });
  }

  // ── Paginación ───────────────────────────────────────────────
  function renderPagination(pages, current) {
    paginationEl.innerHTML = '';
    if (pages <= 1) return;

    const addItem = (label, page, disabled, active) => {
      const li  = document.createElement('li');
      li.className = `page-item${disabled ? ' disabled' : ''}${active ? ' active' : ''}`;
      const btn = document.createElement('button');
      btn.type      = 'button';
      btn.className = 'page-link bg-dark border-secondary' + (active ? ' text-warning' : ' text-secondary');
      btn.innerHTML = label;
      if (!disabled && !active) btn.addEventListener('click', () => fetchPage(page));
      li.appendChild(btn);
      paginationEl.appendChild(li);
    };

    addItem('&laquo;', current - 1, current === 1, false);
    for (let p = 1; p <= pages; p++) addItem(p, p, false, p === current);
    addItem('&raquo;', current + 1, current === pages, false);
  }

  // ── Ver detalle ──────────────────────────────────────────────
  async function openDetail(historyId) {
    sectionList.classList.add('d-none');
    sectionDetail.classList.remove('d-none');
    detailLoading.classList.remove('d-none');
    detailContent.classList.add('d-none');

    try {
      const response = await fetch(`/history/${historyId}`);
      const data     = await response.json();
      renderResult(data);                    // definida en state.js
      detailLoading.classList.add('d-none');
      detailContent.classList.remove('d-none');
    } catch {
      detailLoading.innerHTML = `
        <p class="text-danger text-center">Error al cargar el detalle.</p>`;
    }
  }

  // ── Volver al listado ────────────────────────────────────────
  btnBack.addEventListener('click', () => {
    sectionDetail.classList.add('d-none');
    sectionList.classList.remove('d-none');
  });

  // ── Eliminar ─────────────────────────────────────────────────
  function confirmDelete(historyId, col) {
    pendingDeleteId  = historyId;
    pendingDeleteCol = col;
    if (!deleteModal) {
      deleteModal = new bootstrap.Modal(document.getElementById('modal-delete'));
    }
    deleteModal.show();
  }

  btnConfirmDel.addEventListener('click', async () => {
    if (!pendingDeleteId) return;
    deleteModal.hide();

    const id  = pendingDeleteId;
    const col = pendingDeleteCol;
    pendingDeleteId  = null;
    pendingDeleteCol = null;

    try {
      const response = await fetch(`/history/${id}`, { method: 'DELETE' });
      const data     = await response.json();

      if (data.success && col) {
        col.style.transition = 'opacity 0.25s';
        col.style.opacity    = '0';
        setTimeout(() => {
          col.remove();
          if (historyList.querySelectorAll('.col').length === 0) {
            fetchPage(Math.max(1, currentPage - 1));
          }
        }, 260);
      }
    } catch {
      // Fallo silencioso: el modal ya se cerró, el usuario puede reintentar
    }
  });

})();
