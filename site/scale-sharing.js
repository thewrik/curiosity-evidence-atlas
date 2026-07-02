const progress = document.getElementById("progress");

window.addEventListener("scroll", () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${max > 0 ? (window.scrollY / max) * 100 : 0}%`;
});

fetch("data/scale-sharing-rq.json")
  .then((response) => response.json())
  .then(render);

function render(data) {
  document.getElementById("rq-title").textContent = data.title;
  document.getElementById("rq-subtitle").textContent = data.subtitle;
  document.getElementById("rq-question").textContent = data.research_question;

  document.getElementById("memory-fit").innerHTML = data.why_this_maps_to_memory
    .map((item) => `<p>${escapeHtml(item)}</p>`)
    .join("");

  document.getElementById("seed-companies").innerHTML = data.seed_companies
    .map((company) => `
      <article class="company-card">
        <div class="company-topline">
          <h3>${escapeHtml(company.name)}</h3>
          <span>${escapeHtml(company.ticker || "private")}</span>
        </div>
        <p class="company-meta">${company.mention_count} mentions · ${company.first_mention_year}-${company.last_mention_year}</p>
        <p><b>Sector:</b> ${escapeHtml(company.sector || "not classified")}</p>
        <p>${escapeHtml(company.nomad_thesis_seed)}</p>
      </article>
    `)
    .join("");

  document.getElementById("hypothesis-grid").innerHTML = data.hypotheses
    .map((item) => `
      <article class="answer-card">
        <span class="answer-no">${escapeHtml(item.id)}</span>
        <h3>${escapeHtml(item.claim)}</h3>
        <p><b>Observable:</b> ${escapeHtml(item.observable)}</p>
        <small>${escapeHtml(item.factiq_surfaces.join(" · "))}</small>
      </article>
    `)
    .join("");

  document.getElementById("repo-basis").innerHTML = data.factiq_repo_basis
    .map((item) => `
      <p><b>${escapeHtml(item.repo_file)}</b><br>${escapeHtml(item.used_for)}</p>
    `)
    .join("");

  document.getElementById("starter-queries").innerHTML = data.starter_queries
    .map((item) => `
      <div class="query-card">
        <span>${escapeHtml(item.tool)}</span>
        <p><b>${escapeHtml(item.label)}</b></p>
        <code>${escapeHtml(item.query)}</code>
      </div>
    `)
    .join("");

  document.getElementById("first-output").innerHTML = `
    <p><b>${escapeHtml(data.first_output.artifact)}:</b> ${escapeHtml(data.first_output.working_title)}</p>
    <ol>
      ${data.first_output.sections.map((section) => `<li>${escapeHtml(section)}</li>`).join("")}
    </ol>
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
