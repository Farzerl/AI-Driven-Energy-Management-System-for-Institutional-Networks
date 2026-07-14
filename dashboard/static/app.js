const state = { evidence: null, summary: null, control: null };
const NS = "http://www.w3.org/2000/svg";
const COLORS = ["#0b6b61", "#d2861d", "#4c78a8", "#a63a3a", "#7a5aa6"];

function fmt(value, digits = 1) { return Number(value).toFixed(digits); }
function pct(value, digits = 1) { return `${fmt(Number(value) * 100, digits)}%`; }
function esc(value) { return String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char])); }
function toast(message) {
  const el = document.getElementById("toast");
  el.textContent = message;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 2400);
}
async function getJSON(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}
function svgNode(tag, attributes = {}, text = "") {
  const node = document.createElementNS(NS, tag);
  Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, String(value)));
  if (text !== "") node.textContent = text;
  return node;
}
function chartCanvas(id, height = 340) {
  const target = document.getElementById(id);
  target.replaceChildren();
  const chart = svgNode("svg", {
    viewBox: `0 0 760 ${height}`,
    role: "img",
    "aria-label": target.previousElementSibling?.textContent?.trim() || "Data chart",
    preserveAspectRatio: "xMidYMid meet"
  });
  target.appendChild(chart);
  return { chart, width: 760, height };
}
function addText(chart, x, y, text, options = {}) {
  chart.appendChild(svgNode("text", {
    x, y,
    fill: options.fill || "#62727d",
    "font-size": options.size || 11,
    "font-family": "Inter, Segoe UI, Arial",
    "text-anchor": options.anchor || "middle",
    transform: options.rotate ? `rotate(${options.rotate} ${x} ${y})` : ""
  }, text));
}
function addLegend(chart, series, x = 90, y = 18) {
  series.forEach((item, index) => {
    const offset = index * 150;
    chart.appendChild(svgNode("rect", { x: x + offset, y: y - 10, width: 14, height: 9, rx: 2, fill: item.color }));
    addText(chart, x + offset + 20, y - 2, item.name, { anchor: "start", size: 11, fill: "#31434e" });
  });
}
function rangeTicks(maxValue, count = 5) {
  const safe = Math.max(maxValue, 1);
  const rough = safe / count;
  const power = 10 ** Math.floor(Math.log10(rough));
  const normalized = rough / power;
  const step = (normalized <= 1 ? 1 : normalized <= 2 ? 2 : normalized <= 5 ? 5 : 10) * power;
  const top = Math.ceil(safe / step) * step;
  return { step, top, ticks: Array.from({ length: Math.round(top / step) + 1 }, (_, i) => i * step) };
}
function drawGrid(chart, box, scale, label = "") {
  scale.ticks.forEach(value => {
    const y = box.bottom - (value / scale.top) * (box.bottom - box.top);
    chart.appendChild(svgNode("line", { x1: box.left, y1: y, x2: box.right, y2: y, stroke: "#dbe4e8", "stroke-width": 1 }));
    addText(chart, box.left - 10, y + 4, fmt(value, value < 10 ? 1 : 0), { anchor: "end", size: 10 });
  });
  if (label) addText(chart, 18, (box.top + box.bottom) / 2, label, { rotate: -90, size: 11, fill: "#31434e" });
}
function renderBarChart(id, labels, series, yLabel = "", height = 340) {
  const { chart, width } = chartCanvas(id, height);
  const box = { left: 62, right: width - 22, top: 42, bottom: height - 58 };
  const maxValue = Math.max(...series.flatMap(item => item.values), 1);
  const scale = rangeTicks(maxValue * 1.12);
  drawGrid(chart, box, scale, yLabel);
  addLegend(chart, series.map((item, i) => ({ ...item, color: item.color || COLORS[i] })));
  const groupWidth = (box.right - box.left) / labels.length;
  const inner = groupWidth * 0.72;
  const barWidth = inner / series.length;
  labels.forEach((label, labelIndex) => {
    const groupX = box.left + labelIndex * groupWidth + (groupWidth - inner) / 2;
    series.forEach((item, seriesIndex) => {
      const value = Number(item.values[labelIndex] || 0);
      const h = (value / scale.top) * (box.bottom - box.top);
      chart.appendChild(svgNode("rect", {
        x: groupX + seriesIndex * barWidth + 1,
        y: box.bottom - h,
        width: Math.max(barWidth - 3, 2),
        height: h,
        rx: 3,
        fill: item.color || COLORS[seriesIndex]
      }));
      if (labels.length <= 4) addText(chart, groupX + seriesIndex * barWidth + barWidth / 2, box.bottom - h - 7, fmt(value, 2), { size: 10, fill: "#31434e" });
    });
    addText(chart, box.left + labelIndex * groupWidth + groupWidth / 2, box.bottom + 18, label, { size: labels.length > 8 ? 9 : 10, rotate: labels.length > 6 ? -25 : 0 });
  });
}
function renderLineChart(id, labels, series, yLabel = "", height = 340) {
  const { chart, width } = chartCanvas(id, height);
  const box = { left: 62, right: width - 22, top: 42, bottom: height - 58 };
  const maxValue = Math.max(...series.flatMap(item => item.values), 1);
  const scale = rangeTicks(maxValue * 1.1);
  drawGrid(chart, box, scale, yLabel);
  addLegend(chart, series.map((item, i) => ({ ...item, color: item.color || COLORS[i] })));
  const xFor = index => labels.length === 1 ? (box.left + box.right) / 2 : box.left + (index / (labels.length - 1)) * (box.right - box.left);
  series.forEach((item, seriesIndex) => {
    const points = item.values.map((value, index) => `${xFor(index)},${box.bottom - (Number(value) / scale.top) * (box.bottom - box.top)}`).join(" ");
    chart.appendChild(svgNode("polyline", { points, fill: "none", stroke: item.color || COLORS[seriesIndex], "stroke-width": 3, "stroke-linejoin": "round", "stroke-linecap": "round" }));
    item.values.forEach((value, index) => chart.appendChild(svgNode("circle", { cx: xFor(index), cy: box.bottom - (Number(value) / scale.top) * (box.bottom - box.top), r: 4, fill: item.color || COLORS[seriesIndex], stroke: "#fff", "stroke-width": 2 })));
  });
  const step = Math.max(1, Math.ceil(labels.length / 8));
  labels.forEach((label, index) => {
    if (index % step === 0 || index === labels.length - 1) addText(chart, xFor(index), box.bottom + 18, label, { size: 9, rotate: labels.length > 8 ? -30 : 0 });
  });
}
function heatColor(value, min, max) {
  const ratio = max === min ? 0.5 : Math.max(0, Math.min(1, (value - min) / (max - min)));
  const hue = 175 - ratio * 145;
  const light = 94 - ratio * 43;
  return `hsl(${hue} 62% ${light}%)`;
}
function renderHeatmap(id, xLabels, yLabels, values, height = 430, showNumbers = false) {
  const { chart, width } = chartCanvas(id, height);
  const box = { left: 72, right: width - 30, top: 28, bottom: height - 60 };
  const flat = values.flat().map(Number);
  const min = Math.min(...flat), max = Math.max(...flat);
  const cellW = (box.right - box.left) / xLabels.length;
  const cellH = (box.bottom - box.top) / yLabels.length;
  values.forEach((row, rowIndex) => row.forEach((value, columnIndex) => {
    chart.appendChild(svgNode("rect", {
      x: box.left + columnIndex * cellW,
      y: box.top + rowIndex * cellH,
      width: cellW + 0.3,
      height: cellH + 0.3,
      fill: heatColor(Number(value), min, max),
      stroke: "rgba(255,255,255,.55)",
      "stroke-width": 0.5
    }));
    if (showNumbers) addText(chart, box.left + columnIndex * cellW + cellW / 2, box.top + rowIndex * cellH + cellH / 2 + 4, String(value), { size: 12, fill: Number(value) > (min + max) / 2 ? "#fff" : "#18313a" });
  }));
  yLabels.forEach((label, index) => addText(chart, box.left - 9, box.top + index * cellH + cellH / 2 + 4, label, { anchor: "end", size: 10 }));
  const xStep = Math.max(1, Math.ceil(xLabels.length / 10));
  xLabels.forEach((label, index) => {
    if (index % xStep === 0 || index === xLabels.length - 1) addText(chart, box.left + index * cellW + cellW / 2, box.bottom + 17, label, { size: 9, rotate: -25 });
  });
  addText(chart, box.left, height - 14, `Lower ${fmt(min, 1)}`, { anchor: "start", size: 10 });
  addText(chart, box.right, height - 14, `Higher ${fmt(max, 1)}`, { anchor: "end", size: 10 });
}

