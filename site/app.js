const state = {
  essay: null,
  horizon: 3
};

const progress = document.getElementById("progress");

window.addEventListener("scroll", () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
  progress.style.width = `${pct}%`;
});

const embeddedEssay = document.getElementById("essay-data");

if (embeddedEssay) {
  const essay = JSON.parse(embeddedEssay.textContent);
  state.essay = essay;
  renderEssay(essay);
} else {
  fetch("data/sample-essay.json")
    .then((response) => response.json())
    .then((essay) => {
      state.essay = essay;
      renderEssay(essay);
    });
}

function renderEssay(essay) {
  document.getElementById("kicker").textContent = essay.kicker;
  document.getElementById("title").textContent = essay.title;
  document.getElementById("subtitle").textContent = essay.subtitle;

  const root = document.getElementById("essay");
  root.innerHTML = essay.chapters.map(renderChapter).join("");
  document.getElementById("claims").innerHTML = essay.claims.map(renderClaim).join("");

  const slider = document.getElementById("horizon-slider");
  if (slider) {
    slider.addEventListener("input", (event) => {
      state.horizon = Number(event.target.value);
      updateMechanism();
    });
    updateMechanism();
  }
}

function renderChapter(chapter, index) {
  const paragraphs = chapter.body
    .map((paragraph, paragraphIndex) => {
      const className = index === 0 && paragraphIndex === 0 ? " class=\"dropcap\"" : "";
      return `<p${className}>${escapeHtml(paragraph)}</p>`;
    });

  const sidenote = renderSidenote(chapter.claims);
  const body = [paragraphs[0], sidenote, ...paragraphs.slice(1)].join("");
  const mechanism = chapter.id === "mechanism" ? renderMechanism() : "";

  return `
    <section class="chapter" id="${chapter.id}">
      <p class="chapter-no">Chapter ${chapter.label}</p>
      <h2>${escapeHtml(chapter.title)}</h2>
      <p class="subhead">${escapeHtml(chapter.subhead)}</p>
      <div class="chapter-body">
        ${body}
        ${mechanism}
      </div>
    </section>
  `;
}

function renderSidenote(claimIds) {
  if (!state.essay || !claimIds || claimIds.length === 0) return "";
  const claims = claimIds
    .map((id) => state.essay.claims.find((claim) => claim.id === id))
    .filter(Boolean);
  if (claims.length === 0) return "";
  const text = claims.map((claim) => `<b>${claim.id}</b>: ${escapeHtml(claim.claim)}`).join("<br><br>");
  return `<aside class="sidenote">${text}</aside>`;
}

function renderMechanism() {
  return `
    <div class="mechanism-card" aria-label="Interactive horizon model">
      <div class="mechanism-head">
        <h3>What the horizon lets you see</h3>
        <div class="metric"><span id="horizon-years">3</span> year horizon</div>
      </div>
      <div class="bars">
        <div class="bar-row">
          <span>Visible value</span>
          <div class="track"><div id="visible-fill" class="fill"></div></div>
          <span id="visible-label">61%</span>
        </div>
        <div class="bar-row">
          <span>Ignored value</span>
          <div class="track"><div id="ignored-fill" class="fill ignored"></div></div>
          <span id="ignored-label">39%</span>
        </div>
      </div>
      <label class="horizon-control" for="horizon-slider">
        <input id="horizon-slider" type="range" min="1" max="10" value="3" step="1">
        <output id="horizon-output">3 years</output>
      </label>
      <p class="chart-note">Prototype data only. A real essay would replace this toy output with FactIQ-backed charts and lineage.</p>
    </div>
  `;
}

function updateMechanism() {
  const data = state.essay.sampleData;
  const closest = data.reduce((best, row) => {
    return Math.abs(row.horizon - state.horizon) < Math.abs(best.horizon - state.horizon) ? row : best;
  }, data[0]);

  const visible = closest.visibleValue;
  const ignored = closest.ignoredValue;
  document.getElementById("horizon-years").textContent = state.horizon;
  document.getElementById("horizon-output").textContent = `${state.horizon} years`;
  document.getElementById("visible-fill").style.width = `${visible}%`;
  document.getElementById("ignored-fill").style.width = `${ignored}%`;
  document.getElementById("visible-label").textContent = `${visible}%`;
  document.getElementById("ignored-label").textContent = `${ignored}%`;
}

function renderClaim(claim) {
  return `
    <article class="claim-card">
      <div class="claim-meta"><span>${escapeHtml(claim.status)}</span><span>${escapeHtml(claim.type)}</span></div>
      <h3>${escapeHtml(claim.claim)}</h3>
      <p>${escapeHtml(claim.evidence)}</p>
    </article>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#039;");
}
