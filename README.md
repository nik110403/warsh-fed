# Warsh & the Fed

Replication repository for the deep dive *Inheriting Discretion: What Monetary Rules
Prescribe for the Warsh Fed* (nikkhosravipour.com/research).

R pulls quarterly macroeconomic series from FRED and scores the actual federal funds rate
against four monetary-rule benchmarks. Python reads the scored data and generates Chart.js
widgets and static figures. The pipeline mirrors the Taylor-rule deep dive repo so the two
projects read as one research program.

## Data vintage

FRED revises historical series, including `GDPPOT` (CBO potential output) and `GDP`
(nominal, subject to benchmark revision). Results reproduce exactly against the vintage
retrieved for the published piece; subsequent pulls may shift rule prescriptions. The sample
window is locked at 2018 Q1–2026 Q1 in `R/config.R` (`START_DATE`, `END_DATE`).

## Requirements

- R (≥ 4.0); packages auto-install via `R/setup.R`: `fredr`, `dplyr`, `zoo`, `lubridate`
- Python (≥ 3.10): `numpy`, `pandas`, `matplotlib`
- A free FRED API key — https://fredaccount.stlouisfed.org/apikeys

## Setup

```bash
cp .Renviron.example .Renviron   # edit and paste your FRED_API_KEY
pip install numpy pandas matplotlib
```

R loads `.Renviron` from the project root automatically. Run both commands from the repo
root; `run_all.R` will error if called from a subdirectory.

## Run

```bash
Rscript run_all.R        # FRED pull → rule scoring → output/data/rules_export.csv
python python/charts.py  # rules_export.csv → widgets + figures
```

`run_all.R` also prints a key-numbers block (latest quarter rates, peak deviations) for
use in prose.

## FRED series

| Series ID | Description | Transformation |
|---|---|---|
| `FEDFUNDS` | Effective federal funds rate | levels |
| `PCEPILFE` | Core PCE deflator | YoY% (`pc1`) |
| `GDPC1` | Real GDP | levels |
| `GDPPOT` | CBO potential real GDP | levels |
| `GDP` | Nominal GDP | levels |
| `M2SL` | M2 money stock | levels |

Monthly series convert to quarterly by taking the last observation of each quarter.

## Rule specifications

| Rule | Formula | Key parameters |
|---|---|---|
| Taylor (baseline) | r\* + π + 0.5(π − π\*) + 0.5·y_gap | r\* = 0.5%, π\* = 2% |
| Taylor (original) | same | r\* = 2.0% (Taylor 1993) |
| Meltzer k-percent | M2 YoY growth vs. fixed target | k = 4% |
| Selgin productivity norm | NGDP growth vs. potential GDP growth | NGDP trend = 4%/yr from 2019 Q4 |

Taylor rules are floored at zero. Output gap = 100·(GDPC1 − GDPPOT)/GDPPOT. The NGDP
level path compounds at 1% per quarter from the 2019 Q4 base (`NGDP_BASE_DATE` in
`R/config.R`).

## Where things can drift

`GDPPOT` is revised with each CBO Budget and Economic Outlook, shifting the Taylor
output-gap term. `GDP` benchmark revisions alter both the Meltzer M2 deviation and the
NGDP gap. The Meltzer and Selgin rules are more stable to revision than the Taylor
variants. The companion piece documents the vintage used.

## Layout

| Script | Role |
|---|---|
| `R/01_data.R` | FRED pull → quarterly conversion → `output/data/df_raw.rds` |
| `R/02_rules.R` | Rule scoring (Taylor, Meltzer, Selgin, NGDP path) → `df_rules.rds` |
| `R/03_export.R` | CSV export + prose key-numbers → `output/data/rules_export.csv` |
| `python/charts.py` | Chart.js widgets + PNG figures from `rules_export.csv` |
| `R/config.R` | Sample window, π\*, r\*, k-percent, NGDP trend |
| `R/setup.R` | Package management |

## License

Source data is public, served by [FRED](https://fred.stlouisfed.org/) and subject to its
terms. The code and generated figures are licensed under [CC BY 4.0](LICENSE) — reuse with
attribution.