function activateTabs() {
  const activate = button => {
    document.querySelectorAll(".tab").forEach(item => item.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    document.getElementById(button.dataset.tab).classList.add("active");
  };
  document.querySelectorAll(".tab").forEach(button => button.addEventListener("click", () => activate(button)));
  const requested = new URLSearchParams(window.location.search).get("tab");
  const requestedButton = requested ? document.querySelector(`.tab[data-tab="${requested}"]`) : null;
  if (requestedButton) activate(requestedButton);
}
function renderKPIs(summary) {
  const cards = [
    ["Facilities", summary.dataset.facilities, `${summary.dataset.intervals.toLocaleString()} half-hour intervals`],
    ["Usable data", `${fmt(summary.dataset.usable_percent, 2)}%`, "After conservative cleaning"],
    ["Forecast MAE", `${fmt(summary.forecast.model_mae_kva, 2)} kVA`, `${fmt(summary.forecast.mae_reduction_percent, 1)}% below persistence`],
    ["High-risk warning", pct(summary.peak_risk.high_warning_recall, 1), "Medium or high warning"],
    ["Critical miss", pct(summary.peak_risk.critical_miss_rate, 2), "High event classified low"]
  ];
  document.getElementById("kpi-grid").innerHTML = cards.map(([label, value, detail]) => `<div class="kpi"><div class="label">${label}</div><div class="value">${value}</div><div class="detail">${detail}</div></div>`).join("");
}
function renderForecast(evidence) {
  const f = evidence.forecast;
  renderBarChart("forecast-chart", ["Persistence", "AI model", "Hybrid"], [{ name: "MAE", values: [f.baseline.mae_kva, f.model.mae_kva, f.operational.mae_kva], color: COLORS[0] }], "MAE (kVA)");
  const cv = f.rolling_validation;
  renderLineChart("rolling-chart", cv.map(row => row.validation_month), [
    { name: "AI model", values: cv.map(row => row.model.mae_kva), color: COLORS[0] },
    { name: "Persistence", values: cv.map(row => row.persistence.mae_kva), color: COLORS[1] }
  ], "MAE (kVA)");
}
function renderEvidence(evidence) {
  const aggregate = evidence.aggregate_visualisation_data;
  if (aggregate.status !== "generated") return;
  const heat = aggregate.campus_demand_heatmap;
  renderHeatmap("heatmap-chart", heat.slots, heat.days, heat.normalized_mean_kva, 430, false);
  const monthly = aggregate.monthly_energy_index;
  renderLineChart("monthly-chart", monthly.map(row => row.month), [{ name: "Energy index", values: monthly.map(row => row.energy_index), color: COLORS[0] }], "Index", 430);
  const profile = aggregate.day_type_profiles;
  renderLineChart("profile-chart", [...new Set(profile.map(row => row.time))], ["Weekday", "Weekend"].map((day, index) => ({
    name: day,
    values: profile.filter(row => row.day_type === day).map(row => row.normalized_kva),
    color: COLORS[index]
  })), "Normalized demand");
  const facilities = aggregate.facility_aggregate_aliases.slice(0, 12);
  renderBarChart("facility-chart", facilities.map(row => row.facility), [{ name: "Energy share", values: facilities.map(row => row.energy_share_percent), color: COLORS[2] }], "Energy share (%)");
  const q = evidence.dataset_quality;
  const quality = [
    [q.missing_intervals, "Missing intervals", "Inserted explicitly, not interpolated"],
    [q.partial_intervals, "Partial intervals", "Excluded from benchmark targets"],
    [q.negative_active_rows, "Negative active rows", "Flagged and excluded pending verification"],
    [q.forecast_usable_rows.toLocaleString(), "Forecast-usable rows", `${fmt(q.forecast_usable_percent, 3)}% of the completed grid`]
  ];
  document.getElementById("quality-grid").innerHTML = quality.map(([value, label, detail]) => `<div><strong>${esc(value)}</strong><span>${esc(label)}. ${esc(detail)}</span></div>`).join("");
}
function renderControl(control, evidence) {
  const rule = control.simple_rule_controller;
  const ai = control.forecast_assisted_controller;
  const labels = ["High warning recall", "Exact high recall", "False action rate"];
  renderBarChart("control-chart", labels, [
    { name: "Simple rule", values: [rule.high_warning_recall_medium_or_high * 100, rule.high_exact_recall * 100, rule.false_action_rate_on_actual_low * 100], color: COLORS[1] },
    { name: "Forecast-assisted", values: [ai.high_warning_recall_medium_or_high * 100, ai.high_exact_recall * 100, ai.false_action_rate_on_actual_low * 100], color: COLORS[0] }
  ], "Percent", 430);
  const comparison = control.comparison;
  document.getElementById("tradeoff").innerHTML = [
    [`${fmt(comparison.critical_miss_rate_reduction_percentage_points, 2)} pp`, "Reduction in high events missed as low"],
    [comparison.critical_misses_avoided, "Critical misses avoided across the April test"],
    [`${fmt(comparison.high_warning_recall_gain_percentage_points, 2)} pp`, "Gain in high-event warning recall"],
    [`+${fmt(comparison.additional_action_rate_percentage_points, 2)} pp`, "Additional operator preparation alerts"],
    [`+${fmt(comparison.additional_false_action_rate_percentage_points, 2)} pp`, "False-action trade-off on actual low intervals"]
  ].map(([value, label]) => `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`).join("");
  const peak = evidence.peak_risk;
  renderHeatmap("confusion-chart", ["Low", "Medium", "High"], ["Low", "Medium", "High"], peak.confusion_matrix, 430, true);
}
async function loadAlerts() {
  const payload = await getJSON("/api/alerts");
  const list = document.getElementById("alert-list");
  if (!payload.alerts.length) { list.innerHTML = '<div class="empty">No active sample alerts.</div>'; return; }
  list.innerHTML = payload.alerts.map(alert => `
    <article class="alert ${esc(alert.risk)}" data-alert="${esc(alert.alert_id)}">
      <div><span class="risk-badge">${esc(alert.risk)}</span><span class="alert-title">${esc(alert.facility_name)}</span>
        <div class="alert-meta">${esc(alert.timestamp.replace("T", " "))} · ${esc(alert.tariff_period)} · ${fmt(alert.utilization_percent, 1)}% of limit</div></div>
      <div><strong>${alert.current_kva.toFixed(1)} kVA current${alert.forecast_kva !== undefined ? ` → ${Number(alert.forecast_kva).toFixed(1)} kVA forecast` : ""}</strong> / ${alert.facility_limit_kva.toFixed(1)} kVA limit
        <div class="alert-meta">${esc(alert.recommended_action)}</div>
        <div class="alert-meta">Planning reduction: ${alert.planning_reduction_kva.toFixed(1)} kVA. Engineering proxy, not realised savings.</div></div>
      <div class="alert-actions">
        <button class="confirm" data-decision="confirm">Confirm</button><button data-decision="defer">Defer</button><button data-decision="dismiss">Dismiss</button><button data-decision="mute">Mute</button>
      </div>
    </article>`).join("");
  list.querySelectorAll("button[data-decision]").forEach(button => button.addEventListener("click", async () => {
    const card = button.closest(".alert");
    const alert = payload.alerts.find(item => item.alert_id === card.dataset.alert);
    const note = prompt("Operator note (optional):", "") || "";
    try {
      await getJSON("/api/operator-decisions", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ alert_id: alert.alert_id, decision: button.dataset.decision, operator: "demo-operator", note, requested_reduction_kva: alert.planning_reduction_kva }) });
      toast(`Decision recorded: ${button.dataset.decision}`);
      await loadDecisionLog();
    } catch (error) { toast(`Could not save decision: ${error.message}`); }
  }));
}
async function loadDecisionLog() {
  const payload = await getJSON("/api/operator-decisions?limit=30");
  const element = document.getElementById("decision-log");
  if (!payload.items.length) { element.innerHTML = '<div class="empty">No operator decisions recorded.</div>'; return; }
  element.innerHTML = payload.items.map(row => `<div class="log-row"><span>${esc(row.recorded_utc.replace("T", " ").slice(0, 19))}</span><strong>${esc(row.decision)}</strong><span>${esc(row.alert_id)} · ${esc(row.operator)}${row.note ? ` · ${esc(row.note)}` : ""}</span></div>`).join("");
}

