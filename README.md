# Warsh & the Fed

**What would a Warsh-led Fed imply for the path of policy?**

A data-and-chart project building interactive widgets around a scenario read of
Fed leadership and policy. It pulls quarterly macro series from FRED and scores
the actual federal funds rate against several monetary-rule benchmarks — Taylor
rules under two neutral-rate assumptions, a Meltzer k-percent M2 rule, and a
Selgin-style NGDP-level rule — then renders the results as Chart.js widgets and
static figures.

Part of the research on [nikkhosravipour.com](https://nikkhosravipour.com).

## Requirements

- R (≥ 4.0) — packages `fredr`, `dplyr`, `zoo`, `lubridate` auto-install via `R/setup.R`
- Python (≥ 3.10) for chart rendering — `numpy`, `pandas`, `matplotlib`
- A free FRED API key — https://fredaccount.stlouisfed.org/apikeys

## Setup

```bash
cp .Renviron.example .Renviron   # then edit and paste your FRED_API_KEY
```

R loads `.Renviron` automatically from the project root, so the key is read from
the environment — it is never stored in the source.

## Run

```bash
Rscript run_all.R        # 01_data → 02_rules → 03_export  (FRED pull, rule calc, CSV export)
python python/charts.py  # renders widgets + PNG figures from the exported data
```

`run_all.R` writes `output/data/rules_export.csv` and prints the key numbers to
cite. `charts.py` reads that data and writes the figures.

## Outputs

- `output/widgets/*.html` — standalone Chart.js figures (theme-aware, embeddable)
- `output/widgets/*.embed.md` — paste-ready embed snippets
- `output/figures/*.png` — static fallbacks
- `output/data/rules_export.csv` — the scored rule series
- `output/data/*.rds` — intermediate R data (regenerable; gitignored)

## Configuration

Constants live in `R/config.R` — sample window, inflation target `PI_STAR`,
neutral-rate assumptions, the Meltzer `K_PERCENT` benchmark, and the NGDP trend
baseline.

## Data & license

Source data is public, served by [FRED](https://fred.stlouisfed.org/) and subject
to its terms. The code and generated figures in this repository are licensed
under [CC BY 4.0](LICENSE) — reuse with attribution.
