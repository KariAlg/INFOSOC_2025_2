/* Visualizador kiosco: solo muestra plazas disponibles y un pequeño estado de aforo */
(function () {
  "use strict";

  // ==== Ajustes ====
  const POLL_MS = 5000;
  const TIMEOUT_MS = 8000;
  // Cambia si tienes un endpoint distinto:
  const endpoint = (zonaId) => `/estacionamientos/api/zonas/${encodeURIComponent(zonaId)}/estado/`;

  // Umbrales por % de libres (no se muestran numéricamente, solo cambia el pill)
  const FREE_OK = 40;    // >= 40% libres -> Libre
  const FREE_WARN = 15;  // 15..39%      -> Medio
                         //  < 15%       -> Crítico

  const $ = (s) => document.querySelector(s);

  function getZonaId() {
    const s = document.getElementById("zona-id");
    if (!s) return null;
    try { return JSON.parse(s.textContent); } catch { return null; }
  }

  function getTotales() {
    const cont = document.querySelector(".visual-kiosk");
    const t = Number(cont?.dataset.totales ?? 0);
    return Number.isFinite(t) ? t : 0;
  }

  function setStateByFreePercent(percentFree) {
    const pill = $("#vkState");
    if (!pill) return;
    if (percentFree >= FREE_OK) {
      pill.textContent = "Libre";
      pill.removeAttribute("data-level");
    } else if (percentFree >= FREE_WARN) {
      pill.textContent = "Medio";
      pill.setAttribute("data-level", "warn");
    } else {
      pill.textContent = "Crítico";
      pill.setAttribute("data-level", "crit");
    }
  }

  function updateUI({ disponibles, totales }) {
    const dispEl = $("#disp");
    if (dispEl) dispEl.textContent = String(disponibles);

    // calcular estado (sin mostrar números)
    totales = totales ?? getTotales();
    const freePct = (totales > 0) ? Math.max(0, Math.min(100, Math.round((disponibles / totales) * 100))) : 100;
    setStateByFreePercent(freePct);
  }

  function fetchWithTimeout(url, ms) {
    const ctl = new AbortController();
    const id = setTimeout(() => ctl.abort(), ms);
    return fetch(url, { signal: ctl.signal, headers: { "Accept": "application/json" } })
      .finally(() => clearTimeout(id));
  }

  function start() {
    const zonaId = getZonaId();
    if (!zonaId) return;

    // Inicializa estado con lo que ya viene en el template
    updateUI({ disponibles: Number($("#disp")?.textContent ?? 0) });

    async function tick() {
      if (document.hidden) return;
      try {
        const res = await fetchWithTimeout(endpoint(zonaId), TIMEOUT_MS);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json(); // esperado: { disponibles, totales? }
        updateUI({ disponibles: Number(data.disponibles ?? 0), totales: Number(data.totales ?? getTotales()) });
      } catch (_) {
        // Silencioso: en kiosco evitamos ruidos; el valor permanece hasta el siguiente intento.
      }
    }

    tick();
    setInterval(tick, POLL_MS);

    document.addEventListener("visibilitychange", () => { if (!document.hidden) tick(); });
  }

  document.addEventListener("DOMContentLoaded", start);
})();