function edgeValue(value, fallback = "Not reported") {
  return value === null || value === undefined || value === "" ? fallback : value;
}
async function loadEdgeStatus() {
  const [status, readings] = await Promise.all([
    getJSON("/api/edge-status"),
    getJSON("/api/meter-readings?limit=12")
  ]);
  const store = status.store || {};
  const gateway = status.gateway || {};
  const cards = [
    ["Gateway state", edgeValue(gateway.state, "Not started"), edgeValue(gateway.gateway_id, "Run START_EDGE_DEMO.bat")],
    ["Received readings", Number(store.received_count || 0).toLocaleString(), "Accepted by the runtime API store"],
    ["Buffered locally", Number(gateway.buffered_readings || 0).toLocaleString(), "Waiting for server recovery"],
    ["Last facility", edgeValue(store.latest_facility_id, "None"), "Public facility alias"],
    ["Operating boundary", "Monitoring only", "No automatic switching"]
  ];
  document.getElementById("edge-kpis").innerHTML = cards.map(([label, value, detail]) => `<div class="kpi"><div class="label">${esc(label)}</div><div class="value">${esc(value)}</div><div class="detail">${esc(detail)}</div></div>`).join("");
  const details = [
    ["Gateway ID", edgeValue(gateway.gateway_id)],
    ["Facility", edgeValue(gateway.facility_id)],
    ["Mode", edgeValue(gateway.mode)],
    ["Sent readings", Number(gateway.sent_readings || 0).toLocaleString()],
    ["Failed batches", Number(gateway.failed_batches || 0).toLocaleString()],
    ["Last success", edgeValue(gateway.last_success_utc)],
    ["Last error", edgeValue(gateway.last_error, "None")]
  ];
  document.getElementById("edge-status-detail").innerHTML = details.map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join("");
  const element = document.getElementById("edge-readings");
  if (!readings.items.length) {
    element.innerHTML = '<div class="empty">No edge-demo readings received yet. Run START_EDGE_DEMO.bat.</div>';
    return;
  }
  element.innerHTML = readings.items.map(row => `<div class="reading-row"><span>${esc(String(row.timestamp).replace("T", " "))}</span><strong>${fmt(row.kva, 1)} kVA</strong><span>${fmt(row.kwh, 1)} kWh</span><span>PF ${fmt(row.power_factor, 2)}</span></div>`).join("");
}



