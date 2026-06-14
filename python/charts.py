"""
Chart generator for "Inheriting Discretion: What Monetary Rules Prescribe for the Warsh Fed"
Produces:
  output/widgets/  — Chart.js HTML embeds for the website
  output/figures/  — Static PNGs for vault and general use
"""

import json
import pathlib
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT    = pathlib.Path(__file__).parent.parent
WIDGETS = ROOT / "output" / "widgets";  WIDGETS.mkdir(parents=True, exist_ok=True)
FIGURES = ROOT / "output" / "figures"; FIGURES.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(ROOT / "output" / "data" / "rules_export.csv", parse_dates=["date"])
df = df[df["date"] >= "2018-01-01"].copy().reset_index(drop=True)

# ── Palette (mirrors JS_PALETTE in 03_figures.R) ─────────────────────────────

PAL = {
    "actual":  "#1C1C1A",
    "taylor1": "#185FA5",
    "taylor2": "#1D9E75",
    "dev_pos": "#D85A30",
    "dev_neg": "#185FA5",
    "ngdp":    "#1C1C1A",
    "trend":   "#185FA5",
    "grid":    "#e5e5e5",
    "muted":   "#888888",
    "covid":   "#b9d2eb",
}

# ── HTML helper functions (mirrors 03_figures.R helpers) ─────────────────────

def date_labels(dates):
    return [f"{d.year}-Q{(d.month - 1) // 3 + 1}" for d in dates]

def js_array(vals, digits=2):
    parts = [
        "null" if (v is None or (isinstance(v, float) and np.isnan(v)))
        else f"{round(float(v), digits):.{digits}f}"
        for v in vals
    ]
    return "[" + ", ".join(parts) + "]"

def stat_card(label, value):
    return (
        '<div style="background:var(--bg-soft);border:1px solid var(--border);'
        'border-radius:6px;padding:8px 12px;">'
        f'<div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;'
        f'letter-spacing:.05em;margin-bottom:2px;">{label}</div>'
        f'<div style="font-size:1.05rem;font-weight:600;color:var(--text);">{value}</div>'
        '</div>'
    )

def stat_cards(cards, ncols=3):
    return (
        f'<div style="display:grid;grid-template-columns:repeat({ncols},1fr);'
        f'gap:8px;margin-bottom:12px;">' + "".join(cards) + '</div>\n'
    )

def fig_header(context, title, subtitle):
    return (
        f'<p style="margin:0 0 3px;font-size:10px;letter-spacing:0.13em;'
        f'text-transform:uppercase;color:var(--muted);">{context}</p>\n'
        f'<p style="margin:0 0 3px;font-size:18px;font-weight:500;'
        f'color:var(--text);line-height:1.3;">{title}</p>\n'
        f'<p style="margin:0 0 18px;font-size:12px;color:var(--muted);">{subtitle}</p>\n'
    )

def legend_line(data_k, label):
    return (
        f'<span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);">'
        f'<span data-k="{data_k}" style="display:inline-block;width:20px;height:2px;'
        f'background:#888;border-radius:1px;flex-shrink:0;"></span>{label}</span>'
    )

def legend_dashed(data_k, label):
    return (
        f'<span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);">'
        f'<span data-k="{data_k}" data-dash="1" style="display:inline-block;width:20px;height:0;'
        f'border-bottom:2px dashed #888;flex-shrink:0;"></span>{label}</span>'
    )

def legend_row(items):
    return '<div style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:12px;">' + "".join(items) + '</div>\n'

def footer():
    return (
        '<div style="margin-top:14px;padding-top:10px;border-top:1px solid var(--border);'
        'display:flex;justify-content:space-between;font-size:10px;color:var(--muted);letter-spacing:0.02em;">'
        '<span>Source: <a href="https://fred.stlouisfed.org/" target="_blank" rel="noopener" '
        'style="color:inherit;text-decoration:underline;">Federal Reserve Economic Data (FRED)</a>, '
        'CBO. Author&#8217;s calculations.</span>'
        '<a href="https://nikkhosravipour.com" target="_blank" rel="noopener" '
        'style="color:inherit;text-decoration:underline;">nikkhosravipour.com</a>'
        '</div>\n'
    )

