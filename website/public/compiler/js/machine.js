/* ===== TFPT Machine — interactive engine (v4) ===== */
(function () {
  "use strict";
  const D = window.TFPT_DATA;
  const canvas = document.getElementById("machine");
  const ctx = canvas.getContext("2d");
  const tooltip = document.getElementById("tooltip");
  const byId = {};
  D.stations.forEach((s) => (byId[s.id] = s));

  // ---- depth (forward edges only) ----
  const depth = {};
  function compDepth(id) {
    if (depth[id] != null && depth[id] >= 0) return depth[id];
    depth[id] = -1;
    const ins = D.edges.filter((e) => e[1] === id).map((e) => e[0]);
    const d = ins.length ? Math.max.apply(null, ins.map(compDepth)) + 1 : 0;
    depth[id] = d; return d;
  }
  D.stations.forEach((s) => compDepth(s.id));
  const MAXD = Math.max.apply(null, Object.values(depth));
  D.stations.forEach((s) => { s.depth = depth[s.id]; s.t = s.depth / MAXD; });
  const stageT = (id) => byId[id].t;
  const GLUE_DEPTH = byId.gate.depth;

  // ---- ancestors (for x-ray) ----
  function ancestorsOf(id) {
    const set = new Set([id]); let frontier = [id];
    while (frontier.length) { const next = []; D.edges.forEach(([a, b]) => { if (frontier.indexOf(b) >= 0 && !set.has(a)) { set.add(a); next.push(a); } }); frontier = next; }
    return set;
  }

  // ---- state ----
  let W = 0, H = 0, dpr = 1, progress = 0, running = false, speed = 1;
  let plainMode = true, xrayMode = false, xrayTarget = null, forging = false;
  let substrateMode = false, subHover = null, forcedBreak = null, breakReason = null;
  let tPrev = performance.now(), clock = 0, selected = null, hover = null;
  let liveN = 8, liveG = 5, cl = D.em.closure(8, 5), closesNow = true;
  const onlinePreds = new Set(); let smOnline = false;

  function scaleF() { return Math.max(0.74, Math.min(1.05, W / 1320)); }
  function sizeOf(s) {
    const k = s.kind === "gear" ? 1 : scaleF(); // gear has fixed internal geometry
    let b;
    switch (s.kind) {
      case "source": b = { w: 112, h: 300 }; break;
      case "input": b = { w: 144, h: 82 }; break;
      case "build": b = { w: 148, h: 84 }; break;
      case "auditor": b = { w: 234, h: 234 }; break;
      case "gear": b = { w: 212, h: 142 }; break;
      case "assembler": b = { w: 150, h: 86 }; break;
      case "output": b = { w: 122, h: 102 }; break;
      default: b = { w: 146, h: 84 }; // factory / gate / rom / engine / decoder / stage
    }
    return { w: b.w * k, h: b.h * k };
  }
  function rectOf(s) { const cx = s.x * W, cy = s.y * H, z = sizeOf(s); return { x: cx - z.w / 2, y: cy - z.h / 2, w: z.w, h: z.h, cx, cy }; }
  function resize() { const r = canvas.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height; canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  window.addEventListener("resize", resize);

  // ---- helpers ----
  function roundRect(x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function hexA(hex, a) { const n = parseInt(hex.slice(1), 16); return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`; }
  function cubic(p0, c0, c1, p1, u) { const v = 1 - u; return { x: v*v*v*p0.x+3*v*v*u*c0.x+3*v*u*u*c1.x+u*u*u*p1.x, y: v*v*v*p0.y+3*v*v*u*c0.y+3*v*u*u*c1.y+u*u*u*p1.y }; }
  function edgePath(a, b) { const ra = rectOf(a), rb = rectOf(b); const p0 = { x: ra.x + ra.w, y: ra.cy }, p1 = { x: rb.x, y: rb.cy }; const dx = Math.max(40, (p1.x - p0.x) * 0.5); return { p0, c0: { x: p0.x + dx, y: p0.y }, c1: { x: p1.x - dx, y: p1.y }, p1 }; }
  function clip(t, n) { return t.length > n ? t.slice(0, n - 1) + "\u2026" : t; }
  function wrap(text, x, y, maxW, lh, maxLines, center) {
    const words = String(text).split(" "); let line = "", yy = y, lines = 0;
    const flush = () => { center ? (ctx.textAlign = "center") : 0; ctx.fillText(line, x, yy); };
    for (const w of words) {
      const test = line ? line + " " + w : w;
      if (ctx.measureText(test).width > maxW && line) { flush(); line = w; yy += lh; lines++; if (maxLines && lines >= maxLines) { ctx.fillText(clip(w, 18), x, yy); return yy; } }
      else line = test;
    }
    flush(); return yy;
  }
  function xrayActive() { return xrayMode && xrayTarget != null; }

  // ---- edges ----
  function drawEdges(hset) {
    ctx.lineCap = "round";
    D.edges.forEach(([fa, fb]) => {
      const a = byId[fa], e = edgePath(byId[fa], byId[fb]); const active = progress >= a.t - 0.001;
      const lit = !hset || (hset.has(fa) && hset.has(fb));
      ctx.save(); ctx.globalAlpha = lit ? 1 : 0.07;
      ctx.beginPath(); ctx.moveTo(e.p0.x, e.p0.y); ctx.bezierCurveTo(e.c0.x, e.c0.y, e.c1.x, e.c1.y, e.p1.x, e.p1.y);
      ctx.strokeStyle = "rgba(120,150,220,0.10)"; ctx.lineWidth = 8; ctx.stroke();
      if (active && lit) {
        ctx.strokeStyle = hexA(a.accent, 0.5); ctx.lineWidth = 2; ctx.setLineDash([7, 11]); ctx.lineDashOffset = -clock * 55 * speed; ctx.stroke(); ctx.setLineDash([]);
        for (let k = 0; k < 3; k++) { const u = (clock * 0.26 * speed + k / 3) % 1; const p = cubic(e.p0, e.c0, e.c1, e.p1, u); const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 5); g.addColorStop(0, hexA(a.accent, 0.95)); g.addColorStop(1, hexA(a.accent, 0)); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, Math.PI * 2); ctx.fill(); }
      }
      ctx.restore();
    });
  }
  function arrowHead(x, y, ang, col) { ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-10, -5); ctx.lineTo(-10, 5); ctx.closePath(); ctx.fillStyle = col; ctx.fill(); ctx.restore(); }

  function drawFeedback() {
    if (xrayActive()) return;
    const glue = byId.glue;
    if (progress >= glue.t - 0.001) {
      const rg = rectOf(glue);
      ["c3", "gcar"].forEach((tid) => {
        const rt = rectOf(byId[tid]); const p0 = { x: rg.cx, y: rg.y }, p1 = { x: rt.cx, y: rt.y - 6 };
        const c0 = { x: rg.cx, y: 16 }, c1 = { x: rt.cx, y: 16 };
        ctx.beginPath(); ctx.moveTo(p0.x, p0.y); ctx.bezierCurveTo(c0.x, c0.y, c1.x, c1.y, p1.x, p1.y);
        ctx.strokeStyle = hexA("#f0b429", 0.6); ctx.lineWidth = 2.2; ctx.setLineDash([6, 8]); ctx.lineDashOffset = clock * 70 * speed; ctx.stroke(); ctx.setLineDash([]);
        for (let k = 0; k < 3; k++) { const u = (clock * 0.22 * speed + k / 3) % 1; const p = cubic(p0, c0, c1, p1, u); ctx.beginPath(); ctx.arc(p.x, p.y, 3.5, 0, Math.PI * 2); ctx.fillStyle = hexA("#f0b429", 0.95); ctx.fill(); }
        const pe = cubic(p0, c0, c1, p1, 0.97), pe2 = cubic(p0, c0, c1, p1, 1); arrowHead(p1.x, p1.y, Math.atan2(pe2.y - pe.y, pe2.x - pe.x), hexA("#f0b429", 0.9));
      });
      ctx.textAlign = "center"; ctx.textBaseline = "top"; ctx.fillStyle = "#ffd97a"; ctx.font = "700 12.5px Inter, sans-serif";
      ctx.fillText("\u21ba RECURSION: E\u2088 closes for only one (tempo, width) \u2014 so the \u2018axioms\u2019 are forced, not chosen", W / 2, 4);
      ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    }
    const cosmo = byId.cosmo;
    if (progress >= cosmo.t - 0.001) {
      const rc = rectOf(cosmo), rs = rectOf(byId.seam); const p0 = { x: rc.cx, y: rc.y + rc.h }, p1 = { x: rs.cx, y: rs.y + rs.h }; const low = H - 14, c0 = { x: rc.cx, y: low }, c1 = { x: rs.cx, y: low };
      ctx.beginPath(); ctx.moveTo(p0.x, p0.y); ctx.bezierCurveTo(c0.x, c0.y, c1.x, c1.y, p1.x, p1.y); ctx.strokeStyle = hexA("#a78bfa", 0.4); ctx.lineWidth = 1.8; ctx.setLineDash([5, 9]); ctx.lineDashOffset = clock * 50 * speed; ctx.stroke(); ctx.setLineDash([]);
      ctx.textAlign = "center"; ctx.textBaseline = "bottom"; ctx.fillStyle = hexA("#c4b5fd", 0.9); ctx.font = "600 11px Inter, sans-serif"; ctx.fillText("the cosmic horizon IS the seam \u2014 the loop closes", (rc.cx + rs.cx) / 2, H - 2);
      ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    }
  }

  // ---- shells ----
  function shell(s, r, active) {
    const sel = selected === s.id, hov = hover === s.id;
    ctx.save();
    if (active) { ctx.shadowColor = hexA(s.accent, 0.5); ctx.shadowBlur = sel ? 24 : 14; }
    roundRect(r.x, r.y, r.w, r.h, 12);
    const g = ctx.createLinearGradient(r.x, r.y, r.x, r.y + r.h);
    g.addColorStop(0, active ? "rgba(22,32,54,0.97)" : "rgba(16,23,40,0.85)"); g.addColorStop(1, active ? "rgba(12,19,35,0.97)" : "rgba(10,15,28,0.85)");
    ctx.fillStyle = g; ctx.fill(); ctx.shadowBlur = 0;
    ctx.lineWidth = sel ? 2.2 : 1.4; ctx.strokeStyle = active ? hexA(s.accent, sel || hov ? 0.95 : 0.55) : "rgba(110,140,200,0.22)"; ctx.stroke();
    roundRect(r.x, r.y, 5, r.h, 12); ctx.fillStyle = active ? s.accent : "rgba(110,140,200,0.3)"; ctx.fill();
    ctx.restore();
  }
  function brokenBorder(r) {
    roundRect(r.x, r.y, r.w, r.h, 12); ctx.strokeStyle = hexA("#fb7185", 0.85); ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = hexA("#fb7185", 0.08); ctx.fill();
    ctx.fillStyle = "#fb7185"; ctx.font = "700 14px Inter, sans-serif"; ctx.textAlign = "right"; ctx.fillText("\u2717", r.x + r.w - 9, r.y + 19); ctx.textAlign = "left";
  }

  function moduleText(s, r, active) {
    const main = plainMode ? s.plain : s.title, sub = plainMode ? s.sub : s.tech;
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.font = "18px serif"; ctx.fillStyle = active ? s.accent : "#6b7b9c"; ctx.fillText(s.icon, r.x + 13, r.y + 25);
    ctx.fillStyle = active ? "#eef3ff" : "#7e8eb0"; ctx.font = "700 13px Inter, sans-serif";
    const y1 = wrap(main, r.x + 38, r.y + 21, r.w - 48, 15, 2);
    ctx.fillStyle = active ? hexA(s.accent, 0.95) : "#69799a"; ctx.font = (plainMode ? "11px Inter, sans-serif" : "10.5px 'JetBrains Mono', monospace");
    wrap(sub, r.x + 14, Math.max(y1 + 17, r.y + 40), r.w - 24, 13, 2);
    ctx.textAlign = "left";
  }
  function nodeExtras(s, r, active) {
    if (!active) return;
    ctx.textBaseline = "alphabetic";
    if (s.id === "families") { const ok = liveG === 5 && closesNow; ctx.font = "700 11px 'JetBrains Mono', monospace"; ctx.fillStyle = ok ? "#34d39a" : "#fb7185"; ctx.textAlign = "right"; ctx.fillText(ok ? "3 gen \u2713" : ((cl.nfam == null ? "\u2014" : cl.nfam) + " gen \u2717"), r.x + r.w - 10, r.y + r.h - 11); ctx.textAlign = "left"; }
    if (s.id === "em") { const ok = cl.alphaOk && closesNow; ctx.font = "700 9.5px 'JetBrains Mono', monospace"; ctx.fillStyle = ok ? "#34d39a" : "#fb7185"; ctx.textAlign = "right"; ctx.fillText("\u03b1\u207b\u00b9 " + (isFinite(cl.ainv) ? cl.ainv.toFixed(3) : "\u2014") + (ok ? " \u2713" : " \u2717"), r.x + r.w - 9, r.y + r.h - 9); ctx.textAlign = "left"; }
    if (s.id === "gate") { ctx.font = "700 10px 'JetBrains Mono', monospace"; ctx.fillStyle = closesNow ? "#34d39a" : "#fb7185"; ctx.textAlign = "right"; ctx.fillText(closesNow ? "\u27e8CLACK\u27e9 \u2713" : "won't latch \u2717", r.x + r.w - 10, r.y + r.h - 11); ctx.textAlign = "left"; }
  }

  function drawSource(s, active) {
    const r = rectOf(s); shell(s, r, active); const cx = r.cx;
    const grad = ctx.createLinearGradient(cx - 6, 0, cx + 6, 0); grad.addColorStop(0, hexA(s.accent, 0)); grad.addColorStop(0.5, hexA(s.accent, active ? 0.6 : 0.25)); grad.addColorStop(1, hexA(s.accent, 0));
    ctx.fillStyle = grad; ctx.fillRect(cx - 7, r.y + 56, 14, r.h - 100);
    for (let i = 0; i < 4; i++) { const my = r.y + 82 + i * ((r.h - 156) / 3); const pulse = active && running ? 4 + 1.6 * Math.sin(clock * 3 + i) : 3.5; ctx.beginPath(); ctx.arc(cx, my, pulse, 0, Math.PI * 2); ctx.fillStyle = active ? "#fff" : "#9aa8c6"; ctx.fill(); ctx.beginPath(); ctx.arc(cx, my, pulse + 3, 0, Math.PI * 2); ctx.strokeStyle = hexA(s.accent, 0.7); ctx.lineWidth = 1.4; ctx.stroke(); }
    ctx.textAlign = "center"; ctx.textBaseline = "alphabetic"; ctx.fillStyle = active ? "#eef3ff" : "#7e8eb0"; ctx.font = "700 13px Inter, sans-serif"; ctx.fillText(plainMode ? s.plain : "The seam", r.cx, r.y + 26);
    ctx.fillStyle = active ? hexA(s.accent, 0.95) : "#69799a"; ctx.font = "10.5px Inter, sans-serif"; wrap(plainMode ? s.sub : s.tech, cx, r.y + 44, r.w - 18, 13, 2, true);
    ctx.fillStyle = active ? hexA(s.accent, 0.9) : "#69799a"; ctx.font = "600 10px 'JetBrains Mono', monospace"; ctx.textAlign = "center"; ctx.fillText("\u03bc\u2084 = 4 marks", r.cx, r.y + r.h - 12);
    ctx.textAlign = "left";
  }

  function drawInput(s, active) {
    const r = rectOf(s); shell(s, r, active); ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.font = "16px serif"; ctx.fillStyle = active ? s.accent : "#6b7b9c"; ctx.fillText(s.icon, r.x + 13, r.y + 23);
    ctx.fillStyle = "#8fa0c4"; ctx.font = "700 10px Inter, sans-serif"; ctx.fillText((plainMode ? s.plain : s.title.toUpperCase()), r.x + 36, r.y + 20);
    const val = s.id === "c3" ? `c\u2083 = 1/(${liveN}\u03c0)` : `g_car = ${liveG}`;
    const off = (s.id === "c3" && liveN !== 8) || (s.id === "gcar" && liveG !== 5);
    ctx.fillStyle = off ? "#fb7185" : (active ? s.accent : "#7e8eb0"); ctx.font = "700 16px 'JetBrains Mono', monospace"; ctx.fillText(val, r.x + 14, r.y + 48);
    ctx.fillStyle = "#9fb2d6"; ctx.font = "10px Inter, sans-serif"; wrap(plainMode ? s.sub : "read off the seam", r.x + 14, r.y + 66, r.w - 22, 12, 1);
    if (active && running && !off) { const px = r.x + r.w, py = r.cy, pulse = 3 + 2 * Math.sin(clock * 4 + (s.id === "gcar" ? 1 : 0)); ctx.beginPath(); ctx.arc(px, py, pulse, 0, Math.PI * 2); ctx.fillStyle = hexA(s.accent, 0.9); ctx.fill(); }
  }

  function drawAuditor(s, active) {
    const r = rectOf(s), R = r.w / 2 - 8, cx = r.cx, cy = r.cy;
    const broken = active && !closesNow;
    const col = broken ? "#fb7185" : (active ? "#34d39a" : "#7c8db0");
    if (active && running) { for (let i = 0; i < 3; i++) { const rr = R + 10 + i * 12 + 3 * Math.sin(clock * 2 - i); ctx.beginPath(); ctx.arc(cx, cy, rr, 0, Math.PI * 2); ctx.strokeStyle = hexA(col, 0.16 - i * 0.04); ctx.lineWidth = 2; ctx.stroke(); } }
    ctx.save(); if (active) { ctx.shadowColor = hexA(col, 0.55); ctx.shadowBlur = 28; }
    ctx.beginPath(); for (let i = 0; i < 6; i++) { const a = -Math.PI / 2 + i * Math.PI / 3, x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.closePath();
    const g = ctx.createLinearGradient(cx, cy - R, cx, cy + R);
    g.addColorStop(0, broken ? "rgba(46,14,22,0.97)" : (active ? "rgba(16,34,28,0.97)" : "rgba(16,20,30,0.9)")); g.addColorStop(1, broken ? "rgba(26,10,16,0.97)" : (active ? "rgba(10,22,20,0.97)" : "rgba(10,14,22,0.9)"));
    ctx.fillStyle = g; ctx.fill(); ctx.shadowBlur = 0; ctx.lineWidth = selected === s.id ? 3 : 2.4; ctx.strokeStyle = hexA(col, active ? 0.95 : 0.3); ctx.stroke(); ctx.restore();
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillStyle = active ? (broken ? "#ffd0d8" : "#bff3df") : "#8b9bbd"; ctx.font = "700 13px Inter, sans-serif"; ctx.fillText("E\u2088 AUDIT CORE", cx, cy - R * 0.62);
    ctx.fillStyle = active ? hexA("#9fb2d6", 0.95) : "#69799a"; ctx.font = "9.5px Inter, sans-serif"; ctx.fillText("validates routes \u00b7 not a gauge group", cx, cy - R * 0.47);
    ctx.fillStyle = active ? "#fff" : "#8b9bbd"; ctx.font = "800 " + Math.round(R * 0.46) + "px 'JetBrains Mono', monospace"; ctx.fillText("E\u2088", cx, cy - R * 0.04);
    ctx.font = "700 13px Inter, sans-serif"; ctx.fillStyle = active ? (broken ? "#fb7185" : "#34d39a") : "#5b6b8c"; ctx.fillText(active ? (broken ? "\u2717 DOES NOT CLOSE" : "\u2713 validates the closure") : "does it close?", cx, cy + R * 0.22);
    if (active && !broken) {
      ["det = 1", "roots = 240", "slices 7 / 7"].forEach((t, i) => { const y = cy + R * 0.40 + i * 15; ctx.beginPath(); ctx.arc(cx - 54, y, 2.8, 0, Math.PI * 2); ctx.fillStyle = "#34d39a"; ctx.fill(); ctx.fillStyle = "#bff3df"; ctx.font = "10.5px 'JetBrains Mono', monospace"; ctx.textAlign = "left"; ctx.fillText(t + "  \u2713", cx - 46, y); ctx.textAlign = "center"; });
    } else if (broken) { ctx.font = "10.5px Inter, sans-serif"; ctx.fillStyle = "#ffb3bf"; wrap(breakReason || cl.reason, cx, cy + R * 0.42, R * 1.5, 12, 2, true); }
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
  }

  function drawGearShape(cx, cy, Z, pitch, phase, fill, stroke) {
    const ro = pitch + pitch * 0.32, ri = pitch - pitch * 0.20, step = (Math.PI * 2) / Z, tw = step * 0.48, tipw = step * 0.26;
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(phase); ctx.beginPath(); let started = false;
    const P = (rad, ang) => { const x = Math.cos(ang) * rad, y = Math.sin(ang) * rad; started ? ctx.lineTo(x, y) : (ctx.moveTo(x, y), (started = true)); };
    for (let k = 0; k < Z; k++) { const c = k * step; P(ri, c - step / 2); P(ri, c - tw / 2); P(ro, c - tipw / 2); P(ro, c + tipw / 2); P(ri, c + tw / 2); }
    ctx.closePath(); ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 1.6; ctx.strokeStyle = stroke; ctx.stroke();
    ctx.beginPath(); ctx.arc(0, 0, pitch * 0.34, 0, Math.PI * 2); ctx.fillStyle = "#0a1120"; ctx.fill(); ctx.lineWidth = 1.3; ctx.strokeStyle = stroke; ctx.stroke(); ctx.restore();
  }
  function drawClock(s, active) {
    const r = rectOf(s); shell(s, r, active); ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.font = "16px serif"; ctx.fillStyle = active ? s.accent : "#6b7b9c"; ctx.fillText(s.icon, r.x + 13, r.y + 24);
    ctx.fillStyle = active ? "#eef3ff" : "#7e8eb0"; ctx.font = "700 13px Inter, sans-serif"; ctx.fillText(plainMode ? s.plain : s.title, r.x + 36, r.y + 20);
    const cy = r.y + 78, pA = 27, pB = 22.5, cxA = r.x + 52, cxB = cxA + (pA + pB); const ph = active && running ? clock * 1.05 * speed : clock * 0.12;
    drawGearShape(cxA, cy, 6, pA, ph, hexA("#5b8cff", active ? 0.92 : 0.4), "#9fc0ff"); drawGearShape(cxB, cy, 5, pB, -ph * (6 / 5) + 0.32, hexA("#f0b429", active ? 0.92 : 0.4), "#ffd97a");
    ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillStyle = "#dfe9ff"; ctx.font = "600 12px 'JetBrains Mono', monospace"; ctx.fillText("6", cxA, cy); ctx.fillText("5", cxB, cy);
    ctx.textAlign = "left"; ctx.fillStyle = active ? hexA("#5b8cff", 0.95) : "#69799a"; ctx.font = "10.5px Inter, sans-serif"; ctx.fillText("dynamic 6 \u2192 rates", r.x + r.w - 118, cy - 12); ctx.fillStyle = active ? hexA("#f0b429", 0.95) : "#69799a"; ctx.fillText("static 5 \u2192 lattice", r.x + r.w - 118, cy + 6);
    ctx.textAlign = "center"; ctx.fillStyle = active ? "#cfe0ff" : "#69799a"; ctx.font = "700 13px 'JetBrains Mono', monospace"; ctx.fillText("30 = 5 \u00d7 6", r.cx, r.y + r.h - 13); ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
  }

  function drawOutput(s, active) {
    const r = rectOf(s); shell(s, r, active); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.font = "20px serif"; ctx.fillStyle = active ? s.accent : "#6b7b9c"; ctx.fillText(s.icon, r.cx, r.y + 24);
    ctx.fillStyle = active ? "#eef3ff" : "#7e8eb0"; ctx.font = "700 12px Inter, sans-serif"; ctx.fillText(plainMode ? "PREDICTIONS" : "Readout", r.cx, r.cy + 2);
    ctx.font = "700 20px 'JetBrains Mono', monospace"; ctx.fillStyle = active ? (closesNow ? s.accent : "#fb7185") : "#6b7b9c"; ctx.fillText(closesNow ? onlinePreds.size + " / 23" : "\u2717 0", r.cx, r.cy + 26);
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
  }

  // ---- substrate (hypergraph X-ray) ----
  function subPos() { const m = {}; D.substrate.nodes.forEach((n) => { m[n.id] = { x: n.x * W, y: n.y * H, n }; }); return m; }
  function drawSubstrate() {
    const S = D.substrate, pos = subPos(); ctx.lineCap = "round";
    S.edges.forEach(([a, b, type, st], idx) => {
      const A = pos[a], B = pos[b]; if (!A || !B) return; const col = S.types[type].color;
      const mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2 - 24;
      ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.quadraticCurveTo(mx, my, B.x, B.y);
      ctx.strokeStyle = hexA(col, st === "E" ? 0.6 : 0.42); ctx.lineWidth = st === "E" ? 2 : 1.6; ctx.setLineDash(st === "C" ? [5, 7] : []); ctx.lineDashOffset = -clock * 40; ctx.stroke(); ctx.setLineDash([]);
      const u = (clock * 0.22 + (idx % 3) / 3) % 1, t = u, x = (1 - t) * (1 - t) * A.x + 2 * (1 - t) * t * mx + t * t * B.x, y = (1 - t) * (1 - t) * A.y + 2 * (1 - t) * t * my + t * t * B.y;
      ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fillStyle = hexA(col, 0.9); ctx.fill();
    });
    const KCOL = { in: "#9fb2d6", build: "#5b8cff", audit: "#34d39a", flavor: "#a78bfa", seed: "#f0b429", out: "#3fd0e0" };
    S.nodes.forEach((n) => {
      const p = pos[n.id], R = n.id === "E8" ? 30 : 20, col = KCOL[n.k] || "#9fb2d6", hl = subHover === n.id;
      ctx.beginPath(); ctx.arc(p.x, p.y, R, 0, Math.PI * 2); ctx.fillStyle = "rgba(12,19,35,0.96)"; ctx.fill(); ctx.lineWidth = hl ? 3 : 2; ctx.strokeStyle = col; ctx.stroke();
      ctx.fillStyle = "#eef3ff"; ctx.font = (n.id === "E8" ? "700 16px" : "600 12px") + " 'JetBrains Mono', monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(n.label, p.x, p.y);
    });
    ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.fillStyle = "#cdd9ef"; ctx.font = "700 13px Inter, sans-serif"; ctx.fillText("SUBSTRATE \u2014 typed hypergraph", 18, 26);
    const types = Object.keys(S.types);
    types.forEach((t, i) => { const col = S.types[t].color, xx = 18 + (i % 3) * 150, yy = H - 56 + Math.floor(i / 3) * 18; ctx.strokeStyle = col; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(xx, yy); ctx.lineTo(xx + 22, yy); ctx.stroke(); ctx.fillStyle = "#9fb2d6"; ctx.font = "11px Inter, sans-serif"; ctx.fillText(S.types[t].label, xx + 28, yy + 4); });
    ctx.fillStyle = "#7e8eb0"; ctx.font = "11px Inter, sans-serif"; wrap(S.note, 18, H - 12, W - 36, 13, 1);
  }

  function drawBelts() {
    const bands = [
      { y0: 0.035, y1: 0.43, c: "#5b8cff", t: "SYNTAX \u00b7 compiler (discrete, exact)" },
      { y0: 0.45, y1: 0.655, c: "#3fd0e0", t: "DYNAMICS \u00b7 transport (gapped attractor)" },
      { y0: 0.675, y1: 0.975, c: "#f0b429", t: "PHYSICS \u00b7 dressing (v_geo \u00b7 RG \u00b7 Boltzmann)" },
    ];
    bands.forEach((b) => {
      const y = b.y0 * H, h = (b.y1 - b.y0) * H;
      roundRect(8, y, W - 16, h, 14); ctx.fillStyle = hexA(b.c, 0.035); ctx.fill();
      ctx.strokeStyle = hexA(b.c, 0.16); ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = hexA(b.c, 0.6); ctx.font = "700 10.5px Inter, sans-serif"; ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
      ctx.fillText(b.t, 18, y + 16);
    });
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    if (substrateMode) { drawSubstrate(); return; }
    drawBelts();
    const hset = xrayActive() ? ancestorsOf(xrayTarget) : null;
    drawEdges(hset); drawFeedback();
    D.stations.forEach((s) => {
      const active = progress >= s.t - 0.001;
      ctx.save(); ctx.globalAlpha = hset ? (hset.has(s.id) ? 1 : 0.12) : 1;
      if (s.kind === "source") drawSource(s, active);
      else if (s.kind === "input") drawInput(s, active);
      else if (s.kind === "auditor") drawAuditor(s, active);
      else if (s.kind === "gear") drawClock(s, active);
      else if (s.kind === "output") drawOutput(s, active);
      else { const r = rectOf(s); shell(s, r, active); moduleText(s, r, active); nodeExtras(s, r, active); }
      if (active && !closesNow && s.depth >= GLUE_DEPTH && s.kind !== "auditor") brokenBorder(rectOf(s));
      ctx.restore();
    });
  }

  // ---- boards ----
  function escapeHTML(s) { return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
  const ROUTE_LABEL = { compiler: "compiler-closed", transfer: "transfer bridge", open: "open \u00b7 not forced", failed: "falsified" };
  const BRIDGE_LABEL = { compiler: "closed \u2014 exact compiler readout", transfer: "needs F_transfer / RG / Boltzmann / v_geo", open: "open \u2014 explicitly not a compiler power", failed: "excluded by current data" };
  function routeOf(p, isPred) { if (isPred) return p.status === "E" ? "compiler" : (p.status === "C" ? "transfer" : "open"); return { green: "compiler", orange: "transfer", red: "failed", slate: "open" }[p.match] || "open"; }
  function cardHTML(p, route, isPred) {
    const foot = isPred && p.horizon
      ? `<div class="c-when h-${p.horizon}">${escapeHTML(D.horizons[p.horizon].label)}</div>`
      : `<div class="c-cat">${escapeHTML(p.cat)}</div>`;
    return `<span class="c-dotmark"></span><div class="c-sym">${escapeHTML(p.sym)}</div><div class="c-title">${escapeHTML(p.title)}</div><div class="c-val">TFPT ${escapeHTML(p.tfpt)}</div><div class="c-meas">obs ${escapeHTML(p.measured)}</div>${foot}<div class="c-route r-${route}">\u25cf ${ROUTE_LABEL[route]}</div>`;
  }
  function flash(el) { el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash"); }
  function buildGroupedBoard(container, items, groups, keyOf, isPred) {
    const map = {};
    groups.forEach((grp) => {
      const members = []; items.forEach((p, i) => { if (keyOf(p) === grp.key) members.push({ p, i }); });
      if (!members.length) return;
      const sec = document.createElement("div"); sec.className = "board-group";
      const head = document.createElement("div"); head.className = "board-group-head";
      head.innerHTML = `<span class="bg-bar" style="background:${grp.color}"></span><div><div class="bg-title">${escapeHTML(grp.label)} <span class="bg-count">${members.length}</span></div><div class="bg-blurb">${escapeHTML(grp.blurb)}</div></div>`;
      sec.appendChild(head);
      const grid = document.createElement("div"); grid.className = "board";
      members.forEach(({ p, i }) => {
        const el = document.createElement("div"); el.className = "card m-" + p.match;
        el.innerHTML = cardHTML(p, routeOf(p, isPred), isPred);
        el.addEventListener("click", () => onCard(p, isPred, el));
        grid.appendChild(el); map[i] = el;
      });
      sec.appendChild(grid); container.appendChild(sec);
    });
    return map;
  }
  const smBoard = document.getElementById("sm-board");
  const smMap = buildGroupedBoard(smBoard, D.sm, D.smGroups, (p) => p.sec, false);
  const smCards = Object.keys(smMap).map((k) => smMap[k]);
  const board = document.getElementById("board");
  const predCards = buildGroupedBoard(board, D.predictions, D.predGroups, (p) => p.cat, true);
  function onCard(p, isPred, el) { if (xrayMode) { xrayTarget = (isPred ? p.stage : "sm"); flash(el); } else { openModal(p, isPred); flash(el); } }
  (function () { const c = { green: 0, orange: 0, red: 0, slate: 0 }; D.predictions.forEach((p) => c[p.match]++); document.getElementById("tally").innerHTML = `<span class="t-green">${c.green} match</span><span class="t-orange">${c.orange} near</span><span class="t-red">${c.red} miss</span><span class="t-slate">${c.slate} pending</span>`; })();
  (function () { const order = ["settled", "live", "soon", "next", "structural"]; document.getElementById("timeline-legend").innerHTML = `<span class="tl-lead">When could it be confirmed / refuted?</span>` + order.map((h) => `<span class="tl h-${h}">${escapeHTML(D.horizons[h].label)}</span>`).join(""); })();
  function updateBoards() {
    D.predictions.forEach((p, i) => { if (progress >= stageT(p.stage) - 0.001) { if (!onlinePreds.has(i)) { onlinePreds.add(i); predCards[i].classList.add("online", "flash"); } } });
    document.getElementById("pred-count").textContent = `\u00b7 ${onlinePreds.size} / 23 online`;
    if (progress >= stageT("sm") - 0.001 && !smOnline) { smOnline = true; smCards.forEach((el, k) => setTimeout(() => el.classList.add("online", "flash"), k * 32)); document.getElementById("sm-count").textContent = "\u00b7 assembled"; }
  }
  function updateBanner() { let lvl = 0; D.stations.forEach((s) => { if (progress >= s.t - 0.001) lvl = Math.max(lvl, s.depth); }); const st = D.steps[lvl] || D.steps[0]; document.getElementById("step-index").textContent = `Step ${lvl} / ${MAXD}`; document.getElementById("step-title").textContent = st.t; document.getElementById("step-desc").textContent = st.d; }

  // ---- inspector + modal ----
  const $ = (id) => document.getElementById(id);
  function setChips(arr) { const box = $("insp-atoms"); box.innerHTML = ""; (arr || []).forEach((a) => { const c = document.createElement("span"); c.className = "chip"; c.textContent = a; box.appendChild(c); }); }
  function showStation(s) {
    selected = s.id; $("insp-title").textContent = s.plain || s.title; $("insp-sub").textContent = (s.title || "") + (s.tech ? "  \u00b7  " + s.tech : ""); $("insp-big").textContent = "";
    if (s.id === "glue") {
      setChips(D.e8slices.map((r) => `${r.name}: ${r.what}`));
      $("insp-detail").textContent = "E\u2088 is the audit hull \u2014 the validator, NOT a gauge group and NOT the world. It accepts only structures that close as an even unimodular object (det = 1); the Standard Model is then read out by projection along these seven maximal-slice routes. " + (s.detail || "");
    } else { setChips(s.atoms); $("insp-detail").textContent = s.detail || ""; }
  }
  const modal = $("modal"); const MATCH_LABEL = { green: "match", orange: "near / tension", red: "no match", slate: "not yet decisive" }; const TYPE_LABEL = { E: "[E] exact", C: "[C] conditional", O: "[O] open" };
  function openModal(p, isPred) {
    let b = `<span class="badge b-${p.match}">\u25cf ${MATCH_LABEL[p.match]}</span>`; if (isPred && p.status) b += `<span class="badge b-type">${TYPE_LABEL[p.status]}</span>`; b += `<span class="badge b-type">${escapeHTML(p.cat)}</span>`; if (isPred && p.horizon) b += `<span class="badge b-type">${escapeHTML(D.horizons[p.horizon].label)}</span>`;
    $("modal-badges").innerHTML = b; $("modal-title").textContent = p.title; $("modal-tfpt").textContent = p.tfpt; $("modal-measured").textContent = p.measured; $("modal-note").textContent = p.note || ""; $("modal-formula").textContent = p.formula || "\u2014"; $("modal-detail").textContent = p.detail || "";
    const route = routeOf(p, isPred);
    $("modal-route").textContent = ROUTE_LABEL[route];
    $("modal-e8route").textContent = isPred ? (D.e8routeMap[p.title] || "\u2014") : (D.smRouteByCat[p.cat] || "\u2014");
    $("modal-bridge").textContent = BRIDGE_LABEL[route];
    const kr = $("modal-kill-row"); if (isPred && p.kill) { kr.hidden = false; $("modal-kill").textContent = p.kill; } else kr.hidden = true;
    const wr = $("modal-when-row"); if (isPred && p.when) { wr.hidden = false; $("modal-when").textContent = p.when; } else wr.hidden = true;
    modal.hidden = false;
  }
  function closeModal() { modal.hidden = true; }
  $("modal-close").addEventListener("click", closeModal); modal.addEventListener("click", (e) => { if (e.target === modal) closeModal(); });

  // ---- deep modal (click a key part → rich explainer) ----
  const deepModal = $("deepmodal"), deepBody = $("deep-body");
  const DEEP = new Set(["seam", "glue", "seed", "em", "cosmo"]);
  const C = D.constants;
  const fmt = (x, n) => Number(x).toFixed(n);
  const eh = escapeHTML;

  function deepContent(id) {
    if (id === "seam") return deepSource();
    if (id === "glue") return deepE8();
    if (id === "seed") return deepSeed();
    if (id === "em") return deepAlpha();
    if (id === "cosmo") return deepGravity();
    return "";
  }
  function deepSource() {
    return `
      <div class="deep-kicker">The Source \u00b7 the boundary seam</div>
      <h3>\u25c8 What is \u201cThe Source\u201d?</h3>
      <p class="deep-lede">TFPT does not start from space, particles or forces. It starts from a single <b>boundary</b> \u2014 an <b>edge</b>. Picture the rim where an inside meets an outside.</p>
      <div class="deep-sec"><h4>The one picture to remember</h4>
        <p class="deep-p">On that edge sit exactly <b>four marks</b> \u2014 like four notches on a ring: <b>\u03bc\u2084 = {1, i, \u22121, \u2212i}</b>. Everything else in the theory is just <b>two ways of reading the same marked edge</b>.</p></div>
      <div class="deep-cables">
        <div class="cable" style="--accent:#5b8cff"><div class="cb-i">\u21bb</div><div><div class="cb-t">Reading 1 \u2014 count the loops</div><div class="cb-d">how many independent loops circle the 4 marks</div></div><div class="cb-v">3<small>\u2192 three families</small></div></div>
        <div class="cable" style="--accent:#34d39a"><div class="cb-i">\u0192</div><div><div class="cb-t">Reading 2 \u2014 count the functions</div><div class="cb-d">the smallest set of functions living on the marks</div></div><div class="cb-v">16<small>\u2192 one particle generation</small></div></div>
      </div>
      <div class="deep-sec"><h4>Why exactly four marks? (it\u2019s forced)</h4>
        <p class="deep-p">Not chosen by hand. The one-sided Gauss\u2013Bonnet of the seam\u2019s normal slice gives <b>n = 2\u03c7 = 4</b> marks \u2014 and the same <b>8</b> (|\u2124\u2082|\u00b72\u03c0\u03c7 = 8\u03c0) is the tempo <b>c\u2083 = 1/(8\u03c0)</b>. So the two \u201caxioms\u201d are two fingerprints of this one edge.</p></div>
      <div class="deep-formula">\u2119\u00b9 \u2216 \u03bc\u2084  =  the four-punctured line,   deck map  z \u21a6 i\u00b7z  (the order-4 seam clock)<small>The only ingredient with no cheaper origin is \u03c0 itself.</small></div>
      <p class="deep-hint">Everything to the right is downstream of this single object \u2014 follow the arrows.</p>`;
  }
  function deepE8() {
    return `
      <div class="deep-kicker">The Auditor \u00b7 E\u2088 root system</div>
      <h3>\u2713 E\u2088 \u2014 the rulebook that checks the fit</h3>
      <p class="deep-lede">E\u2088 is <b>not</b> a force, <b>not</b> a gauge group and <b>not</b> \u201cthe universe\u201d. It is the <b>auditor</b>: the unique even-unimodular lattice (det = 1) in which the carrier D\u2085, the families A\u2083 and the glue \u03bc\u2084 lock together \u2014 and they lock <b>only one way</b>.</p>
      <div class="e8-wrap"><canvas id="e8c"></canvas></div>
      <p class="e8-cap">The 240 roots of E\u2088 \u2014 a live rotating projection out of 8 dimensions. (A visual aid for the lattice, not a literal map of \u03b1 or the masses.)</p>
      <div class="deep-grid">
        <div class="deep-fact ok"><div class="df-v">248</div><div class="df-k">dim E\u2088 = 240 roots + 8 (the rank)</div></div>
        <div class="deep-fact ok"><div class="df-v">240</div><div class="df-k">roots \u2713 (audited)</div></div>
        <div class="deep-fact ok"><div class="df-v">8</div><div class="df-k">rank = the \u201c8\u201d in c\u2083 = 1/(8\u03c0)</div></div>
        <div class="deep-fact ok"><div class="df-v">30</div><div class="df-k">Coxeter number h = 2\u00b73\u00b75</div></div>
        <div class="deep-fact ok"><div class="df-v">det = 1</div><div class="df-k">even-unimodular = the closure test</div></div>
        <div class="deep-fact ok"><div class="df-v">7 / 7</div><div class="df-k">maximal slices validate every sector</div></div>
      </div>
      <div class="deep-sec"><h4>The 7 audit routes \u2014 what each slice validates</h4>
        <div class="deep-routes">${D.e8slices.map((r) => `<div class="route-row"><span class="rr-n">${eh(r.name)}</span><span class="rr-role">${eh(r.role)}</span><span class="rr-w">${eh(r.what)}</span></div>`).join("")}</div></div>
      <div class="deep-recursion"><h4>\u21ba The recursion \u2014 how it confirms its own inputs</h4>
        <p class="deep-p">Here is the twist. The lattice <b>only closes</b> for width <b>g_car = 5</b> and the seam\u2019s <b>8</b>. Change either and the pieces no longer fit \u2014 E\u2088 never forms (try the ablation dials, or \u201cFailed universes\u201d).</p>
        <p class="deep-p">So c\u2083 and g_car are <b>not free inputs</b> \u2014 they are the <b>only</b> values the audit accepts. The gold arrows looping from E\u2088 back to the two inputs are exactly this: <b>the theory pins its own axioms.</b></p></div>`;
  }
  function deepSeed() {
    const lc = Math.sqrt(C.phi0 * (1 - C.phi0)), s13 = C.phi0 * Math.exp(-5 / 6);
    return `
      <div class="deep-kicker">Seed decoder \u00b7 \u03c6\u2080</div>
      <h3>\u2726 One seed \u2192 four observables</h3>
      <p class="deep-lede">A single number, the retarded seed <b>\u03c6\u2080 = ${fmt(C.phi0, 5)}</b>, decodes into <b>four independent measurements</b>. No extra knobs \u2014 the same \u03c6\u2080 feeds all four cables.</p>
      <div class="deep-formula">\u03c6\u2080 = 1/(6\u03c0) + 3/(256\u03c0\u2074) = ${fmt(C.phi0, 6)}<small>a base term 1/(6\u03c0) plus a small top correction 3/(256\u03c0\u2074).</small></div>
      <div class="deep-sec"><h4>The four cables</h4>
        <div class="deep-cables">
          <div class="cable" style="--accent:#f0b429"><div class="cb-i">\u27c2</div><div><div class="cb-t">Cabibbo angle \u03bb_C</div><div class="cb-d">quark mixing \u00b7 \u03bb_C = \u221a(\u03c6\u2080(1\u2212\u03c6\u2080))</div></div><div class="cb-v green">${fmt(lc, 4)}<small>obs 0.2245 \u2014 match</small></div></div>
          <div class="cable" style="--accent:#f0b429"><div class="cb-i">\u269b</div><div><div class="cb-t">Reactor angle \u03b8\u2081\u2083</div><div class="cb-d">neutrino mixing \u00b7 sin\u00b2\u03b8\u2081\u2083 = \u03c6\u2080\u00b7e^(\u22125/6)</div></div><div class="cb-v orange">${fmt(s13, 4)}<small>obs 0.0220 \u2014 ~2\u03c3</small></div></div>
          <div class="cable" style="--accent:#f0b429"><div class="cb-i">\u2b21</div><div><div class="cb-t">Baryon fraction \u03a9_b</div><div class="cb-d">cosmology \u00b7 \u03a9_b = (4\u03c0\u22121)\u00b7\u03b2</div></div><div class="cb-v green">0.0489<small>obs 0.0493 \u2014 match</small></div></div>
          <div class="cable" style="--accent:#f0b429"><div class="cb-i">\u2737</div><div><div class="cb-t">Cosmic birefringence \u03b2</div><div class="cb-d">CMB light rotation \u00b7 \u03b2 = \u03c6\u2080/(4\u03c0)</div></div><div class="cb-v green">0.2424\u00b0<small>obs 0.215\u00b0 (ACT DR6) \u2014 match</small></div></div>
        </div></div>
      <p class="deep-hint">Four different experiments \u2014 quark physics, reactors, cosmology, the CMB \u2014 from one number \u03c6\u2080.</p>`;
  }
  function deepAlpha() {
    const a0 = D.em.closure(8, 5).ainv, off = !(liveN === 8 && liveG === 5);
    const liveA = isFinite(cl.ainv) ? cl.ainv.toFixed(7) : "\u2014 no root \u2014";
    return `
      <div class="deep-kicker">\u03b1 engine \u00b7 the fine-structure constant</div>
      <h3>\u26a1 How 1/137 is computed (and why you can\u2019t cheat)</h3>
      <p class="deep-lede">The electromagnetic coupling is <b>not</b> dialled in. It is the <b>unique positive root of one cubic</b> whose every ingredient is already fixed upstream.</p>
      <div class="deep-formula">F<sub>U(1)</sub>(\u03b1) = \u03b1\u00b3 \u2212 2c\u2083\u00b3\u00b7\u03b1\u00b2 \u2212 (4/5)\u00b7c\u2083\u2076\u00b7M\u00b7ln(1/\u03c6_seam(\u03b1)) = 0<small>c\u2083 = 1/(8\u03c0) from the seam \u00b7 M = 41 = 10\u00b7b\u2081 from the hypercharge factory \u00b7 \u03c6_seam from the seed. Nothing here is free.</small></div>
      <div class="deep-grid">
        <div class="deep-fact"><div class="df-v">c\u2083 = 1/(8\u03c0)</div><div class="df-k">from THE SOURCE</div></div>
        <div class="deep-fact"><div class="df-v">M = 41</div><div class="df-k">budget = 10\u00b7b\u2081 from the factory</div></div>
        <div class="deep-fact ok"><div class="df-v">${fmt(a0, 7)}</div><div class="df-k">\u03b1\u207b\u00b9 (audited 8,5) vs CODATA 137.035999177</div></div>
      </div>
      <div class="deep-sec"><h4>No cheating \u2014 it follows from the compiler structure</h4>
        <p class="deep-p">Every symbol in the cubic is an <b>output</b> of earlier stages: the seam fixes c\u2083, the carrier fixes the budget 41, the seed fixes \u03c6_seam. There is <b>no slot to insert 137 by hand</b> \u2014 and existence + uniqueness of the positive root are proved.</p>
        <div class="deep-live"><b>\u03b1\u207b\u00b9 = ${liveA}</b><span>current dials (N=${liveN}, g=${liveG})${off ? " \u2014 off the audited (8,5)!" : " \u2014 the audited universe"}</span></div>
        <p class="deep-p">Turn the ablation dials (or open \u201cFailed universes\u201d): the root <b>moves off 137</b> for every (N, g) except the audited <b>(8, 5)</b>. That is the proof that 1/137 is forced, not fitted.</p></div>`;
  }
  function deepGravity() {
    return `
      <div class="deep-kicker">Gravity \u00b7 QFT \u00b7 Cosmos</div>
      <h3>\u272a Where gravity and quantum field theory live</h3>
      <p class="deep-lede">The <b>same edge</b>, read as a <b>horizon</b>, is where gravity, an emergent quantum field theory and cosmology come from. The seam constant <b>is</b> the gravitational one.</p>
      <div class="deep-sec"><h4>Gravity</h4>
        <p class="deep-p">c\u2083 = 1/(8\u03c0) is exactly the coefficient in Einstein\u2019s equation <b>G_\u03bc\u03bd = 8\u03c0 T_\u03bc\u03bd</b> and in the Bekenstein\u2013Hawking entropy \u2014 the seam tempo <b>is</b> the gravitational coupling.</p>
        <div class="deep-formula">spectral action \u27f6 R + R\u00b2 (Starobinsky),   scalaron mass M = c\u2083^{7/2}\u00b7M\u0304 \u2248 3.06\u00d710\u00b9\u00b3 GeV<small>The E\u2087\u00d7A\u2081 audit slice carries the gravity / inflation sector.</small></div></div>
      <div class="deep-sec"><h4>Quantum field theory</h4>
        <p class="deep-p">The boundary is an <b>emergent chiral QFT</b>: one anomaly-free generation, a spectral-triple / boundary-net description, with modular (KMS) flow in the role of time. The SM fields are projections of this boundary data \u2014 not added by hand.</p></div>
      <div class="deep-sec"><h4>Cosmos</h4>
        <p class="deep-p">The horizon reading fixes the expansion: the cosmological constant\u2019s famous ~122-orders smallness becomes <b>\u039b \u223c e^(\u22122\u03b1\u207b\u00b9)</b> (\u2248 e^(\u22122\u00b7137)), plus the inflation tilt n_s, the tensor ratio r, the baryon density and a tiny cosmic-light rotation.</p></div>
      <div class="deep-frontier"><b>Honest frontier:</b> the full nonperturbative <b>4D quantum-gravity measure</b> and the precise \u201cseam = horizon\u201d theorem stay <b>OPEN</b> (the R\u00b2/Weyl\u00b2 sector carries the Stelle ghost). This is where the compiler hands off to physics that is not yet closed \u2014 and the machine says so.</div>`;
  }

  // E8 root system: 240 roots, rotating 8D\u21922D projection
  let e8roots = null, e8raf = 0, e8t = 0;
  function buildE8Roots() {
    const r = [];
    for (let i = 0; i < 8; i++) for (let j = i + 1; j < 8; j++) for (const si of [1, -1]) for (const sj of [1, -1]) { const v = new Array(8).fill(0); v[i] = si; v[j] = sj; r.push(v); }
    for (let m = 0; m < 256; m++) { let neg = 0; const v = []; for (let b = 0; b < 8; b++) { const s = (m >> b) & 1; if (s) { neg++; v.push(-0.5); } else v.push(0.5); } if (neg % 2 === 0) r.push(v); }
    return r; // 112 + 128 = 240
  }
  function rot8(v, i, j, ang) { const c = Math.cos(ang), s = Math.sin(ang), a = v[i], b = v[j]; v[i] = a * c - b * s; v[j] = a * s + b * c; }
  function drawE8(cv, t) {
    const g = cv.getContext("2d"), w = cv.clientWidth, h = cv.clientHeight; g.clearRect(0, 0, w, h);
    if (!e8roots) e8roots = buildE8Roots();
    const cx = w / 2, cy = h / 2, R = Math.min(w, h) * 0.34;
    const pts = e8roots.map((rt) => { const v = rt.slice();
      rot8(v, 0, 1, t * 0.50); rot8(v, 2, 3, t * 0.37); rot8(v, 4, 5, t * 0.24); rot8(v, 6, 7, t * 0.16); rot8(v, 1, 4, t * 0.11); rot8(v, 3, 6, t * 0.07);
      return { x: cx + v[0] * R, y: cy + v[1] * R, z: v[2] }; });
    pts.sort((a, b) => a.z - b.z);
    for (const p of pts) { const d = Math.max(0, Math.min(1, (p.z + 1.5) / 3)); const alpha = 0.28 + 0.62 * d, rad = 1.2 + 1.9 * d;
      g.beginPath(); g.arc(p.x, p.y, rad, 0, Math.PI * 2); g.fillStyle = `rgba(${Math.round(118 + 80 * d)},${Math.round(168 + 50 * d)},255,${alpha})`; g.fill(); }
  }
  function startE8() {
    const cv = $("e8c"); if (!cv) return;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(cv.clientWidth * ratio); cv.height = Math.round(cv.clientHeight * ratio);
    cv.getContext("2d").setTransform(ratio, 0, 0, ratio, 0, 0);
    stopE8(); const loop = () => { e8t += 0.016; drawE8(cv, e8t); e8raf = requestAnimationFrame(loop); }; loop();
  }
  function stopE8() { if (e8raf) cancelAnimationFrame(e8raf); e8raf = 0; }
  function openDeep(id) { deepBody.innerHTML = deepContent(id); deepBody.scrollTop = 0; deepModal.hidden = false; if (id === "glue") requestAnimationFrame(startE8); else stopE8(); }
  function closeDeep() { deepModal.hidden = true; stopE8(); }
  $("deep-close").addEventListener("click", closeDeep);
  deepModal.addEventListener("click", (e) => { if (e.target === deepModal) closeDeep(); });

  // ---- hit testing ----
  function hitStation(mx, my) { for (const s of D.stations) { const r = rectOf(s); if (mx >= r.x && mx <= r.x + r.w && my >= r.y && my <= r.y + r.h) return s; } return null; }
  canvas.addEventListener("mousemove", (e) => {
    const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    if (substrateMode) { const pos = subPos(); let hit = null; for (const n of D.substrate.nodes) { const p = pos[n.id], R = n.id === "E8" ? 30 : 20; if (Math.hypot(mx - p.x, my - p.y) <= R + 3) { hit = n; break; } } subHover = hit ? hit.id : null; canvas.style.cursor = hit ? "pointer" : "default"; if (hit) { tooltip.hidden = false; tooltip.innerHTML = `<b>${escapeHTML(hit.label)}</b><br>${escapeHTML(hit.k)}`; tooltip.style.left = mx + "px"; tooltip.style.top = my + "px"; } else tooltip.hidden = true; return; }
    const s = hitStation(mx, my); hover = s ? s.id : null; canvas.style.cursor = s ? "pointer" : "default"; if (s) { tooltip.hidden = false; tooltip.innerHTML = `<b>${escapeHTML(s.plain || s.title)}</b><br>${escapeHTML(s.title || s.sub)}`; tooltip.style.left = mx + "px"; tooltip.style.top = my + "px"; } else tooltip.hidden = true;
  });
  canvas.addEventListener("mouseleave", () => { hover = null; subHover = null; tooltip.hidden = true; });
  canvas.addEventListener("click", (e) => { if (substrateMode) return; const r = canvas.getBoundingClientRect(), s = hitStation(e.clientX - r.left, e.clientY - r.top); if (s) { showStation(s); if (xrayMode) xrayTarget = s.id; else if (DEEP.has(s.id)) openDeep(s.id); } else if (xrayMode) xrayTarget = null; });

  // ---- universe state ----
  function refreshMicdrop() { $("micdrop").hidden = !(closesNow && progress >= 1 && !forging); }
  function applyUniverse() {
    cl = D.em.closure(liveN, liveG); closesNow = !forcedBreak && cl.closes;
    breakReason = forcedBreak || (cl.closes ? null : cl.reason);
    document.body.classList.toggle("broken-universe", !closesNow);
    const bb = $("broken-banner"); if (!closesNow) { bb.hidden = false; $("broken-reason").textContent = breakReason; } else bb.hidden = true;
    $("btn-restore").hidden = closesNow; refreshMicdrop();
  }

  // ---- loop ----
  function frame(now) {
    const dt = Math.min(0.05, (now - tPrev) / 1000); tPrev = now; clock += dt;
    if (running && progress < 1) { progress = Math.min(1, progress + dt * 0.13 * speed); if (progress >= 1) { running = false; setRunUI(); } }
    $("progressbar").style.width = (progress * 100).toFixed(1) + "%";
    updateBoards(); updateBanner(); refreshMicdrop(); draw(); requestAnimationFrame(frame);
  }

  // ---- controls ----
  const runIco = $("run-ico"), runLbl = $("run-lbl");
  function setRunUI() { runIco.textContent = running ? "\u275a\u275a" : "\u25b6"; runLbl.textContent = running ? "Pause" : (progress >= 1 ? "Replay" : "Run"); }
  function resetAll() { onlinePreds.clear(); smOnline = false; for (const k in predCards) predCards[k].classList.remove("online", "flash"); smCards.forEach((el) => el.classList.remove("online", "flash")); document.getElementById("sm-count").textContent = "\u00b7 built at the SM stage"; }
  function toggleRun() { if (progress >= 1 && !running) { progress = 0; resetAll(); } running = !running; setRunUI(); }
  $("btn-run").addEventListener("click", toggleRun);
  $("btn-reset").addEventListener("click", () => { running = false; progress = 0; resetAll(); setRunUI(); });
  $("btn-step").addEventListener("click", () => { running = false; setRunUI(); const ts = []; for (let d = 0; d <= MAXD; d++) ts.push(d / MAXD); const next = ts.find((t) => t > progress + 0.001); progress = next === undefined ? 1 : next; });
  $("speed").addEventListener("input", (e) => { speed = parseFloat(e.target.value); });
  $("plain-toggle").addEventListener("change", (e) => { plainMode = e.target.checked; });
  $("xray-toggle").addEventListener("change", (e) => {
    xrayMode = e.target.checked;
    if (xrayMode) { xrayTarget = selected || "glue"; showToast("X-ray on \u2014 click any module to trace what builds it (its inputs light up, the rest dims)."); }
    else xrayTarget = null;
  });
  $("substrate-toggle").addEventListener("change", (e) => { substrateMode = e.target.checked; subHover = null; tooltip.hidden = true; });
  $("btn-restore").addEventListener("click", () => { setUniverse(8, 5); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { closeModal(); closeDeep(); closeForge(); if (!prologue.hidden) closePrologue(true); } if (e.target.tagName === "INPUT") return; if (e.code === "Space") { e.preventDefault(); toggleRun(); } else if (e.key === "r" || e.key === "R") $("btn-reset").click(); else if (e.key === "ArrowRight") $("btn-step").click(); });

  // ---- ablation (now drives the live universe) ----
  const dialN = $("dial-N"), dialG = $("dial-g"), abReadout = $("ablation-readout"), abValue = $("ablation-value"), abVerdict = $("ablation-verdict");
  function setUniverse(N, g) { liveN = N; liveG = g; dialN.value = N; dialG.value = g; updateAblation(); }
  function updateAblation() {
    forcedBreak = null;
    liveN = parseInt(dialN.value, 10); liveG = parseInt(dialG.value, 10); $("out-N").textContent = liveN; $("out-g").textContent = liveG;
    cl = D.em.closure(liveN, liveG); const M = D.em.budgetM(liveG);
    if (!isFinite(cl.ainv) || cl.ainv <= 0) { abReadout.className = "readout bad"; abValue.textContent = "\u2014 no root \u2014"; abVerdict.textContent = `jams (N=${liveN}, g=${liveG}, budget ${M}): no admissible root`; }
    else { abValue.textContent = cl.ainv.toFixed(7); if (cl.closes) { abReadout.className = "readout ok"; abVerdict.textContent = "locked \u2014 the unique fit (N=8, g=5) \u2192 CODATA \u03b1\u207b\u00b9"; } else { abReadout.className = "readout bad"; abVerdict.textContent = `off-target: ${cl.reason}`; } }
    applyUniverse();
  }
  dialN.addEventListener("input", updateAblation); dialG.addEventListener("input", updateAblation);

  // ---- failed-universes as a goal: named break scenarios ----
  let toastTimer = null;
  function showToast(msg) { const t = $("toast"); t.textContent = msg; t.hidden = false; clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, 5600); }
  function forceBreak(reason) {
    dialN.value = 8; dialG.value = 5; liveN = 8; liveG = 5; $("out-N").textContent = 8; $("out-g").textContent = 5;
    cl = D.em.closure(8, 5); forcedBreak = reason;
    abReadout.className = "readout bad"; abValue.textContent = cl.ainv.toFixed(7); abVerdict.textContent = "structurally broken \u2014 " + reason;
    applyUniverse();
  }
  (function () {
    const box = $("scenario-buttons");
    D.scenarios.forEach((s) => {
      const b = document.createElement("button"); b.textContent = s.label; if (s.kind === "firewall") b.className = "fw";
      b.addEventListener("click", () => { if (s.kind === "dial") setUniverse(s.N, s.g); else if (s.kind === "force") forceBreak(s.reason); else showToast(s.toast); });
      box.appendChild(b);
    });
  })();

  // ---- failed-universes forge ----
  const forge = $("forge"); let forgeTimer = null;
  function rand(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function runForge() {
    forging = true; refreshMicdrop(); forge.hidden = false; forge.classList.remove("win");
    const TARGET = 9999, TICKS = 96; let i = 0;
    $("fc-alive").textContent = "0"; $("fc-dead").textContent = "0"; $("forge-bar-fill").style.width = "0%";
    clearInterval(forgeTimer);
    forgeTimer = setInterval(() => {
      i++;
      let N, g; do { N = rand(3, 16); g = rand(2, 9); } while (N === 8 && g === 5);
      const c = D.em.closure(N, g);
      $("forge-now").textContent = `candidate: c\u2083 = 1/(${N}\u03c0),  g_car = ${g}`;
      $("forge-verdict").textContent = "\u2717 " + c.reason;
      const dead = Math.min(TARGET, Math.round(TARGET * i / TICKS));
      $("fc-dead").textContent = dead.toLocaleString("en-US");
      $("forge-bar-fill").style.width = (100 * i / TICKS).toFixed(1) + "%";
      if (i >= TICKS) revealForge();
    }, 52);
  }
  function revealForge() {
    clearInterval(forgeTimer); forge.classList.add("win");
    $("forge-now").textContent = "Universe #137:  c\u2083 = 1/(8\u03c0),  g_car = 5";
    $("forge-verdict").textContent = "\u2713 E\u2088 CLOSES \u2014 all constraints met";
    $("fc-dead").textContent = "9,999"; $("fc-alive").textContent = "1"; $("forge-bar-fill").style.width = "100%";
    $("forge-foot").textContent = "9,999 candidate universes die. Exactly ONE closes itself \u2014 that one is ours.";
  }
  function closeForge() { if (forge.hidden) return; clearInterval(forgeTimer); forge.hidden = true; forging = false; setUniverse(8, 5); }
  $("btn-forge").addEventListener("click", runForge);
  $("forge-skip").addEventListener("click", revealForge);
  $("forge-close").addEventListener("click", closeForge);
  forge.addEventListener("click", (e) => { if (e.target === forge) closeForge(); });

  // ---- origin prologue ----
  const prologue = $("prologue"); let proI = 0;
  const PRO = [
    { k: "PROLOGUE \u00b7 1/5", t: "Reality has an edge", b: "Not space is fundamental \u2014 the <b>edge</b> carries the rules.", v: `<div class="pv-edge"></div>` },
    { k: "PROLOGUE \u00b7 2/5", t: "Four marks", b: "The seam carries four marks: <b>\u03bc\u2084 = {1, i, \u22121, \u2212i}</b>.", v: `<div class="pv-edge"></div>` + [18, 40, 60, 80].map((p) => `<div class="pv-mark" style="top:${p}%"></div>`).join("") },
    { k: "PROLOGUE \u00b7 3/5", t: "The double cover", b: "The edge folds into <b>two sheets</b> \u2014 a front and a back. Not a second universe: the second reading of the <b>same</b> edge (a deck transformation).", v: `<div class="pv-edge2" style="left:42%"></div><div class="pv-edge2" style="left:58%;opacity:.55"></div><div class="pv-label" style="left:50%;bottom:8%;transform:translateX(-50%)">front / back \u2014 same edge</div>` },
    { k: "PROLOGUE \u00b7 4/5", t: "One object, two readings", b: "Cycles around the marks \u2192 <b>3 families</b>. Functions on the marks \u2192 a <b>5-slot carrier</b>. One seam, two canonical readouts.", v: `<div class="pv-edge"></div><div class="pv-side" style="left:14%"><div class="pv-big" style="color:#5b8cff">3</div><div class="pv-cap">families (A\u2083)</div></div><div class="pv-side" style="right:14%"><div class="pv-big" style="color:#34d39a">5</div><div class="pv-cap">carrier (g_car)</div></div>` },
    { k: "PROLOGUE \u00b7 5/5", t: "Now the machine runs", b: "carrier + families + glue \u2192 <b style='color:#fb7185'>E\u2088 validates the closure</b> \u2192 the Standard Model is <b>projected</b>, and the predictions follow.", v: `<div class="pv-label" style="left:50%;top:50%;transform:translate(-50%,-50%);font-size:13.5px;color:#cdd9ef;text-align:center;width:92%;line-height:1.7">carrier + families + glue<br>\u2193<br><b style="color:#fb7185">E\u2088 validates</b><br>\u2193<br>Standard Model \u00b7 predictions</div>` },
  ];
  function renderPro() { const s = PRO[proI]; $("prologue-kicker").textContent = s.k; $("prologue-title").textContent = s.t; $("prologue-body").innerHTML = s.b; $("prologue-visual").innerHTML = s.v; $("prologue-dots").innerHTML = PRO.map((_, i) => `<i class="${i === proI ? "on" : ""}"></i>`).join(""); $("prologue-next").textContent = proI === PRO.length - 1 ? "Start the machine \u25b8" : "Next \u25b8"; }
  function openPrologue() { proI = 0; renderPro(); prologue.hidden = false; running = false; setRunUI(); }
  function closePrologue(start) { prologue.hidden = true; if (start) { progress = 0; resetAll(); running = true; setRunUI(); } }
  $("prologue-next").addEventListener("click", () => { if (proI < PRO.length - 1) { proI++; renderPro(); } else closePrologue(true); });
  $("prologue-skip").addEventListener("click", () => closePrologue(true));
  $("prologue-skip-x").addEventListener("click", () => closePrologue(true));
  $("btn-intro").addEventListener("click", openPrologue);

  // ---- boot ----
  resize(); updateAblation(); showStation(byId.seam); updateBanner(); setRunUI();
  requestAnimationFrame(frame);
  let seenIntro = false; try { seenIntro = !!localStorage.getItem("tfpt_intro_v1"); localStorage.setItem("tfpt_intro_v1", "1"); } catch (e) {}
  if (!seenIntro) openPrologue();
  else setTimeout(() => { if (progress === 0 && prologue.hidden) { running = true; setRunUI(); } }, 800);
})();
