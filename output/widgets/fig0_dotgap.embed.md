```html-embed
<figure class="chart-embed" style="margin:0; font-family:var(--font-body);">
<p style="margin:0 0 3px;font-size:10px;letter-spacing:0.13em;text-transform:uppercase;color:var(--muted);">Federal Reserve · SEP Median Dots · 2015–2024</p>
<p style="margin:0 0 3px;font-size:18px;font-weight:500;color:var(--text);line-height:1.3;">What the Fed Projected for Its Own Rate</p>
<p style="margin:0 0 18px;font-size:12px;color:var(--muted);">Two FOMC median-dot vintages against the realized federal funds rate · percent</p>
<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:12px;"><div style="background:var(--bg-soft);border:1px solid var(--border);border-radius:6px;padding:8px 12px;"><div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px;">Dec 2015 dot for 2018</div><div style="font-size:1.05rem;font-weight:600;color:var(--text);">3.3% &rarr; 2.4%</div></div><div style="background:var(--bg-soft);border:1px solid var(--border);border-radius:6px;padding:8px 12px;"><div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px;">Mar 2021 dot for 2022</div><div style="font-size:1.05rem;font-weight:600;color:var(--text);">0.1% &rarr; 4.3%</div></div></div>
<div style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:12px;"><span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);"><span data-k="real" style="display:inline-block;width:20px;height:2px;background:#888;border-radius:1px;flex-shrink:0;"></span>Realized rate</span><span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);"><span data-k="hawk" style="display:inline-block;width:20px;height:2px;background:#888;border-radius:1px;flex-shrink:0;"></span>Dec 2015 projection (too high)</span><span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);"><span data-k="dove" style="display:inline-block;width:20px;height:2px;background:#888;border-radius:1px;flex-shrink:0;"></span>Mar 2021 projection (too low)</span></div>
<div style="position:relative; width:100%; height:280px;">
<canvas id="warsh-dotgap" role="img" aria-label="The realized federal funds rate against two FOMC median-dot projections: December 2015, which projected too high, and March 2021, which projected too low"></canvas>
</div>
<div style="margin-top:14px;padding-top:10px;border-top:1px solid var(--border);display:flex;flex-wrap:wrap;gap:4px;justify-content:space-between;font-size:10px;color:var(--muted);letter-spacing:0.02em;"><span>Source: FOMC Summary of Economic Projections, median federal funds rate (dots); <a href="https://fred.stlouisfed.org/series/FEDFUNDS" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline;">FRED</a> (realized rate). Author&#8217;s calculations.</span><a href="https://nikkhosravipour.com" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline;">nikkhosravipour.com</a></div>
</figure>
<script>
(function () {
  window.__chartjs = window.__chartjs || new Promise(function(resolve) {
    if (window.Chart) return resolve();
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js';
    s.onload = resolve; document.head.appendChild(s);
  });
  var canvas = document.getElementById('warsh-dotgap');
  if (!canvas) return;
  var scope = canvas.closest('figure');
  var chart;
  function palette() {
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
  }
  function render() {
    if (!window.Chart) return;
    var c = palette();
    scope.querySelectorAll('[data-k]').forEach(function(sw){ sw.style.background = c[sw.dataset.k]; });
    if (chart) chart.destroy();
    chart = new Chart(canvas, {
      type: 'line',
      data: { datasets: [
        { label: 'Realized rate', data: [{"x": 2015.0, "y": 0.11}, {"x": 2015.25, "y": 0.12}, {"x": 2015.5, "y": 0.14}, {"x": 2015.75, "y": 0.16}, {"x": 2016.0, "y": 0.36}, {"x": 2016.25, "y": 0.37}, {"x": 2016.5, "y": 0.4}, {"x": 2016.75, "y": 0.45}, {"x": 2017.0, "y": 0.7}, {"x": 2017.25, "y": 0.95}, {"x": 2017.5, "y": 1.15}, {"x": 2017.75, "y": 1.2}, {"x": 2018.0, "y": 1.51}, {"x": 2018.25, "y": 1.82}, {"x": 2018.5, "y": 1.95}, {"x": 2018.75, "y": 2.27}, {"x": 2019.0, "y": 2.41}, {"x": 2019.25, "y": 2.38}, {"x": 2019.5, "y": 2.04}, {"x": 2019.75, "y": 1.55}, {"x": 2020.0, "y": 0.65}, {"x": 2020.25, "y": 0.08}, {"x": 2020.5, "y": 0.09}, {"x": 2020.75, "y": 0.09}, {"x": 2021.0, "y": 0.07}, {"x": 2021.25, "y": 0.08}, {"x": 2021.5, "y": 0.08}, {"x": 2021.75, "y": 0.08}, {"x": 2022.0, "y": 0.2}, {"x": 2022.25, "y": 1.21}, {"x": 2022.5, "y": 2.56}, {"x": 2022.75, "y": 4.1}, {"x": 2023.0, "y": 4.65}, {"x": 2023.25, "y": 5.08}, {"x": 2023.5, "y": 5.33}, {"x": 2023.75, "y": 5.33}, {"x": 2024.0, "y": 5.33}, {"x": 2024.25, "y": 5.33}, {"x": 2024.5, "y": 5.13}, {"x": 2024.75, "y": 4.48}, {"x": 2025.0, "y": 4.33}, {"x": 2025.25, "y": 4.33}, {"x": 2025.5, "y": 4.22}, {"x": 2025.75, "y": 3.72}, {"x": 2026.0, "y": 3.64}], borderColor: c.real, borderWidth: 3, pointRadius: 0, tension: 0.15, fill: false, order: 1 },
        { label: 'Dec 2015 projection', data: [{"x": 2015.95, "y": 0.4}, {"x": 2016.95, "y": 1.4}, {"x": 2017.95, "y": 2.4}, {"x": 2018.95, "y": 3.3}], borderColor: c.hawk, borderWidth: 2, borderDash: [5,3], pointRadius: 3, pointBackgroundColor: c.hawk, tension: 0, fill: false, order: 2 },
        { label: 'Mar 2021 projection', data: [{"x": 2021.95, "y": 0.1}, {"x": 2022.95, "y": 0.1}, {"x": 2023.95, "y": 0.1}], borderColor: c.dove, borderWidth: 2, borderDash: [5,3], pointRadius: 3, pointBackgroundColor: c.dove, tension: 0, fill: false, order: 2 }
      ]},
      options: {
        responsive: true, maintainAspectRatio: false, animation: false,
        layout: { padding: { top: 16, right: 16, left: 0, bottom: 4 } },
        interaction: { mode: 'nearest', intersect: false },
        plugins: { legend: { display: false }, title: { display: false } },
        scales: {
          x: { type: 'linear', min: 2015, max: 2024.4, border: { display: false },
            grid: { color: c.grid },
            ticks: { color: c.tick, font: { size: 10, family: 'system-ui, sans-serif' },
              stepSize: 1, maxRotation: 0, autoSkip: false,
              callback: function(v) { return Number.isInteger(v) ? ('\u2019' + String(v).slice(2)) : ''; } } },
          y: { beginAtZero: true, border: { display: false }, grid: { color: c.grid },
            ticks: { color: c.yTick, font: { size: 10, family: 'system-ui, sans-serif' },
              callback: function(v) { return v + '%'; } } }
        }
      }
    });
  }
  window.__chartjs.then(function() {
    render();
    new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  });
})();
</script>
```