# ── JS building blocks (mirrors JS constants in 03_figures.R) ─────────────────

JS_PALETTE = """  function palette() {
    var light = document.documentElement.classList.contains('is-light');
    return {
      tick:    light ? 'rgba(0,0,0,0.42)'       : 'rgba(255,255,255,0.5)',
      grid:    light ? 'rgba(0,0,0,0.06)'       : 'rgba(255,255,255,0.07)',
      yTick:   light ? 'rgba(0,0,0,0.65)'       : 'rgba(255,255,255,0.7)',
      actual:  light ? '#1C1C1A'                : '#E8E6DF',
      taylor1: light ? '#185FA5'                : '#60a5fa',
      taylor2: light ? '#1D9E75'                : '#34d399',
      dev_pos: light ? '#D85A30'                : '#f87171',
      dev_neg: light ? '#185FA5'                : '#60a5fa',
      ngdp:    light ? '#1C1C1A'                : '#E8E6DF',
      trend:   light ? '#185FA5'                : '#60a5fa',
      covid:   light ? 'rgba(185,210,235,0.35)' : 'rgba(96,165,250,0.12)',
      text:    light ? '#1C1C1A'                : '#E8E6DF',
      muted:   light ? 'rgba(0,0,0,0.50)'       : 'rgba(255,255,255,0.55)',
    };
  }"""

JS_SWATCH = "    scope.querySelectorAll('[data-k]').forEach(function(sw) { if (sw.dataset.dash) sw.style.borderBottomColor = c[sw.dataset.k]; else sw.style.background = c[sw.dataset.k]; });"

JS_CLOSE = """  window.__chartjs.then(function() {
    render();
    new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  });
})();
</script>"""

COVID_PLUGIN = """    var covidPlugin = {
      id: 'covidShade',
      afterDraw: function(chart) {
        var ctx = chart.ctx, ca = chart.chartArea, xs = chart.scales.x;
        var i1 = labels.indexOf('2020-Q1'), i2 = labels.indexOf('2022-Q1');
        if (i1 < 0 || i2 < 0) return;
        var px1 = xs.getPixelForValue(i1), px2 = xs.getPixelForValue(i2);
        ctx.save(); ctx.fillStyle = c.covid;
        ctx.fillRect(px1, ca.top, px2 - px1, ca.bottom - ca.top);
        ctx.restore();
      }
    };"""

X_SCALE_QTR = """          x: {
            border: { display: false },
            grid: { color: c.grid },
            ticks: { color: c.tick, font: { size: 10, family: 'system-ui, sans-serif' },
              maxRotation: 0, autoSkip: false,
              callback: function(val, i) { return i % 4 === 0 ? labels[i] : null; } }
          }"""

CHART_OPTIONS_HEAD = """      options: {
        responsive: true, maintainAspectRatio: false, animation: false,
        layout: { padding: { top: 26, right: 20, left: 0, bottom: 4 } },
        interaction: { mode: 'index', intersect: false },
        plugins: { legend: { display: false }, title: { display: false } },"""

def js_open(cid):
    return (
        "</figure>\n<script>\n(function () {\n"
        "  window.__chartjs = window.__chartjs || new Promise(function(resolve) {\n"
        "    if (window.Chart) return resolve();\n"
        "    var s = document.createElement('script');\n"
        "    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js';\n"
        "    s.onload = resolve; document.head.appendChild(s);\n"
        "  });\n"
        f"  var canvas = document.getElementById('{cid}');\n"
        "  if (!canvas) return;\n"
        "  var scope = canvas.closest('figure');\n"
        "  var chart;\n"
    )

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — FFR vs. Taylor Rule
# ═══════════════════════════════════════════════════════════════════════════════

lbls    = date_labels(df["date"])
lbls_js = json.dumps(lbls)

peak_dev   = float((df["taylor_base"] - df["FEDFUNDS"]).max())
peak_dev_q = lbls[(df["taylor_base"] - df["FEDFUNDS"]).idxmax()]
cur_ffr    = float(df["FEDFUNDS"].iloc[-1])
cur_taylor = float(df["taylor_base"].iloc[-1])

