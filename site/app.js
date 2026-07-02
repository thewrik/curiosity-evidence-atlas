const progress = document.getElementById("progress");

window.addEventListener("scroll", () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
  progress.style.width = `${pct}%`;
});

fetch("data/nomad-analysis.json")
  .then((response) => response.json())
  .then(render)
  .catch((error) => {
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<div class="load-error">Could not load analysis data: ${escapeHtml(error.message)}</div>`
    );
  });

function render(data) {
  renderHeroStats(data.summary);
  renderAnswers(data.answer_cards);
  renderThemeBars(data.theme_counts.slice(0, 8), data.summary.letter_count);
  renderHeatmap(data.theme_year_matrix, data.theme_counts.slice(0, 6).map((item) => item.name));
  renderCompanyBars(data.top_companies.slice(0, 8));
  renderCompanyTimeline(data.recurring_companies.slice(0, 7), data.summary.date_span);
  renderLetterTable(data.research_rich_letters.slice(0, 6));
  renderExternalQuestions(data.external_questions);
}

function renderHeroStats(summary) {
  const stats = [
    ["Letters", summary.letter_count],
    ["Companies", summary.company_count],
    ["Timeline Items", summary.timeline_item_count],
    ["Artifacts", summary.artifact_count],
    ["Period", summary.date_span]
  ];
  document.getElementById("hero-stats").innerHTML = stats
    .map(([label, value]) => `<div><b>${escapeHtml(value)}</b><span>${escapeHtml(label)}</span></div>`)
    .join("");
}

function renderAnswers(cards) {
  document.getElementById("answer-cards").innerHTML = cards
    .map((card, index) => `
      <article class="answer-card">
        <span class="answer-no">${String(index + 1).padStart(2, "0")}</span>
        <h3>${escapeHtml(card.question)}</h3>
        <p>${escapeHtml(card.answer)}</p>
        <small>${escapeHtml(card.evidence)}</small>
      </article>
    `)
    .join("");
}

function renderThemeBars(rows, total) {
  const max = Math.max(...rows.map((row) => row.letters));
  document.getElementById("theme-bars").innerHTML = rows
    .map((row) => `
      <div class="bar-row">
        <span class="bar-label">${escapeHtml(row.name)}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width:${(row.letters / max) * 100}%"></div>
        </div>
        <span class="bar-value">${row.letters}/${total}</span>
      </div>
    `)
    .join("");
}

function renderHeatmap(rows, themes) {
  const cells = rows.flatMap((row) => {
    return themes.map((theme) => {
      const value = Number(row[theme] || 0);
      return `<div class="heat-cell heat-${value}" title="${escapeHtml(theme)} ${row.year}: ${value}">${value || ""}</div>`;
    });
  }).join("");

  document.getElementById("theme-heatmap").innerHTML = `
    <div class="heat-grid" style="--cols:${themes.length}">
      <div class="heat-years">
        ${rows.map((row) => `<span>${row.year}</span>`).join("")}
      </div>
      <div class="heat-labels">
        ${themes.map((theme) => `<span>${shortTheme(theme)}</span>`).join("")}
      </div>
      <div class="heat-cells">${cells}</div>
    </div>
  `;
}

function renderCompanyBars(rows) {
  const max = Math.max(...rows.map((row) => row.mentions));
  document.getElementById("company-bars").innerHTML = rows
    .map((row) => `
      <div class="bar-row">
        <span class="bar-label">${escapeHtml(row.name)}</span>
        <div class="bar-track">
          <div class="bar-fill amber" style="width:${(row.mentions / max) * 100}%"></div>
        </div>
        <span class="bar-value">${row.mentions}</span>
      </div>
    `)
    .join("");
}

function renderCompanyTimeline(rows, span) {
  const [minYear, maxYear] = span.split("-").map(Number);
  const range = maxYear - minYear || 1;
  const ticks = Array.from({ length: maxYear - minYear + 1 }, (_, index) => minYear + index);
  document.getElementById("company-timeline").innerHTML = `
    <div class="timeline-axis">${ticks.map((year) => `<span>${year}</span>`).join("")}</div>
    ${rows.map((row) => {
      const left = ((row.first_year - minYear) / range) * 100;
      const width = Math.max(((row.last_year - row.first_year) / range) * 100, 3);
      return `
        <div class="time-row">
          <span class="time-label">${escapeHtml(row.name)}</span>
          <div class="time-track">
            <div class="time-window" style="left:${left}%;width:${width}%"></div>
          </div>
          <span class="time-years">${row.first_year}-${row.last_year}</span>
        </div>
      `;
    }).join("")}
  `;
}

function renderLetterTable(rows) {
  document.getElementById("letter-table").innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Period</th>
          <th>Letter</th>
          <th>Claims</th>
          <th>Artifacts</th>
          <th>Companies</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((row) => `
          <tr>
            <td>${row.year}</td>
            <td>${escapeHtml(row.title)}</td>
            <td>${row.claim_count}</td>
            <td>${row.artifact_count}</td>
            <td>${row.company_count}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

function renderExternalQuestions(rows) {
  document.getElementById("external-questions").innerHTML = rows
    .map((row) => `
      <article class="next-card">
        <h3>${escapeHtml(row.question)}</h3>
        <p><b>Needs:</b> ${escapeHtml(row.needs)}</p>
        <p><b>FactIQ fit:</b> ${escapeHtml(row.factiq_fit)}</p>
      </article>
    `)
    .join("");
}

function shortTheme(theme) {
  return theme
    .replace("Consumer Value Proposition", "Consumer value")
    .replace("Management Alignment", "Alignment")
    .replace("Patience & Long-Term Horizon", "Patience")
    .replace("Regulation & Industry Structure", "Regulation")
    .replace("Portfolio Construction", "Portfolio")
    .replace("Capital Allocation", "Capital");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#039;");
}