function riskLabel(value) {
  const safe = String(value || "unknown").toLowerCase();
  return safe.charAt(0).toUpperCase() + safe.slice(1);
}
async function loadLiveForecasts() {
  const [model, payload] = await Promise.all([
    getJSON("/api/model-status"),
    getJSON("/api/live-forecasts?limit=24")
  ]);
  const items = payload.items || [];
  const latest = items[0] || null;
  const metrics = model.metrics || {};
  const cards = [
    ["Model state", model.ready ? "Ready" : "Unavailable", model.model_mode || "No model mode"],
    ["Forecasts generated", Number(payload.summary?.forecast_count || 0).toLocaleString(), "Runtime forecast store"],
    ["Latest facility", latest?.facility_id || "Waiting", "Public facility alias"],
    ["Next-half-hour risk", latest ? riskLabel(latest.peak_risk) : "Waiting", latest ? `${fmt(latest.utilization_percent, 1)}% of limit` : "Run START_EDGE_DEMO.bat"],
    ["Live model MAE", metrics.model_mae_kva !== undefined ? `${fmt(metrics.model_mae_kva, 2)} kVA` : "Not reported", model.source === "private_model" ? "Private chronological test" : "Public synthetic demo test"]
  ];
  document.getElementById("live-kpis").innerHTML = cards.map(([label, value, detail]) => `<div class="kpi"><div class="label">${esc(label)}</div><div class="value">${esc(value)}</div><div class="detail">${esc(detail)}</div></div>`).join("");

  const statusRows = [
    ["Source", model.source || "Unavailable"],
    ["Mode", model.model_mode || "Unavailable"],
    ["Model family", model.model_family || "Unavailable"],
    ["Prediction horizon", `${Number(model.prediction_horizon_minutes || 30)} minutes`],
    ["Required history", `${Number(model.minimum_history_intervals || 4)} intervals`],
    ["Facilities in training", Number(model.facility_count || 0).toLocaleString()],
    ["Operating mode", model.operating_mode || "advisory"],
    ["Error", model.error || "None"]
  ];
  document.getElementById("live-model-status").innerHTML = statusRows.map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join("");

  if (!items.length) {
    document.getElementById("live-forecast-chart").innerHTML = '<div class="empty">No live forecasts yet. Start the edge demo and allow at least four completed interval values to arrive.</div>';
    document.getElementById("live-forecast-table").innerHTML = '<div class="empty">Waiting for edge values.</div>';
    return;
  }
  const chartItems = [...items].reverse().slice(-12);
  renderLineChart(
    "live-forecast-chart",
    chartItems.map(row => String(row.forecast_timestamp).slice(11, 16)),
    [
      { name: "Current kVA", values: chartItems.map(row => Number(row.current_kva)), color: COLORS[2] },
      { name: "Forecast kVA", values: chartItems.map(row => Number(row.forecast_kva)), color: COLORS[0] },
      { name: "Facility limit", values: chartItems.map(row => Number(row.facility_limit_kva)), color: COLORS[3] }
    ],
    "kVA"
  );
  document.getElementById("live-forecast-table").innerHTML = `<table class="cost-table live-table">
    <thead><tr><th>Facility</th><th>Reading</th><th>Forecast for</th><th>Current</th><th>Forecast</th><th>Limit</th><th>Risk</th><th>Method</th><th>Recommendation</th></tr></thead>
    <tbody>${items.map(row => `<tr><td>${esc(row.facility_id)}</td><td>${esc(String(row.reading_timestamp).replace("T", " ").slice(0, 19))}</td><td>${esc(String(row.forecast_timestamp).replace("T", " ").slice(0, 19))}</td><td>${fmt(row.current_kva, 1)} kVA</td><td>${fmt(row.forecast_kva, 1)} kVA</td><td>${fmt(row.facility_limit_kva, 1)} kVA</td><td><span class="risk-badge ${esc(row.peak_risk)}">${esc(row.peak_risk)}</span></td><td>${esc(row.inference_method || "trained_model")}</td><td class="wrap-cell">${esc(row.recommended_action)}</td></tr>`).join("")}</tbody>
  </table>`;
}