ffr_js     = js_array(df["FEDFUNDS"])
taylor1_js = js_array(df["taylor_base"])
taylor2_js = js_array(df["taylor_orig"])

# ── Figure 1 HTML ─────────────────────────────────────────────────────────────

html_fig1 = (
    '<figure class="chart-embed" style="margin:0; font-family:var(--font-body);">\n'
    + fig_header(
        "Federal Reserve · Policy Brief · 2018–2026",
        "Federal Funds Rate vs. Taylor Rule Prescriptions",
        "Effective federal funds rate and rules-based benchmarks · percent · quarterly"
    )
    + stat_cards([
        stat_card("Peak deviation (2022-Q1)", f"+{peak_dev:.1f}pp"),
        stat_card("Taylor implied (2026-Q1)", f"{cur_taylor:.2f}%"),
        stat_card("Actual FFR (2026-Q1)",     f"{cur_ffr:.2f}%"),
    ], ncols=3)
    + legend_row([
        legend_line("actual",  "Actual EFFR"),
        legend_dashed("taylor1", "Taylor Rule (r*=0.5%)"),
        legend_dashed("taylor2", "Taylor Rule (r*=2.0%, 1993 original)"),
    ])
    + '<div style="position:relative; width:100%; height:260px;">\n'
    + '<canvas id="warsh-fig1" role="img" aria-label="Federal funds rate vs Taylor Rule, 2018-2026"></canvas>\n'
    + '</div>\n'
    + footer()
    + js_open("warsh-fig1")
    + JS_PALETTE + "\n"
    + "  function render() {\n"
    + "    if (!window.Chart) return;\n"
    + "    var c = palette();\n"
    + JS_SWATCH + "\n"
    + f"    var labels = {lbls_js};\n"
    + COVID_PLUGIN + "\n"
    + "    if (chart) chart.destroy();\n"
    + "    chart = new Chart(canvas, {\n"
    + "      type: 'line',\n"
    + "      plugins: [covidPlugin],\n"
    + "      data: { labels: labels, datasets: [\n"
    + f"        {{ label: 'Actual EFFR', data: {ffr_js}, borderColor: c.actual, borderWidth: 3, pointRadius: 0, tension: 0.3, fill: false }},\n"
    + f"        {{ label: 'Taylor (r*=0.5%)', data: {taylor1_js}, borderColor: c.taylor1, borderWidth: 1.5, borderDash: [6,3], pointRadius: 0, tension: 0.3, fill: false }},\n"
    + f"        {{ label: 'Taylor (r*=2.0%)', data: {taylor2_js}, borderColor: c.taylor2, borderWidth: 1.5, borderDash: [3,3], pointRadius: 0, tension: 0.3, fill: false }}\n"
    + "      ]},\n"
    + CHART_OPTIONS_HEAD + "\n"
    + "        scales: {\n"
    + X_SCALE_QTR + ",\n"
    + "          y: { border: { display: false }, grid: { color: c.grid },\n"
    + "            ticks: { color: c.yTick, font: { size: 10, family: 'system-ui, sans-serif' },\n"
    + "              callback: function(v) { return v + '%'; } } }\n"
    + "        }\n"
    + "      }\n"
    + "    });\n"
    + "  }\n"
    + JS_CLOSE
)

(WIDGETS / "fig1_taylor_vs_actual.html").write_text(html_fig1)

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — NGDP Level vs. 4% Trend
# ═══════════════════════════════════════════════════════════════════════════════

peak_gap     = float(df["ngdp_gap"].max())
peak_gap_q   = lbls[df["ngdp_gap"].idxmax()]
cur_gap      = float(df["ngdp_gap"].iloc[-1])
cur_ngdp     = float(df["GDP"].iloc[-1])
cur_trend    = float(df["ngdp_trend"].iloc[-1])
overshoot_bn = cur_ngdp - cur_trend

gdp_js   = js_array(df["GDP"], digits=1)
trend_js = js_array(df["ngdp_trend"], digits=1)
gap_js   = js_array(df["ngdp_gap"], digits=2)

# ── Figure 2 HTML ─────────────────────────────────────────────────────────────

