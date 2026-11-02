"use strict";
const $ = (s) => document.querySelector(s),
  esc = (v) =>
    String(v ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
const GH = "https://github.com/chirag-7/neural-data-direct-inference";
const HISTORICAL_MODELS = ["gpt-5.6-sol", "gpt-6-sol", "gpt-6.1-sol"];
const COMPARISON_MODELS = ["gpt-4.1-2025-04-14", "gpt-5-2025-08-07", "gpt-5.6-sol", "gpt-6.1-sol"];
let MODELS = [...COMPARISON_MODELS], comparisonActive = true, historicalRecords = [];
const COLORS = {
  "gpt-4.1-2025-04-14": "#347e73",
  "gpt-5-2025-08-07": "#3c7fa4",
  "gpt-5.6-sol": "#9475aa",
  "gpt-6-sol": "#3c7fa4",
  "gpt-6.1-sol": "#c77735",
};
const NAMES = {
  "gpt-4.1-2025-04-14": "GPT-4.1",
  "gpt-5-2025-08-07": "GPT-5",
  "gpt-5.6-sol": "GPT-5.6 Sol",
  "gpt-6-sol": "GPT-6 Sol",
  "gpt-6.1-sol": "GPT-6.1 Sol",
  "wavpack-high": "WavPack 5.8 · lossless very-high",
  "delta-blosc-zstd": "Delta + Blosc/Zstd9 · bitshuffle",
  mountainsort5: "MountainSort5 · scheme 1",
  "yasa-eeg": "YASA · pretrained EEG",
  "pyriemann-ts-svm": "pyRiemann · TS-SVM",
  "pyriemann-aligned": "pyRiemann · aligned TS-SVM",
  "polya-gamma": "Polya–Gamma Gibbs · local",
  laplace: "Laplace approximation",
  singler: "SingleR · donor-layer profiles",
  "behavioral-glm": "Behavioral GLM · paper-inspired",
  "xdawn-tslr": "xDAWN · fixed",
  "xdawn-tslr-tuned": "xDAWN · train-CV tuned",
  "canonical-posterior": "Posterior median · post-hoc audit",
  "canonical-mle": "Canonical MLE",
  "oasis-default": "OASIS · default AR1",
  "raw-calcium": "Raw calcium",
  spikepack: "Spikepack · 100 µs grid",
  "mean-baseline": "Mean of observed history",
  midpoint: "Midpoint",
  "mriqc-rfc-2017": "MRIQC · archived 2017",
  deneux: "Deneux · archived",
  speiser: "Speiser · archived",
  friedrich: "Friedrich · archived",
  rupprecht: "Rupprecht · archived",
};
const METRIC_LABELS = {
  recording_mean_motion_rmse_um: "Recording-mean motion RMSE (µm)",
  mean_encoded_bits_per_event_50us: "Mean encoded bits/event · ≤50 µs timing error",
  animal_mean_neuron_pearson_smoothed200ms: "Animal-equal neuron Pearson correlation · 200 ms smoothing",
  mse_dff: "Calcium forecast mean squared error (dF/F)²",
  donor_block_macro_rmse: "Donor/block-balanced fraction RMSE",
  class_balanced_mouse_accuracy: "Class-balanced mouse accuracy",
  recording_macro_event_f1_20ms_onset_20ms_or_20pct_offset: "Recording-mean event F1 · 20 ms onset / duration-aware offset",
};
const metricLabel = (metric) => METRIC_LABELS[metric] || metric;
const CATEGORIES = {
  A: "Behavior & movement",
  B: "Extracellular data",
  C: "Calcium imaging",
  D: "Voltage & intracellular",
  E: "Population dynamics",
  F: "Neural encoding",
  G: "Intracortical BCI",
  H: "EEG, MEG & sleep",
  I: "Neuroimaging",
  J: "Anatomy & microscopy",
  K: "Cell & molecular data",
  L: "Statistical inference",
  M: "Cognition & control",
  N: "Analysis workflows",
};
const TITLES = {
  A09: "Social behavior classification",
  A14: "Missing-pose recovery",
  A15: "Birdsong acoustic-event detection",
  B03: "Synthetic probe-motion recovery",
  B08: "Spike-event compression · 50 µs tolerance",
  C06: "Held-out-fish spike inference",
  E06: "Zebrafish activity forecasting",
  K05: "Measured cell-fraction calibration",
  K06: "Optotagged PV/SST waveform inference",
  B01: "Extracellular spike sorting",
  B07: "Lossless voltage compression",
  C05: "Calcium-to-spike inference",
  D02: "Passive cell-response prediction",
  E01: "Population activity inference",
  F04: "Retinal image-response encoding",
  G01: "Cross-day finger-velocity decoding",
  H01: "EEG motor-imagery decoding",
  H02: "P300 target ranking",
  H08: "Sleep-stage classification",
  H16: "EEG artifact removal",
  I07: "fNIRS condition classification",
  I10: "MRI scan-quality classification",
  J08: "Microscopy puncta segmentation",
  K01: "Cell morphology classification",
  L06: "Spiking-neuron posterior inference",
  K04: "Cortical-layer label transfer",
  M01: "Conditional mouse-choice prediction",
  L04: "Place-cell count encoding",
  M04: "Cognitive parameter recovery",
  N05: "NWB file analysis",
};
const DATASETS = {
  A09: "CalMS21 · processed pose context",
  A14: "Rat7M · artificial HeadF gaps",
  A15: "DAS / Bengalese finch · one held-out bird",
  B03: "SpikeInterface · eight synthetic recordings",
  B08: "FALCON M2 · seven runs shared with G01",
  C06: "CASCADE DS04 · two held-out fish",
  E06: "ZAPBench · one brain, two dependent slices",
  K05: "Human DLPFC · orthogonal IF/RNAScope fractions",
  K06: "CellExplorer / Allen · five held-out mice",
  B01: "MEArec · 10 s stationary simulation",
  B07: "AIND / IBL · 16 real short chunks",
  C05: "Spikefinder · five preparations",
  D02: "Allen Cell Types · one passive cell",
  E01: "NLB · Maze, Area2, DMFC",
  F04: "Goldin 2022 · one retinal preparation",
  G01: "FALCON M2 · four recording days",
  H01: "PhysioNet EEGMMI · held-out subjects",
  H02: "Brain Invaders 2012 · 25 people",
  H08: "Sleep-EDF · eight first nights",
  H16: "EEGdenoiseNet · semisynthetic EOG mixtures",
  I07: "FRESH · tapping conditions",
  I10: "MRIQC · ABIDE → DS030",
  J08: "SynAPSeg · two held-out 2D fields",
  K01: "Allen Cell Types · ephys features",
  L06: "sbibm · ten synthetic GLM observations",
  K04: "HumanPilot DLPFC · held-out donor",
  M01: "IBL behavior · 17 held-out mice",
  L04: "Kramer · one rat place cell",
  M04: "Synthetic two-choice Q-learning agents",
  N05: "Allen · one legacy NWB file",
};
let b01Metric = "primary";
let catalog,
  summary,
  replication,
  records = [],
  excluded = [],
  selectedTask = "B03",
  selectedSlice = "",
  l06Metric = "c2st",
  c06Metric = "primary",
  l06Observation = "mean",
  plotView = "graph",
  showAllRefs = false,
  showReferences = true,
  startAtZero = false,
  query = "",
  listMode = "measured",
  hiddenModels = new Set(),
  analysisClass = "historical_specialist",
  analysisScope = "observed_data";
const label = (x) =>
    NAMES[x] ||
    (x.startsWith("vassi-run-") ? "VASSI · archived " + x.slice(-2) : x),
  title = (e) => TITLES[e.id] || e.task;
const valid = (r) => r && Number.isFinite(r.score),
  rowsFor = (id) => records.filter((r) => r.benchmark_id === id),
  measured = (id) => rowsFor(id).some((r) => MODELS.includes(r.model));
const link = (url, text, cls = "") =>
  `<a class="${cls}" href="${esc(url)}" target="_blank" rel="noopener noreferrer">${text} ↗</a>`;
const route = (path, text, cls = "") =>
  `<a class="${cls}" href="#/${path}">${text}</a>`;
const fmt = (v) =>
  Number.isFinite(v)
    ? Math.abs(v) > 0 && Math.abs(v) < 0.00001
      ? v.toExponential(2)
      : v.toFixed(4)
    : "—";
function methodName(r) {
  if (r.display_name) return r.display_name;
  if (r.model === "task-baseline") {
    if (r.benchmark_id === "B07") return "Raw zlib9";
    if (r.benchmark_id === "B03") return "SpikeInterface · decentralized registration";
    if (r.benchmark_id === "B08") return "Quantized deltas + zlib9";
    if (r.benchmark_id === "C06") return "OASIS AR1 · training-calibrated";
    if (r.benchmark_id === "E06") return "NLinear · analytical ridge1";
    if (r.benchmark_id === "K05") return "Donor-CV weighted ridge";
    if (r.benchmark_id === "K06") return "Mouse-CV SVM / ExtraTrees";
    if (r.benchmark_id === "A15") return "Spectral boosting · event-CV";
    if (r.benchmark_id === "J08") return "StarDist · author archive";
    if (r.benchmark_id === "N05") return "Audited file reference";
    if (r.benchmark_id === "G01") return "FALCON-style ridge";
    if (r.benchmark_id === "K04") return "Balanced multinomial logit";
    if (r.benchmark_id === "M01") return "Training mean choice probability";
    if (r.benchmark_id === "H02") return "Shrinkage LDA · time bins";
    if (r.benchmark_id === "F04") return "PCA–Poisson GLM";
    return "Conventional task baseline";
  }
  return label(r.model);
}
function isSpecialist(r) {
  if (["historical_specialist", "local_specialist", "pretrained_specialist"].includes(r.display_reference_class)) return true;
  return (
    [
      "spikepack",
      "wavpack-high",
      "delta-blosc-zstd",
      "deneux",
      "speiser",
      "friedrich",
      "rupprecht",
      "oasis-default",
      "mountainsort5",
      "mriqc-rfc-2017",
      "yasa-eeg",
      "pyriemann-ts-svm",
      "pyriemann-aligned",
      "xdawn-tslr",
      "polya-gamma",
      "singler",
      "behavioral-glm",
      "xdawn-tslr-tuned",
    ].includes(r.model) ||
    r.model.startsWith("vassi-run-") ||
    (["J08", "B03", "C06"].includes(r.benchmark_id) && r.model === "task-baseline")
  );
}
function isDomainReference(r) {
  return r.model === "behavioral-glm" || (r.benchmark_id === "E06" && r.model === "task-baseline");
}
function evidence(r) {
  if (MODELS.includes(r.model)) return "Direct inference";
  if (r.display_reference_class === "historical_specialist") return "Archived specialist · current best unverified";
  if (r.display_reference_class === "local_specialist") return "Local specialist · current best unverified";
  if (r.display_reference_class === "pretrained_specialist") return "Pretrained specialist · current best unverified";
  if (r.benchmark_id === "B07" && isSpecialist(r)) return "Domain-aligned codec reference";
  if (r.model === "behavioral-glm") return "Source-inspired pooled domain reference";
  if (r.benchmark_id === "E06" && r.model === "task-baseline") return "Conventional domain reference · altered NLinear optimization";
  if (["B03", "C06", "B08"].includes(r.benchmark_id) && isSpecialist(r)) return "Local specialist reproduction · global best unverified";
  if (r.reference_type === "pretrained_specialist")
    return "Pretrained specialist";
  if (isSpecialist(r))
    return r.reference_type === "archived_predictions_rescored"
      ? "Archived specialist"
      : "Reproduced specialist";
  if (r.model === "canonical-posterior") return "Post-hoc mathematical audit";
  if (r.model === "canonical-mle") return "Frozen mathematical reference";
  if (r.benchmark_id === "N05") return "Deterministic correctness";
  return "Conventional baseline";
}
function best(rs) {
  const vs = rs.filter(valid);
  return vs.sort(
    (a, b) => (b.score - a.score) * (a.direction === "lower" ? -1 : 1),
  )[0];
}
function primary(id, sid) {
  const ref = summary.reference_envelopes.find(
    (r) => r.benchmark_id === id && r.slice_id === sid,
  );
  return (
    ref && rowsFor(id).find((r) => r.slice_id === sid && r.model === ref.model)
  );
}
function comparisons(id, sid) {
  const rs = rowsFor(id).filter((r) => r.slice_id === sid),
    specialists = rs.filter((r) => isSpecialist(r) && valid(r)),
    available = rs.filter((r) => !MODELS.includes(r.model) && valid(r)),
    specialist = best(specialists),
    reference = specialist || primary(id, sid) || best(available);
  return { rs, specialists, specialist, reference, frozen: primary(id, sid) };
}
function brief(id) {
  const ss = [
      ...new Set(
        rowsFor(id)
          .filter((r) => MODELS.includes(r.model))
          .map((r) => r.slice_id),
      ),
    ],
    rs = [];
  for (const model of MODELS) {
    const a = rowsFor(id).filter((r) => r.model === model && valid(r));
    if (a.length && (!comparisonActive || a.length === ss.length))
      rs.push({
        ...a[0],
        score: a.reduce((s, r) => s + r.score, 0) / a.length,
        line_limit_compliant: a.every((r) => r.line_limit_compliant !== false),
      });
  }
  const refs = ss.map((s) => comparisons(id, s).reference).filter(valid);
  return {
    models: rs,
    bestModel: best(rs),
    reference: refs.length
      ? {
          ...refs[0],
          score: refs.reduce((s, r) => s + r.score, 0) / refs.length,
          display_name:
            refs.length > 1 && new Set(refs.map((r) => r.model)).size > 1
              ? "Slice-equal inspected reference envelope"
              : refs[0].display_name,
        }
      : null,
    nSlices: ss.length,
  };
}
function sidebar(family = "") {
  const counts = Object.fromEntries(
    catalog.families.map((f) => [
      f.code,
      catalog.entries.filter((e) => e.family_code === f.code && measured(e.id))
        .length,
    ]),
  );
  $("#sidebar").innerHTML =
    `<p class="side-label">Benchmark categories</p>${route("", '<span>All measured benchmarks</span><span class="count">' + summary.measured_tasks + "</span>", "side-link " + (!family ? "active" : ""))}${catalog.families.map((f) => route("category/" + f.code, `<span>${esc(CATEGORIES[f.code] || f.name)}</span><span class="count">${counts[f.code]}</span>`, "side-link " + (family === f.code ? "active" : ""))).join("")}<div class="side-note">Counts show tasks with model attempts. Each task has its own protocol and native metric.<br><br>${route("excluded", "Archived & excluded candidates →")}<br>${link(GH, "Source & audit trail")}</div>`;
}
function draw() {
  let p = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  if (p[0] === "task")
    p = ["benchmark", p[1], p[2] === "procedure" ? "evaluation" : p[2]];
  if (p[0] === "family") p = ["category", p[1]];
  if (p[0] === "trends") p = ["analysis"];
  let fam = p[0] === "category" ? p[1] : p[0] === "benchmark" ? p[1]?.[0] : "";
  sidebar(fam);
  document
    .querySelectorAll("[data-nav]")
    .forEach((a) =>
      a.classList.toggle(
        "active",
        a.dataset.nav ===
          (["models", "model"].includes(p[0])
            ? "models"
            : ["analysis", "methods"].includes(p[0])
              ? p[0]
              : "benchmarks"),
      ),
    );
  if (p[0] === "benchmark") benchmark(p[1], p[2] || "results");
  else if (p[0] === "models") modelsPage();
  else if (p[0] === "model") modelsPage(p[1]);
  else if (p[0] === "analysis" && p[1] === "specialists") specialistFrontierPage();
  else if (p[0] === "analysis" && p[1] === "lags") generationLagsPage();
  else if (p[0] === "analysis" && p[1] === "patterns") generationPatternsPage();
  else if (p[0] === "analysis" && p[1] === "practical") practicalReviewPage();
  else if (p[0] === "analysis" && p[1] === "report") macroReportPage();
  else if (p[0] === "analysis") analysisPage();
  else if (p[0] === "methods") methodsPage();
  else if (p[0] === "excluded") excludedPage();
  else explorer(p[0] === "category" ? p[1] : "");
}
function mobileFilter(fam) {
  return `<div class="mobile-filter"><label class="screen-reader" for="mobile-category">Category</label><select id="mobile-category"><option value="">All categories</option>${catalog.families.map((f) => `<option value="${f.code}" ${fam === f.code ? "selected" : ""}>${esc(CATEGORIES[f.code] || f.name)}</option>`).join("")}</select></div>`;
}
function categoryOptions(selected) {
  return catalog.families.map((family) => `<option value="${family.code}" ${family.code === selected ? "selected" : ""}>${esc(CATEGORIES[family.code] || family.name)}</option>`).join("");
}
function categoryTasks(family, measuredOnly = false) {
  return catalog.entries.filter((entry) => entry.family_code === family && (!measuredOnly || measured(entry.id)));
}
function taskOptions(entries, selected, placeholder = false) {
  return (placeholder ? '<option value="">Choose a benchmark…</option>' : '') + entries.map((entry) => `<option value="${entry.id}" ${entry.id === selected ? "selected" : ""}>${entry.id} · ${esc(title(entry))}</option>`).join("");
}
function detailJumpMarkup(family, id) {
  return `<div class="toolbar benchmark-jump" aria-label="Jump to a benchmark"><label>Category <select id="detail-category-picker">${categoryOptions(family)}</select></label><label>Benchmark <select id="detail-benchmark-picker">${taskOptions(categoryTasks(family), id, true)}</select></label></div>`;
}
function bindDetailJump(tab) {
  $("#detail-category-picker").onchange = (event) => {
    $("#detail-jump").innerHTML = detailJumpMarkup(event.target.value, "");
    bindDetailJump(tab);
  };
  $("#detail-benchmark-picker").onchange = (event) => {
    if (event.target.value) location.hash = "#/benchmark/" + event.target.value + "/" + (["evaluation", "sources"].includes(tab) ? tab : "results");
  };
}
function explorer(fam = "") {
  const f = catalog.families.find((f) => f.code === fam),
    es = catalog.entries.filter((e) => !fam || e.family_code === fam),
    selectedCategory = fam || catalog.entries.find((entry) => entry.id === selectedTask)?.family_code || catalog.families[0].code,
    scored = categoryTasks(selectedCategory, true).filter(e=>facetMatches(e.id,false)),
    choices = (listMode === "measured" ? scored : categoryTasks(selectedCategory).filter(e=>facetMatches(e.id,false)));
  if (choices.length && !choices.some((entry) => entry.id === selectedTask)) selectedTask = choices[0].id;
  $("#app").innerHTML =
    `<p class="eyebrow">General models × specialist methods</p><h1>${f ? esc(CATEGORIES[fam] || f.name) : "Neuroscience direct inference"}</h1><p class="lede">${f ? esc(f.tasks) : "Models receive task inputs and return predictions directly. Compare retained native scores with verified task-specific reference predictions. No general model writes or fits a task-specific model."}</p>${!fam ? `<p class="note">Choose a category, then a benchmark. ${route("analysis/practical", "Task changes & measured references →")} ${route("analysis/report", "Cross-benchmark findings →")}</p>` : ""}${!fam ? `<div class="stats"><div class="stat"><strong>${summary.measured_tasks}</strong><span>tasks with model attempts</span></div><div class="stat"><strong>${summary.measured_families} / ${catalog.families.length}</strong><span>categories represented</span></div><div class="stat"><strong>${MODELS.length}</strong><span>general models evaluated</span></div><div class="stat"><strong>${summary.model_attempts}</strong><span>model × task attempts</span></div></div>` : ""}${facetToolbar(es.filter(e=>listMode === "all" || measured(e.id)).map(e=>e.id))}${choices.length ? `<div class="toolbar benchmark-jump" aria-label="Explore by category and benchmark"><label>Category <select id="category-picker">${categoryOptions(selectedCategory)}</select></label><label>Benchmark <select id="benchmark-picker">${taskOptions(choices, selectedTask)}</select></label>${route("benchmark/" + selectedTask, "Open benchmark →", "button secondary")}</div>${fam ? '<div id="featured-chart"></div>' : ""}` : `<div class="toolbar benchmark-jump"><label>Category <select id="category-picker">${categoryOptions(selectedCategory)}</select></label><label>Benchmark <select disabled aria-label="Benchmark"><option>No matches in this category</option></select></label></div><p class="note">No matching benchmarks in this category. Choose another category or clear the filters.</p>`}<div class="section-head"><h2>${f ? "Benchmarks in this category" : "Explore benchmark categories"}</h2><span class="small">Native scores · no mixed-metric ranking</span></div><div class="toolbar"><input id="search" class="search" aria-label="Search benchmarks" placeholder="Search tasks, datasets or methods…" value="${esc(query)}"><select id="list-mode" aria-label="Result availability"><option value="measured" ${listMode === "measured" ? "selected" : ""}>Measured results</option><option value="all" ${listMode === "all" ? "selected" : ""}>All active candidates</option></select><a class="download-link" href="data/${comparisonActive ? "comparison-measurements.jsonl" : "measurements.csv"}" download>Download results ↓</a></div><div id="benchmark-directory"></div><p class="small" style="margin-top:17px">Ten tasks have complete four-model panels; C06 is incomplete. A published task score is conditional on its frozen slice and procedure. ${comparisonActive ? "Directory scores use the current retained comparison results, including documented repairs." : "Directory scores use each task’s first submission."}  The highest inspected reference score does not establish current global SOTA. ${route("methods", "Read the methodology →")}</p>`;
  bindFacetToolbar(()=>explorer(fam));
  if ($("#mobile-category"))
    $("#mobile-category").onchange = (e) => {
      location.hash = e.target.value ? "#/category/" + e.target.value : "#/";
    };
  if ($("#category-picker")) $("#category-picker").onchange = (event) => {
    const entries = categoryTasks(event.target.value, true);
    selectedTask = (entries[0] || categoryTasks(event.target.value)[0])?.id || "";
    selectedSlice = "";
    if (fam) location.hash = "#/category/" + event.target.value;
    else explorer("");
  };
  if ($("#benchmark-picker"))
    $("#benchmark-picker").onchange = (e) => {
      selectedTask = e.target.value;
      selectedSlice = "";
      explorer(fam);
    };
  $("#search").oninput = (e) => {
    query = e.target.value;
    directory(es, !fam);
  };
  $("#list-mode").onchange = (e) => {
    listMode = e.target.value;
    explorer(fam);
  };
  directory(es, !fam);
  if (fam && scored.some(e=>e.id===selectedTask)) renderChart("#featured-chart", selectedTask, true);
}
function directory(es, grouped = false) {
  const q = query.toLowerCase(),
    filtered = es.filter(
      (e) =>
        facetMatches(e.id,false) && (listMode === "all" || measured(e.id)) &&
        (!q ||
          JSON.stringify([
            e.id,
            title(e),
            DATASETS[e.id],
            e.resource,
            e.data,
            e.specialist_baselines,
          ])
            .toLowerCase()
            .includes(q)),
    );
  if (grouped) {
    const families = catalog.families.filter((family) => filtered.some((entry) => entry.family_code === family.code));
    $("#benchmark-directory").innerHTML = `<div class="category-grid">${families.map((family) => {
      const entries = filtered.filter((entry) => entry.family_code === family.code);
      return `<section class="category-card" aria-labelledby="category-title-${family.code}"><div class="category-card-head"><h3 id="category-title-${family.code}">${route("category/" + family.code, esc(CATEGORIES[family.code] || family.name))}</h3><span class="count">${entries.length}</span></div><p class="small">${esc(family.tasks)}</p><label class="category-task-label" for="category-task-${family.code}">Open a benchmark</label><select id="category-task-${family.code}" aria-label="Benchmark in ${esc(CATEGORIES[family.code] || family.name)}">${taskOptions(entries, "", true)}</select><details class="category-task-details"><summary>Browse task names</summary><ul class="category-task-list">${entries.map((entry) => {
        const result = brief(entry.id).bestModel;
        return `<li>${route("benchmark/" + entry.id, `<span class="task-id">${entry.id}</span>${esc(title(entry))}`)}<span class="small">${result ? esc(metricLabel(result.metric)) : "Candidate · not run"}</span></li>`;
      }).join("")}</ul></details></section>`;
    }).join("")}</div>${families.length ? "" : '<p class="empty">No matching benchmarks. Try another search or result-availability filter.</p>'}`;
    for (const family of families) $("#category-task-" + family.code).onchange = (event) => {
      if (event.target.value) location.hash = "#/benchmark/" + event.target.value + "/results";
    };
    return;
  }
  $("#benchmark-directory").innerHTML =
    `<div class="table-panel table-wrap"><table><thead><tr><th>Benchmark / dataset</th><th>Category</th><th>Best measured general model</th><th>Tested reference</th><th>Metric</th></tr></thead><tbody>${
      filtered
        .map((e) => {
          const b = brief(e.id);
          return `<tr><td>${route("benchmark/" + e.id, esc(title(e)), "bench-name")}<span class="bench-sub">${e.id} · ${esc(DATASETS[e.id] || e.resource)}</span></td><td><span class="small">${esc(CATEGORIES[e.family_code])}</span></td><td>${b.bestModel ? `<span class="number">${fmt(b.bestModel.score)}</span><span class="score-caption">${label(b.bestModel.model)}${b.bestModel.line_limit_compliant === false ? " †" : ""}${b.nSlices > 1 ? " · mean of " + b.nSlices + " slices" : ""}</span>` : '<span class="badge">Not run</span>'}</td><td>${b.reference ? `<span class="number">${fmt(b.reference.score)}</span><span class="score-caption">${esc(methodName(b.reference))}${isSpecialist(b.reference) ? "" : " · baseline/reference"}</span>` : '<span class="small">Unverified</span>'}</td><td>${b.bestModel ? `<span class="small">${esc(metricLabel(b.bestModel.metric))} ${b.bestModel.direction === "higher" ? "↑" : "↓"}</span>` : "—"}</td></tr>`;
        })
        .join("") ||
      '<tr><td colspan="5" class="empty">No matching benchmarks. Try another category or result-availability filter.</td></tr>'
    }</tbody></table></div>`;
}
function referenceSelection(c) {
  const selected = [];
  const add = (r) => {
    if (r && !selected.some((v) => v.model === r.model)) selected.push(r);
  };
  add(c.reference);
  add(c.frozen);
  if (c.rs.some((r) => r.benchmark_id === "B07")) add(c.rs.find((r) => r.model === "delta-blosc-zstd"));
  const baseline = c.rs.find((r) => r.model === "task-baseline") || c.rs.find((r) => r.benchmark_id === "L06" && r.model === "laplace");
  if (valid(baseline)) add(baseline);
  if (showAllRefs)
    for (const r of c.rs)
      if (!MODELS.includes(r.model) && !r.model.startsWith("vassi-run-"))
        add(r);
  return selected;
}
function calciumCountError(row) {
  const cells = row.cell_results;
  if (!Array.isArray(cells) || !cells.length || cells.some((cell) => !cell.animal || !Number.isFinite(cell.relative_error))) return undefined;
  const animals = [...new Set(cells.map((cell) => cell.animal))];
  return animals.reduce((total, animal) => {
    const values = cells.filter((cell) => cell.animal === animal).map((cell) => cell.relative_error);
    return total + values.reduce((a, b) => a + b, 0) / values.length;
  }, 0) / animals.length;
}
function renderChart(target, id, compact = false) {
  const e = catalog.entries.find((e) => e.id === id),
    all = rowsFor(id),
    slices = [
      ...new Set(
        all.filter((r) => MODELS.includes(r.model)).map((r) => r.slice_id),
      ),
    ];
  if (!slices.includes(selectedSlice)) selectedSlice = slices[0];
  let c = comparisons(id, selectedSlice);
  if (id === "B01" && b01Metric === "all-event-f1") {
    const convert = (r) =>
      r
        ? {
            ...r,
            score: r.posthoc_secondary_metrics?.all_event_f1,
            metric: "All-output event F1 (post-hoc)",
            direction: "higher",
          }
        : r;
    c = {
      ...c,
      rs: c.rs.map(convert),
      specialists: c.specialists.map(convert),
      specialist: convert(c.specialist),
      reference: convert(c.reference),
      frozen: convert(c.frozen),
    };
  }
  if (id === "L06") {
    const convert = (r) => {
      if (!r) return r;
      const per = l06Metric === "sliced-w2" ? r.per_observation_sliced_w2 : r.per_unit;
      const score = l06Observation === "mean" ? (l06Metric === "sliced-w2" ? r.sliced_w2 : r.score) : per?.[Number(l06Observation)];
      return { ...r, score, metric: l06Metric === "sliced-w2" ? "Prior-whitened sliced Wasserstein-2" : "Classifier accuracy · chance target 0.5", direction: "lower" };
    };
    c = { ...c, rs: c.rs.map(convert), specialists: c.specialists.map(convert), specialist: convert(c.specialist), reference: convert(c.reference), frozen: convert(c.frozen) };
  }
  if (id === "C06" && c06Metric === "relative-error") {
    const convert = (r) => r ? { ...r, score: calciumCountError(r), metric: "Animal-equal neuron relative count error · predeclared secondary", direction: "lower" } : r;
    c = { ...c, rs: c.rs.map(convert), specialists: c.specialists.map(convert), specialist: convert(c.specialist), reference: convert(c.reference), frozen: convert(c.frozen) };
  }
  const native = c.rs.find(valid);
  if (!native) {
    $(target).innerHTML =
      '<p class="empty">No valid measurements for this slice.</p>';
    return;
  }
  const refs = showReferences ? referenceSelection(c) : [],
    generals = MODELS.filter((m) => !hiddenModels.has(m)).map(
      (m) => c.rs.find((r) => r.model === m) || { model: m, status: "missing" },
    );
  $(target).innerHTML =
    `<div class="chart-card"><div class="chart-head"><div><h2>${compact ? route("benchmark/" + id, esc(title(e))) : esc(title(e))}</h2><p class="small">${esc(metricLabel(native.metric))} · ${native.direction === "higher" ? "higher" : "lower"} is better · ${id}</p></div><div class="segmented" role="group" aria-label="Chart or table"><button data-view="graph" class="${plotView === "graph" ? "active" : ""}">Graph</button><button data-view="table" class="${plotView === "table" ? "active" : ""}">Table</button></div></div><div class="plot-controls">${id === "L06" ? `<label>Posterior metric <select id="metric-picker"><option value="c2st" ${l06Metric === "c2st" ? "selected" : ""}>Primary · classifier accuracy (target 0.5)</option><option value="sliced-w2" ${l06Metric === "sliced-w2" ? "selected" : ""}>Secondary · sliced Wasserstein-2</option></select></label><label>Observation <select id="observation-picker"><option value="mean" ${l06Observation === "mean" ? "selected" : ""}>Mean of all ten</option>${Array.from({length:10},(_,i)=>`<option value="${i}" ${l06Observation === String(i) ? "selected" : ""}>Observation ${i+1}</option>`).join("")}</select></label>` : ""}${false ? `<label>Calcium metric <select id="metric-picker"><option value="primary" ${c06Metric === "primary" ? "selected" : ""}>Primary · animal-equal Pearson correlation</option><option value="relative-error" ${c06Metric === "relative-error" ? "selected" : ""}>Secondary · relative count error</option></select></label>` : ""}${id === "B01" ? `<label>Plot metric <select id="metric-picker"><option value="primary" ${b01Metric === "primary" ? "selected" : ""}>Frozen mean GT-unit accuracy</option><option value="all-event-f1" ${b01Metric === "all-event-f1" ? "selected" : ""}>All-output event F1 · post-hoc</option></select></label>` : ""}<label>Evaluation slice <select id="slice-picker">${slices.map((s) => `<option value="${s}" ${s === selectedSlice ? "selected" : ""}>${id === "C05" ? "Preparation " + s : id === "E06" ? (s === "taxis" ? "Unseen taxis stimulus · dependent slice" : "Seen-stimulus temporal forecast") : s}</option>`).join("")}</select></label><label><input id="show-ref" type="checkbox" ${showReferences ? "checked" : ""}>Include references</label><label><input id="all-ref" type="checkbox" ${showAllRefs ? "checked" : ""}>Show additional references</label>${plotView === "graph" ? `<label class="right"><input id="zero-axis" type="checkbox" ${startAtZero ? "checked" : ""}>Line axis starts at zero</label>` : ""}</div>${plotView === "graph" ? `${referenceCards(refs, c.frozen)}<p class="plot-reading-key"><span class="solid-key"></span>Solid connected points = general models. <span class="dashed-key"></span>Dashed horizontal lines = specialists or domain references. <span class="dotted-key"></span>Dotted lines = other references.</p><div class="chart-grid"><section><p class="chart-label">Performance across model versions</p>${linePlot(generals, refs, native.direction, c.specialists)}</section><section><p class="chart-label">General models and named references</p>${barPlot([...generals, ...refs], native.direction)}</section></div><div class="legend">${MODELS.map((m) => `<label><input type="checkbox" data-model="${m}" ${!hiddenModels.has(m) ? "checked" : ""}><i class="dot" style="background:${COLORS[m]}"></i>${label(m)}</label>`).join("")}${refs.map((r, i) => `<span><i class="dash" style="border-color:${refColor(r, i)}"></i>${esc(methodName(r))} · ${fmt(r.score)}</span>`).join("")}</div>` : `<div class="table-wrap">${scoreTable(c.rs)}</div>`}<div class="chart-foot">${chartCaveat(id, c)} ${compact ? route("benchmark/" + id, "Inspect protocol, sources and all scores →") : ""}<br>Connected points show version order, not elapsed time or a compute scaling law. Line axes ${startAtZero ? "include zero" : "adapt to the score range; inspect the ticks"}; bars include zero. ${comparisonActive ? "Final retained results: repairs are identified in provenance; API and Codex inference contexts differ." : "First-submission panel: one generated program per model/task."}${id === "H02" ? " " + route("benchmark/H02/replication", "Inspect three-generation follow-up →") : ""}</div></div>`;
  $(target)
    .querySelectorAll?.("[data-view]")
    .forEach(
      (b) =>
        (b.onclick = () => {
          plotView = b.dataset.view;
          renderChart(target, id, compact);
        }),
    );
  if ($("#metric-picker"))
    $("#metric-picker").onchange = (ev) => {
      if (id === "L06") l06Metric = ev.target.value;
      else if (id === "C06") c06Metric = ev.target.value;
      else b01Metric = ev.target.value;
      renderChart(target, id, compact);
    };
  if (id === "L06") $("#observation-picker").onchange = (ev) => {
    l06Observation = ev.target.value;
    renderChart(target, id, compact);
  };
  $("#slice-picker").onchange = (ev) => {
    selectedSlice = ev.target.value;
    renderChart(target, id, compact);
  };
  $("#show-ref").onchange = (ev) => {
    showReferences = ev.target.checked;
    renderChart(target, id, compact);
  };
  $("#all-ref").onchange = (ev) => {
    showAllRefs = ev.target.checked;
    renderChart(target, id, compact);
  };
  if ($("#zero-axis"))
    $("#zero-axis").onchange = (ev) => {
      startAtZero = ev.target.checked;
      renderChart(target, id, compact);
    };
  document.querySelectorAll("[data-model]").forEach(
    (b) =>
      (b.onchange = () => {
        b.checked
          ? hiddenModels.delete(b.dataset.model)
          : hiddenModels.add(b.dataset.model);
        renderChart(target, id, compact);
      }),
  );
}
function refColor(r, i = 0) {
  return (isSpecialist(r) || isDomainReference(r))
    ? ["#24796d", "#5f9e75", "#688c5e", "#4b806b"][i % 4]
    : r.model === "canonical-posterior"
      ? "#8e6ab0"
      : "#8a939c";
}
function referenceCards(refs, frozen) {
  if (!refs.length)
    return '<p class="reference-empty">No reference lines are shown.</p>';
  return `<div class="reference-strip" aria-label="Named reference scores">${refs
    .filter(valid)
    .map(
      (r, i) =>
        `<div class="reference-card ${isSpecialist(r) ? "specialist" : "baseline"}"><div class="reference-kicker"><span class="reference-key" style="color:${refColor(r, i)}">R${i + 1} · ${r.benchmark_id === "B07" && isSpecialist(r) ? "Codec reference · dashed line" : isDomainReference(r) ? "Domain reference · dashed line" : isSpecialist(r) ? "Specialist · dashed line" : "Other reference · dotted line"}</span>${r.model === frozen?.model ? '<span class="reference-policy">Primary comparator</span>' : ""}</div><div class="reference-value"><span>${esc(methodName(r))}</span><strong>${fmt(r.score)}</strong></div><span class="reference-policy">${esc(evidence(r))}</span></div>`,
    )
    .join("")}</div>`;
}
function notScoredLabel(row) {
  if (row.not_scored_reason) return row.not_scored_reason;
  if (!MODELS.includes(row.model) && !HISTORICAL_MODELS.includes(row.model)) return 'Reference output unavailable from archive';
  return /exceeded|timed out/i.test(row.reason || '') ? 'Not scored within computation limit' : 'Not scored under task requirements';
}
function linePlot(general, refs, direction, specialists = [], zeroAxis = startAtZero, modelOrder = MODELS) {
  let vals = [...general, ...refs].filter(valid).map((r) => r.score);
  if (showReferences)
    vals.push(
      ...specialists
        .filter((r) => r.model.startsWith("vassi-run-"))
        .map((r) => r.score),
    );
  if (!vals.length) return '<p class="empty">No finite scores.</p>';
  const shown = refs.filter(valid),
    plotHeight = Math.max(190, shown.length * 38 + 15),
    top = 40,
    bottom = top + plotHeight;
  let lo = Math.min(...vals),
    hi = Math.max(...vals),
    padding = Math.max((hi - lo) * 0.16, Math.abs(hi) * 0.025, 1e-6);
  lo = zeroAxis ? Math.min(0, lo - padding) : lo - padding;
  hi += padding;
  if (direction === "lower" && vals.every(v => v >= 0)) lo = Math.max(0, lo);
  const x = (i) => 88 + (250 / Math.max(1, modelOrder.length - 1)) * i,
    y = (v) => direction === 'lower' ? top + ((v - lo) / (hi - lo)) * plotHeight : bottom - ((v - lo) / (hi - lo)) * plotHeight;
  const labels = shown
    .map((r, i) => ({ r, i, ideal: y(r.score), position: y(r.score) }))
    .sort((a, b) => a.ideal - b.ideal);
  for (let i = 0; i < labels.length; i++)
    labels[i].position = Math.max(
      top + 10,
      labels[i].ideal,
      i ? labels[i - 1].position + 38 : top + 10,
    );
  if (labels.length && labels.at(-1).position > bottom - 10) {
    labels.at(-1).position = bottom - 10;
    for (let i = labels.length - 2; i >= 0; i--)
      labels[i].position = Math.min(
        labels[i].position,
        labels[i + 1].position - 38,
      );
  }
  const labelPosition = new Map(labels.map((v) => [v.i, v.position]));
  let path = "",
    prior = false;
  for (const r of general) {
    if (valid(r)) {
      path +=
        (prior ? " L" : " M") + x(modelOrder.indexOf(r.model)) + " " + y(r.score);
      prior = true;
    } else prior = false;
  }
  const archives = specialists.filter((r) => r.model.startsWith("vassi-run-"));
  return `<p class="small metric-direction-key"> Better performance ↑ · ${direction === "lower" ? "lower native score is better; vertical axis reversed" : "higher native score is better"}</p><svg class="plot line-plot" viewBox="0 0 570 ${bottom + 68}" role="img" aria-label="Model-version line chart with named specialist reference lines"><title>Solid connected points: general model scores. Horizontal dashed lines: specialists. Dotted lines: other references. ${direction} is better. Better scores are higher on the page; lower-is-better axes are reversed.</title>${[
    0, 0.25, 0.5, 0.75, 1,
  ]
    .map((t) => {
      const v = lo + t * (hi - lo);
      return `<line x1="65" x2="365" y1="${y(v)}" y2="${y(v)}" stroke="#e5ebef"/><text x="56" y="${y(v) + 4}" text-anchor="end">${fmt(v)}</text>`;
    })
    .join(
      "",
    )}${archives.length > 1 && showReferences ? `<rect x="65" width="300" y="${y(Math.max(...archives.map((r) => r.score)))}" height="${Math.abs(y(Math.min(...archives.map((r) => r.score))) - y(Math.max(...archives.map((r) => r.score))))}" fill="#24796d" opacity=".12"><title>Range of 20 archived VASSI runs; not independent tasks</title></rect>` : ""}${shown
    .map((r, i) => {
      const yy = y(r.score),
        ly = labelPosition.get(i),
        name = methodName(r),
        short = name.length > 24 ? name.slice(0, 23) + "…" : name;
      return `<g class="direct-reference-label"><line x1="65" x2="365" y1="${yy}" y2="${yy}" stroke="${refColor(r, i)}" stroke-width="2" stroke-dasharray="${(isSpecialist(r) || isDomainReference(r)) ? "7 4" : "2 5"}"/><path d="M365 ${yy} L376 ${yy} L389 ${ly}" fill="none" stroke="${refColor(r, i)}" stroke-width="1"/><text x="395" y="${ly - 4}" class="reference-label-name" style="fill:${refColor(r, i)}">R${i + 1} · ${esc(short)}</text><text x="395" y="${ly + 10}" class="reference-label-score">${fmt(r.score)} · ${isDomainReference(r) ? "domain reference" : r.benchmark_id === "B07" && isSpecialist(r) ? "codec reference" : isSpecialist(r) ? "specialist" : "other reference"}</text><title>R${i + 1}: ${esc(name)}, ${fmt(r.score)}. ${evidence(r)}</title></g>`;
    })
    .join(
      "",
    )}<path d="${path}" fill="none" stroke="#547b97" stroke-width="2"/>${general
    .map((r) => {
      const xx = x(modelOrder.indexOf(r.model));
      return `${valid(r) && Number.isFinite(r.range_min) ? `<g class="generation-range"><line x1="${xx}" x2="${xx}" y1="${y(r.range_min)}" y2="${y(r.range_max)}" stroke="${COLORS[r.model]}" stroke-width="2"/><path d="M${xx-6} ${y(r.range_min)}h12 M${xx-6} ${y(r.range_max)}h12" stroke="${COLORS[r.model]}"/><title>${label(r.model)} generation range ${fmt(r.range_min)} to ${fmt(r.range_max)}; not a confidence interval</title></g>` : ""}${valid(r) ? `<circle cx="${xx}" cy="${y(r.score)}" r="5.5" fill="${COLORS[r.model]}"><title>${label(r.model)}: ${fmt(r.score)}</title></circle><text class="value-label" x="${xx}" y="${y((direction === "lower" ? r.range_min : r.range_max) ?? r.score) - 13}" text-anchor="middle">${fmt(r.score)}${r.line_limit_compliant === false ? "†" : ""}${r.repair_applied ? " *" : ""}</text>` : `<text x="${xx}" y="${top + plotHeight / 2}" text-anchor="middle">Not scored<title>${esc(notScoredLabel(r))}</title></text>`}<text x="${xx}" y="${bottom + 29}" text-anchor="middle">${label(r.model).replace("GPT-", "")}</text>`;
    })
    .join(
      "",
    )}<text x="215" y="${bottom + 58}" text-anchor="middle">General model version</text></svg>`;
}
function barPlot(rs, direction) {
  const vals = rs.filter(valid).flatMap((r) => [r.score,r.range_min,r.range_max].filter(Number.isFinite));
  let lo = Math.min(0, ...vals),
    hi = Math.max(0, ...vals);
  if (hi === lo) hi = lo + 1;
  const scale = (v) => 195 + ((v - lo) / (hi - lo)) * 300,
    zero = scale(0),
    height = rs.length * 42 + 50;
  const ticks = [...new Set([lo, (lo + hi) / 2, 0, hi])].sort((a, b) => a - b);
  return `<p class="small metric-direction-key"> Raw native scores · ${direction === "lower" ? "lower is better" : "higher is better"}; read the values rather than bar length.</p><svg class="plot" viewBox="0 0 570 ${height}" role="img" aria-label="Bar chart including general models and named specialist or baseline scores"><title>Native metric; ${direction} is better. Bar axis includes zero.</title>${ticks
    .map((v) => {
      return `<line x1="${scale(v)}" x2="${scale(v)}" y1="5" y2="${height - 32}" stroke="${v === 0 ? "#b5c2cc" : "#e9edf0"}"/><text x="${scale(v)}" y="${height - 10}" text-anchor="middle">${fmt(v)}</text>`;
    })
    .join("")}${rs
    .map((r, i) => {
      const yy = 12 + i * 42;
      return `<text x="181" y="${yy + 15}" text-anchor="end">${esc(methodName(r))}${r.line_limit_compliant === false ? "†" : ""}${r.repair_applied ? " *" : ""}</text>${valid(r) ? `<rect x="${Math.min(zero, scale(r.score))}" y="${yy}" width="${Math.max(0.8, Math.abs(scale(r.score) - zero))}" height="23" fill="${COLORS[r.model] || refColor(r, i)}"><title>${esc(methodName(r))}: ${fmt(r.score)} · ${evidence(r)}</title></rect>${Number.isFinite(r.range_min) ? `<g class="generation-range"><line x1="${scale(r.range_min)}" x2="${scale(r.range_max)}" y1="${yy+12}" y2="${yy+12}" stroke="#233c50" stroke-width="2"/><path d="M${scale(r.range_min)} ${yy+7}v10 M${scale(r.range_max)} ${yy+7}v10" stroke="#233c50"/><title>Generation range ${fmt(r.range_min)} to ${fmt(r.range_max)}; not a confidence interval</title></g>` : ""}<text class="value-label" x="560" y="${yy + 15}" text-anchor="end">${fmt(r.score)}</text>` : `<text x="360" y="${yy + 15}">Not scored<title>${esc(notScoredLabel(r))}</title></text>`}`;
    })
    .join("")}</svg>`;
}
function chartCaveat(id){const t=direct.tasks.find(t=>t.id===id);return esc(t.notes.join(' '));}
function scoreTable(rs){return `<table><thead><tr><th>Model / reference</th><th>Native score</th><th>Direction</th><th>Coverage</th><th>Evidence</th></tr></thead><tbody>${rs.map(r=>`<tr><td>${esc(methodName(r))}</td><td>${fmt(r.score)}</td><td>${esc(r.direction)} is better</td><td>${MODELS.includes(r.model)?`${r.n_valid_predictions} / ${r.n_expected}`:'Rescored reference'}</td><td>${esc(evidence(r))}</td></tr>`).join('')}</tbody></table>`;}
function benchmark(id,tab='results'){
 const e=catalog.entries.find(e=>e.id===id),t=direct.tasks.find(t=>t.id===id);if(!e){$('#app').innerHTML='<h1>Benchmark unavailable</h1>';return;}
 $('#app').innerHTML=`<div id="detail-jump">${detailJumpMarkup(e.family_code,id)}</div><p class="breadcrumb">${route('','Benchmarks')} / ${route('category/'+e.family_code,esc(CATEGORIES[e.family_code]))} / ${id}</p><p class="eyebrow">${id} · ${esc(CATEGORIES[e.family_code])}</p><h1>${esc(t.title)}</h1><p class="lede">${esc(t.input)} · ${esc(t.test_units)}</p><div class="detail-top"><span class="badge verified">Direct inference</span><span class="badge">${esc(t.condition)}</span><span class="badge">${t.complete_all_four?'Complete four-model panel':'Incomplete panel · excluded from macro tables'}</span></div>${facetBadges(id)}<nav class="tabs">${[['results','Results'],['evaluation','Evaluation details'],['sources','Data & sources']].map(([v,n])=>route('benchmark/'+id+'/'+v,n,tab===v?'active':'')).join('')}</nav><div id="detail-chart"></div><div id="benchmark-content"></div>`;
 bindDetailJump(tab);
 if(tab==='results'){renderChart('#detail-chart',id);$('#benchmark-content').innerHTML=`<div class="table-wrap">${scoreTable(rowsFor(id))}</div><details open><summary>What can this result establish?</summary><p>${esc(t.notes.join(' '))}</p><p>Direct predictions, no model-generated solver or local model fitting. Public-data contamination and provider identity remain unverified. Reference training, calibration and input access can differ. Missing results are unknown, not zero.</p></details>`;}
 else $('#benchmark-content').innerHTML=`<div class="doc-grid"><section class="doc-panel"><h2>${tab==='sources'?'Sources & provenance':'Evaluation contract'}</h2><dl class="kv"><dt>Input</dt><dd>${esc(t.input)}</dd><dt>Test</dt><dd>${esc(t.test_units)}</dd><dt>Metric</dt><dd>${esc(t.metric_label)} · ${t.rows[0].direction} is better</dd><dt>Condition</dt><dd>${esc(t.condition)}</dd></dl><div class="link-list">${link(t.source,'Frozen protocol and run report')}${e.source_urls.map(u=>link(u,esc(u))).join('')}${link(GH+'/blob/main/results/reference-validation.json','Reference prediction audit')}</div></section><section class="doc-panel"><h2>Validity & reference</h2><p>${esc(t.notes.join(' '))}</p><p>${esc(t.reference.name)}: ${fmt(t.reference.score)}. ${esc(t.reference.comparison_limit)}</p>${link(t.reference.source,'Reference source')}</section></div>`;
}
const analysisNav=()=>`<div class="actions">${[['analysis','Overview'],['analysis/practical','Task charts'],['analysis/patterns','Generation patterns'],['analysis/lags','Lag & IQR tables'],['analysis/specialists','Specialist comparison']].map(([p,n])=>route(p,n+' →','button secondary')).join('')}</div>`;
function analysisHeader(title){return `<p class="eyebrow">Cross-task analysis · Direct inference</p><h1>${title}</h1>${analysisNav()}<p class="note">Primary cohort: 10 complete four-model tasks across 7 categories. C06 is separately visible with missing outputs. Counts are descriptive, not significance, equivalence, randomness or a scaling law. Model transport, reasoning, context and repairs differ.</p>`;}
function selectedPatterns(){return patternData.tasks.filter(t=>facetMatches(t.benchmark_id));}
function pairTable(ts){return generationLagTable({...lagData,summaries:lagData.summaries.map(s=>{const rows=lagData.task_pairs.filter(p=>ts.some(t=>t.benchmark_id===p.benchmark_id)&&p.older===s.older&&p.newer===s.newer);return {...s,counts:Object.fromEntries(Object.keys(s.counts).map(k=>[k,rows.filter(r=>r[s.analysis]===k).length]))};})},'raw');}
function analysisPage(){const ts=selectedPatterns(),endpoint=ts.map(t=>(t.scores[MODELS[3]]-t.scores[MODELS[0]])*(t.direction==='lower'?-1:1)),better=endpoint.filter(v=>v>1e-9).length;
 $('#app').innerHTML=analysisHeader('Where do models improve?')+facetToolbar(patternData.tasks.map(t=>t.benchmark_id),true)+`<div class="stats"><div class="stat"><strong>${ts.length}</strong><span>selected complete tasks</span></div><div class="stat"><strong>${better} / ${ts.length}</strong><span>6.1 better than 4.1</span></div><div class="stat"><strong>${ts.filter(t=>t.trajectory_class==='strictly_improving').length}</strong><span>improve every step</span></div><div class="stat"><strong>${ts.filter(t=>t.trajectory_class==='mixed_reversals').length}</strong><span>mixed intermediate steps</span></div></div><section class="practical-section"><h2>Model-version changes</h2>${pairTable(ts)}</section>${referenceModelTable(ts)}${patternTable(ts)}${familyTable(ts)}<section class="doc-panel practical-section"><h2>Interpretation</h2><p>The full, unfiltered complete cohort shows endpoint progress but uneven intermediate steps. Three of ten tasks improve at every generation; four are nondecreasing if ties count. The retained task-specific reference still beats the best general score on seven of ten tasks. Only two complete tasks have an eligible specialist, and one of those favors general inference.</p><p>B03 and M04 are synthetic diagnostics. Cell-data tasks share a broad category, while several other categories have only one task. A uniform direction of endpoint change is interesting, but it does not establish a universal neuroscience scaling law or justify replacing laboratory tools.</p><p>${link(GH+'/blob/main/analysis/explorer-analysis.md','All tables, interpretation and limitations')}</p></section>`;bindFacetToolbar(analysisPage,true);}
function patternTable(ts){const names=['strictly_improving','nondecreasing_with_ties','mixed_reversals','numerically_flat','strictly_declining','nonincreasing_with_ties'];return `<section class="practical-section"><h2>Whole generation trajectories</h2><div class="table-wrap"><table><thead><tr><th>Pattern</th><th>Tasks</th><th>Which tasks?</th></tr></thead><tbody>${names.map(c=>`<tr><td>${c.replaceAll('_',' ')}</td><td>${ts.filter(t=>t.trajectory_class===c).length}</td><td>${ts.filter(t=>t.trajectory_class===c).map(t=>route('benchmark/'+t.benchmark_id,t.benchmark_id)).join(', ')||'—'}</td></tr>`).join('')}</tbody></table></div></section>`;}
function familyTable(ts){return `<section class="practical-section"><h2>By category</h2><div class="table-wrap"><table><thead><tr><th>Category</th><th>Tasks</th><th>6.1 better / worse / tie vs 4.1</th><th>Strictly improving</th></tr></thead><tbody>${catalog.families.map(f=>{const a=ts.filter(t=>t.family===f.code);if(!a.length)return '';const ds=a.map(t=>(t.scores[MODELS[3]]-t.scores[MODELS[0]])*(t.direction==='lower'?-1:1));return `<tr><td>${esc(CATEGORIES[f.code])}</td><td>${a.length}</td><td>${ds.filter(v=>v>1e-9).length} / ${ds.filter(v=>v< -1e-9).length} / ${ds.filter(v=>Math.abs(v)<=1e-9).length}</td><td>${a.filter(t=>t.trajectory_class==='strictly_improving').length}</td></tr>`;}).join('')}</tbody></table></div><p class="small">Task counts, not independent biological replications. Native differences are never averaged across incompatible metrics.</p></section>`;}
function generationPatternsPage(){const ts=selectedPatterns();$('#app').innerHTML=analysisHeader('Endpoint progress, uneven steps.')+facetToolbar(patternData.tasks.map(t=>t.benchmark_id),true)+patternTable(ts)+`<section class="practical-section"><h2>Every task’s trajectory</h2><div class="table-wrap"><table><thead><tr><th>Task</th>${MODELS.map(m=>`<th>${label(m)}</th>`).join('')}<th>Preferred direction</th><th>Steps</th><th>Pattern</th></tr></thead><tbody>${ts.map(t=>`<tr><td>${route('benchmark/'+t.benchmark_id,t.benchmark_id+' · '+esc(t.task))}</td>${MODELS.map(m=>`<td>${fmt(t.scores[m])}</td>`).join('')}<td>${t.direction}</td><td>${t.step_pattern}</td><td>${t.trajectory_class.replaceAll('_',' ')}</td></tr>`).join('')}</tbody></table></div></section>`+familyTable(ts)+`<section class="doc-panel"><h2>Quantitative and qualitative reading</h2><p><strong>Quantitative:</strong> the full, unfiltered complete cohort has 10 endpoint improvements, 3 strict stepwise improvements and 6 mixed trajectories. Raw and IQR-filtered pair comparisons show which changes survive a larger relative-gap threshold.</p><p><strong>Qualitative:</strong> segmentation remains far behind archived StarDist; compressed numerical summaries sometimes admit good direct inference. D02 is underdetermined without neuron-specific calibration. These task-level interpretations are hypotheses, not statistically established explanations.</p><p><strong>Combined:</strong> newer models help on these retained interfaces, while success depends heavily on input representation, required output precision and access to task calibration. Ten selected tasks cannot establish which factor causes improvement.</p></section>`;bindFacetToolbar(generationPatternsPage,true);}
function frontierCounts(tasks,key,mode){const c={general_better:0,specialist_better:0,numerical_tie:0,within_band:0,unavailable:0,not_estimable:0};for(const t of tasks)c[t[key]?.classes[mode]||'unavailable']++;return c;}
function frontierTable(ts,key,name){return `<section class="doc-panel practical-section"><h2>${name}</h2><p>${ts.filter(t=>t[key]).length} scored comparators / ${ts.length} selected tasks.</p><div class="table-wrap"><table><thead><tr><th>Size filter</th><th>General better</th><th>Comparator better</th><th>Tie / within band</th><th>Unavailable</th><th>Not estimable</th></tr></thead><tbody>${[['raw','Absolute/native direction'],['iqr_0.1','Gap > 0.1 IQR'],['iqr_0.5','Gap > 0.5 IQR']].map(([k,n])=>{const c=frontierCounts(ts,key,k);return `<tr><td>${n}</td><td>${c.general_better}</td><td>${c.specialist_better}</td><td>${c.numerical_tie+c.within_band}</td><td>${c.unavailable}</td><td>${c.not_estimable}</td></tr>`;}).join('')}</tbody></table></div></section>`;}
function specialistFrontierPage(){const ts=frontierData.tasks.filter(t=>facetMatches(t.benchmark_id));$('#app').innerHTML=analysisHeader('Best direct inference versus specialists')+`<p class="lede">A separate comparison using the best of four retained general-model scores on each task. “Best” is a post-hoc envelope, not a single deployable model or certified current global SOTA.</p>`+facetToolbar(frontierData.tasks.map(t=>t.benchmark_id),true)+frontierTable(ts,'best_specialist','1. Best general versus measured specialist')+frontierTable(ts,'best_available_reference','2. Context: best general versus any available reference')+`<section class="doc-panel practical-section"><h2>What counts as a specialist?</h2><p>Within this ten-task cohort, B03 has local SpikeInterface registration and J08 has author-archived StarDist predictions. C06 has OASIS but lacks a complete four-model panel and is excluded. Other retained comparators are conventional estimators, domain models or mathematical audits. They appear in the second table, not the specialist-only count. These references were rescored on identical retained targets; training and input access can differ. Current-best paper performance remains unverified.</p><h2>Absolute and relative gaps</h2><p>“Absolute/native direction” checks who has the better original score, with a 1e−9 numerical tie tolerance; it does not average incompatible absolute metrics. R = direction-adjusted (best general score − reference score) / IQR of the four general-model scores. Specialist scores do not change that IQR. Within band means |R| ≤ threshold. These post-hoc filters do not prove negligible differences, equivalence, randomness or significance.</p></section><section class="practical-section"><h2>Per-task comparisons</h2><div class="table-wrap"><table><thead><tr><th>Task</th><th>Best general</th><th>Available comparator</th><th>Native reference score</th><th>R</th><th>Absolute</th><th>0.1 IQR</th><th>0.5 IQR</th></tr></thead><tbody>${ts.map(t=>{const r=t.best_available_reference;return `<tr><td>${route('benchmark/'+t.benchmark_id,t.benchmark_id)}<span class="bench-sub">${esc(metricLabel(t.metric))} · ${t.direction} better</span></td><td>${fmt(t.best_general_score)}<span class="bench-sub">${t.best_general_models.map(label).join(' / ')}</span></td><td>${esc(r.name)}<span class="bench-sub">${t.best_specialist?'Specialist':'Other reference'}</span></td><td>${fmt(r.score)}</td><td>${fmt(r.gap_in_general_panel_iqr)}</td>${['raw','iqr_0.1','iqr_0.5'].map(k=>`<td>${r.classes[k].replace('specialist_better','comparator_better').replaceAll('_',' ')}</td>`).join('')}</tr>`;}).join('')}</tbody></table></div></section><section class="doc-panel practical-section"><h2>Interpretation</h2><p>On the full, unfiltered complete cohort, general inference beats the retained reference on B03, K05 and K06; the other seven favor their reference. Only B03 is a specialist win. Tiny K05 differences and unequal calibration/training access prevent a recommendation to switch. Inspect native differences alongside the IQR bands.</p></section><div class="actions"><a class="button secondary" href="data/specialist-frontier.json" download>Download comparison audit ↓</a>${link(GH+'/blob/main/analysis/explorer-analysis.md','All tables & methods','button secondary')}</div>`;bindFacetToolbar(specialistFrontierPage,true);}
let practicalCategory='B',practicalTask='B03';
function practicalReviewPage(){const choices=catalog.entries.filter(t=>t.family_code===practicalCategory);if(!choices.some(t=>t.id===practicalTask))practicalTask=choices[0].id;$('#app').innerHTML=analysisHeader('Inspect each task’s retained results')+`<div class="toolbar benchmark-jump"><label>Category<select id="practical-category">${categoryOptions(practicalCategory)}</select></label><label>Task detail<select id="practical-task">${taskOptions(choices,practicalTask)}</select></label></div><div id="practical-chart"></div><p>${route('benchmark/'+practicalTask,'Protocol, coverage and source audit →')}</p>`;renderChart('#practical-chart',practicalTask);$('#practical-category').onchange=e=>{practicalCategory=e.target.value;practicalReviewPage();};$('#practical-task').onchange=e=>{practicalTask=e.target.value;practicalReviewPage();};}
function macroReportPage(){analysisPage();}
function modelsPage(){ $('#app').innerHTML=`<p class="eyebrow">Evaluated models</p><h1>Four models, one retained task panel.</h1><div class="table-wrap"><table><thead><tr><th>Model</th><th>Completed / attempted</th><th>Transport</th></tr></thead><tbody>${MODELS.map(m=>`<tr><td>${label(m)}</td><td>${direct.tasks.filter(t=>t.rows.find(r=>r.model===m)?.complete).length} / 11</td><td>${m.includes('sol')?'Codex harness only':'OpenAI API'}</td></tr>`).join('')}</tbody></table></div><p class="note">No Sol model is called through the API. Different reasoning and transport contexts limit generation attribution. GPT-6 Sol is excluded from this study.</p>`;}
function methodsPage(){ $('#app').innerHTML=`<p class="eyebrow">Methods & data</p><h1>Trace every result.</h1><div class="doc-grid"><section class="doc-panel"><h2>Direct inference</h2><p>Models receive fixed numerical payloads or images and return predictions. No solver generation, tool calls or local fitting. L04 has 64 fixed in-context examples; the remaining tasks are zero-shot. Ten tasks have complete four-model panels; C06 has two complete model scores and two unscored incomplete outputs.</p><p>Frozen payload hashes, output traces, coverage and independently rescored references are retained. No old general-model code-generation scores enter this study.</p></section><section class="doc-panel"><h2>Scientific limits</h2><p>Retained custom protocols are not automatically official whole-benchmark evaluations. Small biological samples, public labels, synthetic diagnostics and unequal reference training access constrain interpretation. No uncertainty or causal scaling law is claimed. A numeric tie or IQR band is not statistical equivalence.</p></section></div><div class="link-list">${[['README.md','Main plan and status'],['analysis/explorer-analysis.md','All analysis tables and interpretation'],['analysis/generation-lags-v1/methods.md','Lag and IQR methods'],['docs/task-classification/README.md','Task filter definitions'],['results/reference-validation.json','Rescored comparator audit'],['results/primary-summary.json','Canonical primary scores'],['registry/feasibility-audit.json','Candidate decisions']].map(([p,n])=>link(GH+'/blob/main/'+p,n)).join('')}</div>`;}
function excludedPage(){ $('#app').innerHTML=`<p class="eyebrow">Coverage</p><h1>Deferred candidates</h1><p>19 original candidates remain outside the current direct-inference run. This is a selected pilot, not exhaustive coverage. Tasks are not dropped for low model scores.</p><div class="table-wrap"><table><thead><tr><th>Task</th><th>Assessment</th><th>Reason</th></tr></thead><tbody>${direct.audit.map(t=>`<tr><td>${t.id} · ${esc(t.title)}</td><td>${esc(t.assessment)}</td><td>${esc(t.reason)}</td></tr>`).join('')}</tbody></table></div>`;}
let direct,lagData,patternData,frontierData;
Promise.all(['catalog','summary','direct-inference','task-facets','generation-lags','generation-patterns','specialist-frontier'].map(n=>fetch('data/'+n+'.json').then(r=>{if(!r.ok)throw Error(n);return r.json();}))).then(async ([c,s,d,f,l,p,fr])=>{catalog=c;summary=s;direct=d;taskFacetData=f;lagData=l;generationLagData=l;patternData=p;frontierData=fr;for(const t of d.tasks){TITLES[t.id]=t.title;METRIC_LABELS[t.rows[0].metric]=t.metric_label;}records=(await (await fetch('data/measurements.jsonl')).text()).trim().split('\n').map(JSON.parse);draw();}).catch(e=>{console.error(e);$('#app').innerHTML='<h1>Results could not load</h1><p>Reload or inspect GitHub.</p>';});
window.addEventListener('hashchange',()=>{selectedSlice='';draw();window.scrollTo({top:0});});

function referenceModelTable(ts){return `<section class="practical-section"><h2>Each model versus the available reference</h2><div class="table-wrap"><table><thead><tr><th>Model</th><th>Better / worse / numerical tie</th><th>Tasks / categories</th><th>Category-equal win fraction</th></tr></thead><tbody>${MODELS.map(m=>{const rows=ts.map(t=>{const ref=direct.tasks.find(x=>x.id===t.benchmark_id).reference;return {family:t.family,delta:(t.scores[m]-ref.score)*(t.direction==='lower'?-1:1)};});const fs=[...new Set(rows.map(r=>r.family))];const fe=fs.length?fs.reduce((a,f)=>{const rs=rows.filter(r=>r.family===f);return a+rs.filter(r=>r.delta>1e-9).length/rs.length;},0)/fs.length:null;return `<tr><td>${label(m)}</td><td>${rows.filter(r=>r.delta>1e-9).length} / ${rows.filter(r=>r.delta< -1e-9).length} / ${rows.filter(r=>Math.abs(r.delta)<=1e-9).length}</td><td>${rows.length} / ${fs.length}</td><td>${fmt(fe)}</td></tr>`;}).join('')}</tbody></table></div><p class="small">All retained references, including conventional estimators and mathematical audits. This is not a specialist-only win count. Category-equal fractions average within each category then equally across categories, avoiding a three-task category receiving three times the weight.</p></section>`;}
