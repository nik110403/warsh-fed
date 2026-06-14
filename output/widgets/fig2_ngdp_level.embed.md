```html-embed
<figure class="chart-embed" style="margin:0; font-family:var(--font-body);">
<p style="margin:0 0 3px;font-size:10px;letter-spacing:0.13em;text-transform:uppercase;color:var(--muted);">Federal Reserve · Policy Brief · 2019–2026</p>
<p style="margin:0 0 3px;font-size:18px;font-weight:500;color:var(--text);line-height:1.3;">Nominal GDP vs. 4% Trend Path from 2019 Q4</p>
<p style="margin:0 0 18px;font-size:12px;color:var(--muted);">Actual nominal spending vs. rules-based benchmark · billions USD · quarterly</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;"><div style="background:var(--bg-soft);border:1px solid var(--border);border-radius:6px;padding:8px 12px;"><div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px;">Current NGDP gap</div><div style="font-size:1.05rem;font-weight:600;color:var(--text);">+13.1%</div></div><div style="background:var(--bg-soft);border:1px solid var(--border);border-radius:6px;padding:8px 12px;"><div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px;">Overshoot (billions)</div><div style="font-size:1.05rem;font-weight:600;color:var(--text);">&#36;3,683bn</div></div><div style="background:var(--bg-soft);border:1px solid var(--border);border-radius:6px;padding:8px 12px;"><div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px;">Peak gap</div><div style="font-size:1.05rem;font-weight:600;color:var(--text);">+13.1% (2026-Q1)</div></div></div>
<div style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:12px;"><span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);"><span data-k="ngdp" style="display:inline-block;width:20px;height:2px;background:#888;border-radius:1px;flex-shrink:0;"></span>Nominal GDP (actual)</span><span style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:var(--muted);"><span data-k="trend" data-dash="1" style="display:inline-block;width:20px;height:0;border-bottom:2px dashed #888;flex-shrink:0;"></span>4% trend from 2019 Q4</span></div>
<div style="position:relative; width:100%; height:260px;">
<canvas id="warsh-fig2" role="img" aria-label="Nominal GDP vs 4% trend path, 2019-2026"></canvas>
</div>
<div style="margin-top:14px;padding-top:10px;border-top:1px solid var(--border);display:flex;justify-content:space-between;font-size:10px;color:var(--muted);letter-spacing:0.02em;"><span>Source: <a href="https://fred.stlouisfed.org/" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline;">Federal Reserve Economic Data (FRED)</a>, CBO. Author&#8217;s calculations.</span><a href="https://nikkhosravipour.com" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline;">nikkhosravipour.com</a></div>
</figure>
<script>
(function () {
  window.__chartjs = window.__chartjs || new Promise(function(resolve) {
    if (window.Chart) return resolve();
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js';
    s.onload = resolve; document.head.appendChild(s);
  });
  var canvas = document.getElementById('warsh-fig2');
  if (!canvas) return;
  var scope = canvas.closest('figure');
  var chart;
  function palette() {
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
  }
  function render() {
    if (!window.Chart) return;
    var c = palette();
    scope.querySelectorAll('[data-k]').forEach(function(sw) { if (sw.dataset.dash) sw.style.borderBottomColor = c[sw.dataset.k]; else sw.style.background = c[sw.dataset.k]; });
    var labels = ["2018-Q1", "2018-Q2", "2018-Q3", "2018-Q4", "2019-Q1", "2019-Q2", "2019-Q3", "2019-Q4", "2020-Q1", "2020-Q2", "2020-Q3", "2020-Q4", "2021-Q1", "2021-Q2", "2021-Q3", "2021-Q4", "2022-Q1", "2022-Q2", "2022-Q3", "2022-Q4", "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1"];
    if (chart) chart.destroy();
    chart = new Chart(canvas, {
      type: 'line',
      data: { labels: labels, datasets: [
        { label: 'Nominal GDP', data: [20328.6, 20580.9, 20798.7, 20917.9, 21111.6, 21397.9, 21717.2, 21933.2, 21751.2, 19958.3, 21704.4, 22087.2, 22680.7, 23425.9, 23982.4, 24813.6, 25250.3, 25861.3, 26336.3, 26770.5, 27216.4, 27530.1, 28074.8, 28424.7, 28708.2, 29147.0, 29511.7, 29825.2, 30042.1, 30485.7, 31098.0, 31422.5, 31819.5], borderColor: c.ngdp, borderWidth: 3, pointRadius: 0, tension: 0.3, fill: false },
        { label: '4% trend', data: [20459.2, 20661.0, 20867.0, 21077.4, 21289.9, 21499.9, 21714.3, 21933.2, 22154.4, 22375.3, 22598.4, 22826.3, 23056.4, 23283.8, 23516.0, 23753.1, 23992.6, 24229.2, 24470.9, 24717.6, 24966.8, 25213.0, 25464.5, 25721.2, 25980.6, 26239.7, 26501.3, 26768.5, 27038.4, 27305.1, 27577.4, 27855.4, 28136.3], borderColor: c.trend, borderWidth: 1.5, borderDash: [6,3], pointRadius: 0, tension: 0.3, fill: false }
      ]},
      options: {
        responsive: true, maintainAspectRatio: false, animation: false,
        layout: { padding: { top: 26, right: 20, left: 0, bottom: 4 } },
        interaction: { mode: 'index', intersect: false },
        plugins: { legend: { display: false }, title: { display: false } },
        scales: {
          x: {
            border: { display: false },
            grid: { color: c.grid },
            ticks: { color: c.tick, font: { size: 10, family: 'system-ui, sans-serif' },
              maxRotation: 0, autoSkip: false,
              callback: function(val, i) { return i % 4 === 0 ? labels[i] : null; } }
          },
          y: { border: { display: false }, grid: { color: c.grid },
            ticks: { color: c.yTick, font: { size: 10, family: 'system-ui, sans-serif' },
              callback: function(v) { return String.fromCharCode(36) + (v/1000).toFixed(0) + 'T'; } } }
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