html_fig2 = (
    '<figure class="chart-embed" style="margin:0; font-family:var(--font-body);">\n'
    + fig_header(
        "Federal Reserve · Policy Brief · 2019–2026",
        "Nominal GDP vs. 4% Trend Path from 2019 Q4",
        "Actual nominal spending vs. rules-based benchmark · billions USD · quarterly"
    )
    + stat_cards([
        stat_card("Current NGDP gap",    f"+{cur_gap:.1f}%"),
        stat_card("Overshoot (billions)", f"&#36;{overshoot_bn:,.0f}bn"),  # &#36; = literal $, kept out of source so markdown editors don't mangle the embed
        stat_card("Peak gap",            f"+{peak_gap:.1f}% ({peak_gap_q})"),
    ], ncols=3)
    + legend_row([
        legend_line("ngdp",  "Nominal GDP (actual)"),
        legend_dashed("trend", "4% trend from 2019 Q4"),
    ])
    + '<div style="position:relative; width:100%; height:260px;">\n'
    + '<canvas id="warsh-fig2" role="img" aria-label="Nominal GDP vs 4% trend path, 2019-2026"></canvas>\n'
    + '</div>\n'
    + footer()
    + js_open("warsh-fig2")
    + JS_PALETTE + "\n"
    + "  function render() {\n"
    + "    if (!window.Chart) return;\n"
    + "    var c = palette();\n"
    + JS_SWATCH + "\n"
    + f"    var labels = {lbls_js};\n"
    + "    if (chart) chart.destroy();\n"
    + "    chart = new Chart(canvas, {\n"
    + "      type: 'line',\n"
    + "      data: { labels: labels, datasets: [\n"
    + f"        {{ label: 'Nominal GDP', data: {gdp_js}, borderColor: c.ngdp, borderWidth: 3, pointRadius: 0, tension: 0.3, fill: false }},\n"
    + f"        {{ label: '4% trend', data: {trend_js}, borderColor: c.trend, borderWidth: 1.5, borderDash: [6,3], pointRadius: 0, tension: 0.3, fill: false }}\n"
    + "      ]},\n"
    + CHART_OPTIONS_HEAD + "\n"
    + "        scales: {\n"
    + X_SCALE_QTR + ",\n"
    + "          y: { border: { display: false }, grid: { color: c.grid },\n"
    + "            ticks: { color: c.yTick, font: { size: 10, family: 'system-ui, sans-serif' },\n"
    + "              callback: function(v) { return String.fromCharCode(36) + (v/1000).toFixed(0) + 'T'; } } }\n"  # charCode 36 = $, no literal $ in source so editors can't mangle
    + "        }\n"
    + "      }\n"
    + "    });\n"
    + "  }\n"
    + JS_CLOSE
)

(WIDGETS / "fig2_ngdp_level.html").write_text(html_fig2)

# ═══════════════════════════════════════════════════════════════════════════════
# PNGs — matplotlib, matching 04_pngs.R visual style
# ═══════════════════════════════════════════════════════════════════════════════

