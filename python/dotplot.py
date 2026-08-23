"""
Dot-plot chart for "Pattern and Pretence: The Dot the Chairman Declined to Submit".

Two FOMC median-dot projections against the rate that realized. December 2015 projected
the policy rate climbing toward 3.3% by 2018; the rate stopped short and was cut. March
2021 projected 0.1% through the 2021 inflation; the rate realized above 4%. The dots miss
in both directions. Three lines, nothing else.

Produces (per chart-embed-contract.md):
  output/widgets/fig0_dotgap.html       — raw Chart.js embed
  output/widgets/fig0_dotgap.embed.md   — ```html-embed fenced version (paste into personal.site)
  output/figures/fig0_dotgap.png        — static PNG for the vault

DATA PROVENANCE
  Median dots: FOMC Summary of Economic Projections, "Federal funds rate" median row,
  federalreserve.gov/monetarypolicy/fomcprojtabl{YYYYMMDD}.htm (Dec 2015; Mar 2021).
  Realized rate: effective federal funds rate, quarterly (FRED FEDFUNDS / warsh-fed series).
"""

import pathlib, json
import matplotlib.pyplot as plt

ROOT    = pathlib.Path(__file__).parent.parent
WIDGETS = ROOT / "output" / "widgets";  WIDGETS.mkdir(parents=True, exist_ok=True)
FIGURES = ROOT / "output" / "figures"; FIGURES.mkdir(parents=True, exist_ok=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
# Two median-dot vintages (year -> median FFR %), plotted at each target year-end.
HAWK = {2015: 0.4, 2016: 1.4, 2017: 2.4, 2018: 3.3}   # Dec 2015 — projected too high
DOVE = {2021: 0.1, 2022: 0.1, 2023: 0.1}              # Mar 2021 — projected too low

# Realized effective federal funds rate, quarterly, 2015 Q1 -> 2026 Q1.
REALIZED = [0.11,0.12,0.14,0.16, 0.36,0.37,0.40,0.45, 0.70,0.95,1.15,1.20,
            1.51,1.82,1.95,2.27, 2.41,2.38,2.04,1.55, 0.65,0.08,0.09,0.09,
            0.07,0.08,0.08,0.08, 0.20,1.21,2.56,4.10, 4.65,5.08,5.33,5.33,
            5.33,5.33,5.13,4.48, 4.33,4.33,4.22,3.72, 3.64]
REAL_X = [round(2015.0 + i * 0.25, 2) for i in range(len(REALIZED))]

def pts(d):
    return [{"x": round(y + 0.95, 2), "y": v} for y, v in sorted(d.items())]

PAL = {"real": "#1C1C1A", "hawk": "#A32D2D", "dove": "#185FA5", "grid": "#e5e5e5", "muted": "#888888"}

# ── HTML helpers (verbatim from charts.py, matches the live widgets) ───────────
def stat_card(label, value):
    return ('<div style="background:var(--bg-soft);border:1px solid var(--border);'
            'border-radius:6px;padding:8px 12px;">'
            f'<div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;'
            f'letter-spacing:.05em;margin-bottom:2px;">{label}</div>'
            f'<div style="font-size:1.05rem;font-weight:600;color:var(--text);">{value}</div></div>')

def stat_cards(cards, ncols=2):
    return (f'<div style="display:grid;grid-template-columns:repeat({ncols},1fr);'
            f'gap:8px;margin-bottom:12px;">' + "".join(cards) + '</div>\n')

def fig_header(context, title, subtitle):
    return (f'<p style="margin:0 0 3px;font-size:10px;letter-spacing:0.13em;'
            f'text-transform:uppercase;color:var(--muted);">{context}</p>\n'
            f'<p style="margin:0 0 3px;font-size:18px;font-weight:500;'
            f'color:var(--text);line-height:1.3;">{title}</p>\n'
            f'<p style="margin:0 0 18px;font-size:12px;color:var(--muted);">{subtitle}</p>\n')

def legend_line(data_k, label):
    return (f'<span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);">'
            f'<span data-k="{data_k}" style="display:inline-block;width:20px;height:2px;'
            f'background:#888;border-radius:1px;flex-shrink:0;"></span>{label}</span>')

def legend_row(items):
    return '<div style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:12px;">' + "".join(items) + '</div>\n'

def footer():
    return ('<div style="margin-top:14px;padding-top:10px;border-top:1px solid var(--border);'
            'display:flex;flex-wrap:wrap;gap:4px;justify-content:space-between;font-size:10px;color:var(--muted);letter-spacing:0.02em;">'
            '<span>Source: FOMC Summary of Economic Projections, median federal funds rate (dots); '
            '<a href="https://fred.stlouisfed.org/series/FEDFUNDS" target="_blank" rel="noopener" '
            'style="color:inherit;text-decoration:underline;">FRED</a> (realized rate). Author&#8217;s calculations.</span>'
            '<a href="https://nikkhosravipour.com" target="_blank" rel="noopener" '
            'style="color:inherit;text-decoration:underline;">nikkhosravipour.com</a></div>\n')

JS_PALETTE = """  function palette() {
    var light = document.documentElement.classList.contains('is-light');
    return {
      tick:  light ? 'rgba(0,0,0,0.42)' : 'rgba(255,255,255,0.5)',
      grid:  light ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.07)',
      yTick: light ? 'rgba(0,0,0,0.65)' : 'rgba(255,255,255,0.7)',
      real:  light ? '#1C1C1A' : '#E8E6DF',
      hawk:  light ? '#A32D2D' : '#f87171',
      dove:  light ? '#185FA5' : '#60a5fa',
      text:  light ? '#1C1C1A' : '#E8E6DF',
      muted: light ? 'rgba(0,0,0,0.50)' : 'rgba(255,255,255,0.55)',
    };
  }"""

JS_SWATCH = "    scope.querySelectorAll('[data-k]').forEach(function(sw){ sw.style.background = c[sw.dataset.k]; });"

JS_CLOSE = """  window.__chartjs.then(function() {
    render();
    new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  });
})();
</script>"""

def js_open(cid):
    return ("</figure>\n<script>\n(function () {\n"
            "  window.__chartjs = window.__chartjs || new Promise(function(resolve) {\n"
            "    if (window.Chart) return resolve();\n"
            "    var s = document.createElement('script');\n"
            "    s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js';\n"
            "    s.onload = resolve; document.head.appendChild(s);\n"
            "  });\n"
            f"  var canvas = document.getElementById('{cid}');\n"
            "  if (!canvas) return;\n"
            "  var scope = canvas.closest('figure');\n"
            "  var chart;\n")

CID = "warsh-dotgap"
real_pts = [{"x": x, "y": y} for x, y in zip(REAL_X, REALIZED)]
html = (
    '<figure class="chart-embed" style="margin:0; font-family:var(--font-body);">\n'
    + fig_header(
        "Federal Reserve · SEP Median Dots · 2015–2024",
        "What the Fed Projected for Its Own Rate",
        "Two FOMC median-dot vintages against the realized federal funds rate · percent"
    )
    + stat_cards([
        stat_card("Dec 2015 dot for 2018", "3.3% &rarr; 2.4%"),
        stat_card("Mar 2021 dot for 2022", "0.1% &rarr; 4.3%"),
    ], ncols=2)
    + legend_row([
        legend_line("real", "Realized rate"),
        legend_line("hawk", "Dec 2015 projection (too high)"),
        legend_line("dove", "Mar 2021 projection (too low)"),
    ])
    + '<div style="position:relative; width:100%; height:280px;">\n'
    + f'<canvas id="{CID}" role="img" aria-label="The realized federal funds rate against two FOMC median-dot projections: December 2015, which projected too high, and March 2021, which projected too low"></canvas>\n'
    + '</div>\n'
    + footer()
    + js_open(CID)
    + JS_PALETTE + "\n"
    + "  function render() {\n    if (!window.Chart) return;\n    var c = palette();\n"
    + JS_SWATCH + "\n"
    + "    if (chart) chart.destroy();\n"
    + "    chart = new Chart(canvas, {\n      type: 'line',\n"
    + "      data: { datasets: [\n"
    + f"        {{ label: 'Realized rate', data: {json.dumps(real_pts)}, borderColor: c.real, borderWidth: 3, pointRadius: 0, tension: 0.15, fill: false, order: 1 }},\n"
    + f"        {{ label: 'Dec 2015 projection', data: {json.dumps(pts(HAWK))}, borderColor: c.hawk, borderWidth: 2, borderDash: [5,3], pointRadius: 3, pointBackgroundColor: c.hawk, tension: 0, fill: false, order: 2 }},\n"
    + f"        {{ label: 'Mar 2021 projection', data: {json.dumps(pts(DOVE))}, borderColor: c.dove, borderWidth: 2, borderDash: [5,3], pointRadius: 3, pointBackgroundColor: c.dove, tension: 0, fill: false, order: 2 }}\n"
    + "      ]},\n"
    + "      options: {\n"
    + "        responsive: true, maintainAspectRatio: false, animation: false,\n"
    + "        layout: { padding: { top: 16, right: 16, left: 0, bottom: 4 } },\n"
    + "        interaction: { mode: 'nearest', intersect: false },\n"
    + "        plugins: { legend: { display: false }, title: { display: false } },\n"
    + "        scales: {\n"
    + "          x: { type: 'linear', min: 2015, max: 2024.4, border: { display: false },\n"
    + "            grid: { color: c.grid },\n"
    + "            ticks: { color: c.tick, font: { size: 10, family: 'system-ui, sans-serif' },\n"
    + "              stepSize: 1, maxRotation: 0, autoSkip: false,\n"
    + "              callback: function(v) { return Number.isInteger(v) ? ('\\u2019' + String(v).slice(2)) : ''; } } },\n"
    + "          y: { beginAtZero: true, border: { display: false }, grid: { color: c.grid },\n"
    + "            ticks: { color: c.yTick, font: { size: 10, family: 'system-ui, sans-serif' },\n"
    + "              callback: function(v) { return v + '%'; } } }\n"
    + "        }\n      }\n    });\n  }\n"
    + JS_CLOSE
)
(WIDGETS / "fig0_dotgap.html").write_text(html)
(WIDGETS / "fig0_dotgap.embed.md").write_text("```html-embed\n" + html + "\n```\n")

# ── PNG ───────────────────────────────────────────────────────────────────────
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(7.6, 3.5), dpi=120, facecolor="white")