function usd(value, digits = 0) {
  return `$${Number(value || 0).toLocaleString(undefined, { minimumFractionDigits: digits, maximumFractionDigits: digits })}`;
}

// Backwards-compatible adapter for Stage 4 cost widgets.
// Older Stage 4 files called barChart(id, labels, numericValues, yLabel).
// The current dashboard chart engine uses renderBarChart(id, labels, series, yLabel).
function barChart(id, labels, valuesOrSeries, yLabel = "") {
  const series = Array.isArray(valuesOrSeries)
    && valuesOrSeries.length > 0
    && typeof valuesOrSeries[0] === "object"
    && valuesOrSeries[0] !== null
    && Array.isArray(valuesOrSeries[0].values)
      ? valuesOrSeries
      : [{
          name: yLabel || "Value",
          values: Array.isArray(valuesOrSeries)
            ? valuesOrSeries.map(value => Number(value || 0))
            : [],
          color: COLORS[0]
        }];
  return renderBarChart(id, labels, series, yLabel);
}

async function loadCostImpact() {
  const payload = await getJSON("/api/cost-impact");
  const summary = payload.summary || {};
  const monthly = payload.monthly || [];
  const scenarios = payload.scenarios || [];
  const central = scenarios.find(row => row.scenario === "Central planning") || scenarios[0] || {};
  const billRange = summary.estimated_monthly_bill_range_usd || {};
  const demandRange = summary.estimated_peak_demand_range_kva || {};
  const cards = [
    ["Indicative study-period bill", usd(summary.estimated_baseline_bill_usd), "Public average tariff, not an invoice"],
    ["Average tariff anchor", `${fmt((summary.average_end_user_tariff_usd_per_kwh || 0) * 100, 2)} USc/kWh`, "ZERA public national average"],
    ["Monthly bill range", `${usd(billRange.minimum)} - ${usd(billRange.maximum)}`, "September 2025 to April 2026"],
    ["Estimated demand range", `${fmt(demandRange.minimum, 0)} - ${fmt(demandRange.maximum, 0)} kVA`, "Derived from energy and load factor"],
    ["Central scenario", `${usd(central.estimated_total_saving_usd)} (${fmt(central.estimated_saving_percent_of_baseline, 2)}%)`, "Planning estimate, not realised savings"]
  ];
  document.getElementById("cost-kpis").innerHTML = cards.map(([label, value, detail]) => `<div class="kpi"><div class="label">${esc(label)}</div><div class="value">${esc(value)}</div><div class="detail">${esc(detail)}</div></div>`).join("");

  if (monthly.length) {
    renderBarChart(
      "cost-monthly-chart",
      monthly.map(row => row.month),
      [{ name: "Estimated bill", values: monthly.map(row => Number(row.estimated_total_bill_usd)), color: COLORS[0] }],
      "Estimated bill (USD)",
      340
    );
    document.getElementById("cost-monthly-table").innerHTML = `<table class="cost-table">
      <thead><tr><th>Month</th><th>Energy</th><th>Load factor</th><th>Max demand</th><th>Bill estimate</th></tr></thead>
      <tbody>${monthly.map(row => `<tr><td>${esc(row.month)}</td><td>${Number(row.energy_kwh).toLocaleString()} kWh</td><td>${fmt(row.load_factor, 2)}</td><td>${fmt(row.estimated_max_demand_kva, 0)} kVA</td><td>${usd(row.estimated_total_bill_usd)}</td></tr>`).join("")}</tbody>
    </table>`;
  } else {
    document.getElementById("cost-monthly-chart").innerHTML = '<div class="empty">Cost evidence has not been generated.</div>';
    document.getElementById("cost-monthly-table").innerHTML = '<div class="empty">Run RUN_STAGE4_COST_MODEL.bat.</div>';
  }

  if (scenarios.length) {
    renderBarChart(
      "cost-scenario-chart",
      scenarios.map(row => row.scenario.replace(" planning", "")),
      [{ name: "Estimated saving", values: scenarios.map(row => Number(row.estimated_total_saving_usd)), color: COLORS[2] }],
      "Estimated saving (USD)",
      340
    );
  } else {
    document.getElementById("cost-scenario-chart").innerHTML = '<div class="empty">No scenarios available.</div>';
  }

  const assumptionRows = [
    ["Public tariff anchor", `${fmt((summary.average_end_user_tariff_usd_per_kwh || 0) * 100, 2)} USc/kWh`],
    ["Study period", summary.study_period || "Not reported"],
    ["Months modelled", summary.months_modelled || 0],
    ["Cost status", payload.status || "Not generated"],
    ["Financial status", "Planning estimate only"],
    ["Private bill", "Not disclosed or reproduced"]
  ];
  document.getElementById("cost-assumptions").innerHTML = assumptionRows.map(([label, value]) => `<div><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join("");
  if (summary.claim_boundary) document.getElementById("cost-boundary").textContent = summary.claim_boundary;
}

async function init() {
  activateTabs();
  document.getElementById("refresh-alerts").addEventListener("click", () => loadAlerts().catch(error => toast(`Alert refresh failed: ${error.message}`)));
  document.getElementById("refresh-edge").addEventListener("click", () => loadEdgeStatus().catch(error => toast(`Edge status failed: ${error.message}`)));
  document.getElementById("refresh-cost").addEventListener("click", () => loadCostImpact().catch(error => toast(`Cost estimate failed: ${error.message}`)));
  document.getElementById("refresh-live").addEventListener("click", () => Promise.all([loadLiveForecasts(), loadAlerts()]).catch(error => toast(`Live forecast failed: ${error.message}`)));

  const status = document.getElementById("api-status");
  try {
    const health = await getJSON("/api/health");
    status.textContent = health.status === "online" ? "API online" : health.status;
    status.classList.add("online");
  } catch (error) {
    status.textContent = "API unavailable";
    toast(`Health check failed: ${error.message}`);
    return;
  }

  try {
    [state.summary, state.evidence, state.control] = await Promise.all([
      getJSON("/api/summary"),
      getJSON("/api/evidence"),
      getJSON("/api/control-comparison")
    ]);
    renderKPIs(state.summary);
    renderForecast(state.evidence);
    renderEvidence(state.evidence);
    renderControl(state.control, state.evidence);
  } catch (error) {
    toast(`Core evidence failed to load: ${error.message}`);
  }

  const optionalLoads = await Promise.allSettled([
    loadAlerts(),
    loadDecisionLog(),
    loadEdgeStatus(),
    loadLiveForecasts(),
    loadCostImpact()
  ]);
  optionalLoads.forEach(result => {
    if (result.status === "rejected") {
      console.error(result.reason);
    }
  });
}
init();