plt.rcParams.update({
    "font.family":  "sans-serif",
    "font.size":    8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

def png_footer(fig):
    fig.text(0.0, -0.03,
             "Source: FRED, CBO. Author's calculations.  |  nikkhosravipour.com",
             fontsize=6, color=PAL["muted"], ha="left")

def style_ax(ax):
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(PAL["muted"])
    ax.yaxis.set_tick_params(length=0)
    ax.tick_params(colors=PAL["muted"], labelsize=7)
    for y in ax.get_yticks():
        ax.axhline(y, color=PAL["grid"], lw=0.7, zorder=0)

# ── Figure 1 PNG ──────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(7.5, 3.5), dpi=120, facecolor="white")

# COVID shading
covid_start = pd.Timestamp("2020-01-01")
covid_end   = pd.Timestamp("2022-01-01")
ax.axvspan(covid_start, covid_end, color=PAL["covid"], alpha=0.35, zorder=0, label="_nolegend_")

ax.axhline(0, lw=0.8, ls="--", color=PAL["muted"], zorder=1)

ax.plot(df["date"], df["taylor_orig"],  color=PAL["taylor2"], lw=1.2, ls=(0,(3,3)), label="Taylor (r*=2.0%, 1993)", zorder=2)
ax.plot(df["date"], df["taylor_base"],  color=PAL["taylor1"], lw=1.4, ls="--",      label="Taylor (r*=0.5%)", zorder=2)
ax.plot(df["date"], df["FEDFUNDS"],     color=PAL["actual"],  lw=2.2,               label="Actual EFFR", zorder=3)

style_ax(ax)
ax.set_ylabel("Rate (%)", color=PAL["muted"], fontsize=7)
ax.legend(frameon=False, fontsize=7, loc="upper left")

ax.set_title("Federal Reserve Policy vs. Taylor Rule Prescriptions",
             loc="left", fontweight="bold", fontsize=9, pad=18)
ax.text(0, 1.045, "Effective federal funds rate and rules-based benchmarks · percent · quarterly",
        transform=ax.transAxes, fontsize=7, color=PAL["muted"])

png_footer(fig)
plt.tight_layout()
fig.savefig(FIGURES / "fig1_taylor_vs_actual.png", dpi=120, bbox_inches="tight", facecolor="white")
plt.close()

# ── Figure 2 PNG ──────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(7.5, 3.5), dpi=120, facecolor="white")

ax.fill_between(df["date"], df["GDP"], df["ngdp_trend"],
                where=df["GDP"] >= df["ngdp_trend"],
                color=PAL["dev_pos"], alpha=0.18, zorder=1, label="_nolegend_")
ax.fill_between(df["date"], df["GDP"], df["ngdp_trend"],
                where=df["GDP"] < df["ngdp_trend"],
                color=PAL["dev_neg"], alpha=0.18, zorder=1, label="_nolegend_")

ax.plot(df["date"], df["ngdp_trend"], color=PAL["trend"], lw=1.4, ls="--", label="4% trend (2019 Q4 baseline)", zorder=2)
ax.plot(df["date"], df["GDP"],        color=PAL["ngdp"],  lw=2.2,          label="Nominal GDP (actual)", zorder=3)

style_ax(ax)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1000:.0f}T"))
ax.set_ylabel("Nominal GDP", color=PAL["muted"], fontsize=7)
ax.legend(frameon=False, fontsize=7, loc="upper left")

ax.set_title("Nominal GDP vs. 4% Trend Path from 2019 Q4",
             loc="left", fontweight="bold", fontsize=9, pad=18)
ax.text(0, 1.045, "Actual nominal spending vs. rules-based benchmark · billions USD · quarterly",
        transform=ax.transAxes, fontsize=7, color=PAL["muted"])

png_footer(fig)
plt.tight_layout()
fig.savefig(FIGURES / "fig2_ngdp_level.png", dpi=120, bbox_inches="tight", facecolor="white")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 0 — Hook: Taylor deviation (bars) + NGDP gap % (line, right axis)
# ═══════════════════════════════════════════════════════════════════════════════
# Mirrors the hook figure approach from the taylor-rule project (fig0_hook):
# dual-axis, policy gap left, macro consequence right, COVID shading, one view.

df["taylor_dev_base"] = df["taylor_base"] - df["FEDFUNDS"]

peak_dev_hook = float(df["taylor_dev_base"].max())
peak_dev_q    = lbls[int(df["taylor_dev_base"].idxmax())]
peak_ngdp     = float(df["ngdp_gap"].max())
cur_ngdp_gap  = float(df["ngdp_gap"].iloc[-1])

dev_js    = js_array(df["taylor_dev_base"])
ngdp_gap_js = js_array(df["ngdp_gap"])

ZERO_LINE_PLUGIN = """    var zeroLinePlugin = {
      id: 'zeroLine',
      afterDraw: function(chart) {
        var ctx = chart.ctx, ca = chart.chartArea, ys = chart.scales.y;
        var y0 = ys.getPixelForValue(0);
        ctx.save();
        ctx.strokeStyle = c.tick; ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.moveTo(ca.left, y0); ctx.lineTo(ca.right, y0); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = c.tick;
        ctx.font = '9px system-ui, sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText('Rules-based prescription', ca.right - 4, y0 - 4);
        ctx.restore();
      }
    };"""

# ── Hook HTML ─────────────────────────────────────────────────────────────────

html_hook = (
    '<figure class="chart-embed" style="margin:0; font-family:var(--font-body);">\n'
    + fig_header(
        "Federal Reserve · Policy Brief · 2018–2026",
        "Two Measures. One Verdict.",
        "Taylor Rule deviation (bars, left) and NGDP gap vs. 4% trend (line, right) · quarterly"
    )
    + stat_cards([
        stat_card("Peak Taylor gap", f"+{peak_dev_hook:.1f}pp ({peak_dev_q})"),
        stat_card("NGDP overshoot (2026-Q1)", f"+{cur_ngdp_gap:.1f}%"),
        stat_card("Actual FFR (2026-Q1)", f"{cur_ffr:.2f}%"),
    ], ncols=3)
    + legend_row([
        '<span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);">'
        '<span data-k="dev_pos" style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#888;flex-shrink:0;"></span>Too loose (above Taylor prescription)</span>',
        '<span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);">'
        '<span data-k="dev_neg" style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#888;flex-shrink:0;"></span>Too tight (below prescription)</span>',
        legend_line("taylor1", "NGDP gap vs. 4% trend (right)"),
    ])
    + '<div style="position:relative; width:100%; height:260px;">\n'
    + '<canvas id="warsh-fig0" role="img" aria-label="Taylor Rule deviation bars and NGDP gap line, 2018-2026"></canvas>\n'
    + '</div>\n'
    + footer()
    + js_open("warsh-fig0")
    + JS_PALETTE + "\n"
    + "  function render() {\n"
    + "    if (!window.Chart) return;\n"
    + "    var c = palette();\n"
    + JS_SWATCH + "\n"
    + f"    var labels = {lbls_js};\n"
    + f"    var vals   = {dev_js};\n"
    + COVID_PLUGIN + "\n"
    + ZERO_LINE_PLUGIN + "\n"
    + "    if (chart) chart.destroy();\n"
    + "    chart = new Chart(canvas, {\n"
    + "      type: 'bar',\n"
    + "      plugins: [covidPlugin, zeroLinePlugin],\n"
    + "      data: { labels: labels, datasets: [\n"
    + f"        {{ label: 'Taylor deviation', data: {dev_js},\n"
    + "          backgroundColor: vals.map(function(v) { return v > 0 ? c.dev_pos : c.dev_neg; }),\n"
    + "          borderRadius: 2, yAxisID: 'y' },\n"
    + f"        {{ label: 'NGDP gap (%)', data: {ngdp_gap_js},\n"
    + "          type: 'line', borderColor: c.taylor1, borderWidth: 2,\n"
    + "          pointRadius: 0, tension: 0.3, fill: false, yAxisID: 'y1' }\n"
    + "      ]},\n"
    + "      options: {\n"
    + "        responsive: true, maintainAspectRatio: false, animation: false,\n"
    + "        layout: { padding: { top: 26, right: 20, left: 0, bottom: 4 } },\n"
    + "        interaction: { mode: 'index', intersect: false },\n"
    + "        plugins: { legend: { display: false }, title: { display: false } },\n"
    + "        scales: {\n"
    + X_SCALE_QTR + ",\n"
    + "          y: { position: 'left', border: { display: false }, grid: { color: c.grid },\n"
    + "            ticks: { color: c.yTick, font: { size: 10, family: 'system-ui, sans-serif' },\n"
    + "              callback: function(v) { return v + 'pp'; } } },\n"
    + "          y1: { position: 'right', border: { display: false }, grid: { drawOnChartArea: false },\n"
    + "            ticks: { color: c.taylor1, font: { size: 10, family: 'system-ui, sans-serif' },\n"
    + "              callback: function(v) { return v + '%'; } } }\n"
    + "        }\n"
    + "      }\n"
    + "    });\n"
    + "  }\n"
    + JS_CLOSE
)

(WIDGETS / "fig0_hook.html").write_text(html_hook)

# ── Hook PNG ──────────────────────────────────────────────────────────────────

fig, ax_left = plt.subplots(figsize=(7.5, 3.5), dpi=120, facecolor="white")
ax_right = ax_left.twinx()

# COVID shading
ax_left.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2022-01-01"),
                color=PAL["covid"], alpha=0.35, zorder=0)

