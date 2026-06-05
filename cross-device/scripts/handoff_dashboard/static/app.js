(function () {
  "use strict";
  const POLL_MS = 5000;
  const COMPLETED_LIMIT = 5;
  const COLS = [
    ["awaiting", "Awaiting"],
    ["in_progress", "In Progress"],
    ["completed", "Completed"],
    ["archived", "Archived"],
  ];
  let lastModel = null;

  function el(id) { return document.getElementById(id); }

  function setText(node, text) {
    node.textContent = text == null ? "" : String(text);
  }

  function cardEl(c) {
    const d = document.createElement("div");
    d.className = "card";
    d.dataset.id = c.id;
    const id = document.createElement("span");
    id.className = "id";
    setText(id, c.id);
    d.appendChild(id);
    if (c.has_return) {
      const b = document.createElement("span");
      b.className = "badge";
      setText(b, "RETURN");
      d.appendChild(b);
    }
    const route = document.createElement("div");
    setText(route, (c.from || "") + " → " + (c.to || ""));
    d.appendChild(route);
    const st = document.createElement("div");
    setText(st, c.effective_status || "");
    d.appendChild(st);
    d.addEventListener("click", () => showDetail(c));
    return d;
  }

  function showDetail(c) {
    const lines = [
      "ID: " + c.id,
      "Route: " + (c.from || "") + " → " + (c.to || ""),
      "Effective: " + (c.effective_status || ""),
      "LOG: " + (c.log_status || ""),
      "README: " + (c.readme_status || "—"),
      "Link: " + (c.link || ""),
      "Warnings: " + ((c.warnings || []).join(", ") || "none"),
    ];
    setText(el("detail-body"), lines.join("\n"));
    el("detail").classList.remove("hidden");
  }

  function renderBoard(model) {
    lastModel = model;
    const meta = model.meta || {};
    setText(
      el("meta-line"),
      (meta.device || "?") + " | " + (meta.timestamp_utc || "") +
        (meta.ball_holder ? " | " + meta.ball_holder : "")
    );
    const top3 = (model.coordination && model.coordination.open_items_top3) || "_none_";
    setText(el("top3"), top3);
    const wul = el("warnings");
    wul.replaceChildren();
    (model.warnings || []).forEach((w) => {
      const li = document.createElement("li");
      setText(li, w);
      wul.appendChild(li);
    });
    const board = el("board");
    board.replaceChildren();
    const columns = model.columns || {};
    COLS.forEach(([key, title]) => {
      const col = document.createElement("div");
      col.className = "col";
      const h = document.createElement("h3");
      const cards = columns[key] || [];
      setText(h, title + " (" + cards.length + ")");
      col.appendChild(h);
      cards.forEach((c) => col.appendChild(cardEl(c)));
      board.appendChild(col);
    });
  }

  function apiUrl(fmt, limit) {
    const q = "format=" + encodeURIComponent(fmt) +
      "&completed_limit=" + encodeURIComponent(String(limit));
    return "/api/kanban?" + q;
  }

  async function fetchJson() {
    const r = await fetch(apiUrl("json", COMPLETED_LIMIT));
    if (!r.ok) throw new Error("API " + r.status);
    return r.json();
  }

  async function refresh() {
    try {
      const model = await fetchJson();
      renderBoard(model);
    } catch (e) {
      setText(el("meta-line"), "Error: " + e.message);
    }
  }

  async function exportFmt(fmt) {
    const r = await fetch(apiUrl(fmt, COMPLETED_LIMIT));
    const body = await r.text();
    if (fmt === "json") {
      await navigator.clipboard.writeText(body);
      alert("JSON copied to clipboard");
      return;
    }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([body], { type: "text/plain" }));
    a.download = "handoff-kanban." + (fmt === "board" ? "txt" : "md");
    a.click();
    URL.revokeObjectURL(a.href);
  }

  el("btn-refresh").addEventListener("click", refresh);
  el("btn-close-detail").addEventListener("click", () => el("detail").classList.add("hidden"));
  document.querySelectorAll("#export button").forEach((btn) => {
    btn.addEventListener("click", () => exportFmt(btn.dataset.fmt));
  });

  refresh();
  setInterval(refresh, POLL_MS);
})();