def xy(d):
    p = sorted(d.items()); return [y + 0.95 for y, _ in p], [v for _, v in p]

ax.plot(REAL_X, REALIZED, color=PAL["real"], lw=2.6, zorder=5, label="Realized rate")
xh, yh = xy(HAWK); ax.plot(xh, yh, color=PAL["hawk"], lw=2.0, ls="--", marker="o", ms=4, zorder=4, label="Dec 2015 projection (too high)")
xd, yd = xy(DOVE); ax.plot(xd, yd, color=PAL["dove"], lw=2.0, ls="--", marker="o", ms=4, zorder=4, label="Mar 2021 projection (too low)")

ax.annotate("Dec 2015 projected 3.3%\nby 2018; rate stopped at 2.4%", xy=(2018.95, 3.3),
            xytext=(2015.3, 4.4), fontsize=6.4, color=PAL["hawk"], ha="left")
ax.annotate("Mar 2021 projected 0.1%;\nrate reached above 4%", xy=(2022.95, 0.1),
            xytext=(2019.6, 0.9), fontsize=6.4, color=PAL["dove"], ha="left")

ax.set_xlim(2015, 2024.4); ax.set_ylim(0, 6)
ax.spines["left"].set_visible(False); ax.spines["bottom"].set_color(PAL["muted"])
ax.yaxis.set_tick_params(length=0); ax.tick_params(colors=PAL["muted"], labelsize=7)
ax.set_xticks(range(2015, 2025)); ax.set_xticklabels([f"'{str(y)[2:]}" for y in range(2015, 2025)], fontsize=7)
for yv in ax.get_yticks(): ax.axhline(yv, color=PAL["grid"], lw=0.7, zorder=0)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.legend(frameon=False, fontsize=6.8, loc="upper center", ncol=1)
ax.set_title("What the Fed Projected for Its Own Rate", loc="left", fontweight="bold", fontsize=9, pad=18)
ax.text(0, 1.045, "Two FOMC median-dot vintages against the realized federal funds rate",
        transform=ax.transAxes, fontsize=7, color=PAL["muted"])
fig.text(0.0, -0.03, "Source: FOMC Summary of Economic Projections; FRED (realized rate). Author's calculations.  |  nikkhosravipour.com",
         fontsize=6, color=PAL["muted"], ha="left")
plt.tight_layout()
fig.savefig(FIGURES / "fig0_dotgap.png", dpi=120, bbox_inches="tight", facecolor="white")
plt.close()

print("\n── fig0_dotgap (3-line) output ──────────────────────────")
for name, p in [("fig0_dotgap.html", WIDGETS/"fig0_dotgap.html"),
                ("fig0_dotgap.embed.md", WIDGETS/"fig0_dotgap.embed.md"),
                ("fig0_dotgap.png", FIGURES/"fig0_dotgap.png")]:
    s = p.stat().st_size if p.exists() else 0
    print(f"  {name:<24} {s:>8,} bytes  {'[OK]' if s else '[MISSING]'}")