# Zero line on left axis
ax_left.axhline(0, lw=0.8, ls="--", color=PAL["muted"], zorder=1)
ax_left.text(df["date"].iloc[-1], 0.15, "Rules-based prescription",
             fontsize=6, color=PAL["muted"], ha="right")

# Bars: Taylor deviation
colors_bar = [PAL["dev_pos"] if v >= 0 else PAL["dev_neg"] for v in df["taylor_dev_base"]]
bar_width   = pd.Timedelta(days=60)
ax_left.bar(df["date"], df["taylor_dev_base"], width=bar_width,
            color=colors_bar, alpha=0.85, zorder=2)

# Line: NGDP gap (right axis)
ax_right.plot(df["date"], df["ngdp_gap"], color=PAL["taylor1"], lw=2.0, zorder=3,
              label="NGDP gap vs. 4% trend (%)")

# Annotate peak Taylor deviation
peak_idx = df["taylor_dev_base"].idxmax()
ax_left.annotate(
    f"{peak_dev_q}\n+{peak_dev_hook:.1f}pp",
    xy=(df["date"].iloc[peak_idx], df["taylor_dev_base"].iloc[peak_idx]),
    xytext=(0, 10), textcoords="offset points",
    ha="center", fontsize=6, color=PAL["dev_pos"], fontweight="bold"
)

# Style left axis
style_ax(ax_left)
ax_left.set_ylabel("Taylor deviation (pp)", color=PAL["muted"], fontsize=7)
ax_left.tick_params(axis="y", colors=PAL["muted"], labelsize=7)

# Style right axis
ax_right.spines["top"].set_visible(False)
ax_right.spines["left"].set_visible(False)
ax_right.spines["bottom"].set_visible(False)
ax_right.spines["right"].set_color(PAL["taylor1"])
ax_right.tick_params(axis="y", colors=PAL["taylor1"], labelsize=7)
ax_right.set_ylabel("NGDP gap vs. trend (%)", color=PAL["taylor1"], fontsize=7)
ax_right.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))

# Legends
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor=PAL["dev_pos"], alpha=0.85, label="Too loose (above Taylor prescription)"),
    Patch(facecolor=PAL["dev_neg"], alpha=0.85, label="Too tight (below prescription)"),
    Line2D([0], [0], color=PAL["taylor1"], lw=2, label="NGDP gap vs. 4% trend (right)"),
]
ax_left.legend(handles=legend_elements, frameon=False, fontsize=6.5, loc="upper left")

ax_left.set_title("Two Measures. One Verdict.", loc="left", fontweight="bold", fontsize=9, pad=18)
ax_left.text(0, 1.045,
             "Taylor Rule deviation (bars, left) and NGDP gap vs. 4% trend (line, right) · quarterly",
             transform=ax_left.transAxes, fontsize=7, color=PAL["muted"])

png_footer(fig)
plt.tight_layout()
fig.savefig(FIGURES / "fig0_hook.png", dpi=120, bbox_inches="tight", facecolor="white")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# Verification
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── Output verification ───────────────────────────────────────────────────")
for name, path in [
    ("fig0_hook.html",             WIDGETS / "fig0_hook.html"),
    ("fig1_taylor_vs_actual.html", WIDGETS / "fig1_taylor_vs_actual.html"),
    ("fig2_ngdp_level.html",       WIDGETS / "fig2_ngdp_level.html"),
    ("fig0_hook.png",              FIGURES / "fig0_hook.png"),
    ("fig1_taylor_vs_actual.png",  FIGURES / "fig1_taylor_vs_actual.png"),
    ("fig2_ngdp_level.png",        FIGURES / "fig2_ngdp_level.png"),
]:
    size = path.stat().st_size if path.exists() else 0
    print(f"  {name:<38}  {size:>8,} bytes  {'[OK]' if size > 0 else '[MISSING]'}")
print("─────────────────────────────────────────────────────────────────────────\n")
