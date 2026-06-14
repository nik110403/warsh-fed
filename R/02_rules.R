source("R/config.R")
library(dplyr)

df <- readRDS(file.path(DATA_DIR, "df_raw.rds"))

# ── Output gap ────────────────────────────────────────────────────────────────

df <- df |>
  mutate(output_gap = 100 * (GDPC1 - GDPPOT) / GDPPOT)

# ── Taylor Rule (both r* variants) ───────────────────────────────────────────
# r = r* + π + 0.5*(π - π*) + 0.5*y_gap

df <- df |>
  mutate(
    taylor_base = pmax(R_STAR_BASE + PCEPILFE + 0.5 * (PCEPILFE - PI_STAR) + 0.5 * output_gap, 0),
    taylor_orig = pmax(R_STAR_ORIG + PCEPILFE + 0.5 * (PCEPILFE - PI_STAR) + 0.5 * output_gap, 0),
    taylor_dev_base = taylor_base - FEDFUNDS,
    taylor_dev_orig = taylor_orig - FEDFUNDS
  )

# ── NGDP level path (4% trend from 2019 Q4) ──────────────────────────────────

# dplyr::pull qualified: 01_data.R defines a custom pull() (FRED fetch) that
# shadows dplyr's when both files are sourced into the same env via run_all.R.
gdp_base <- df |> dplyr::filter(date == NGDP_BASE_DATE) |> dplyr::pull(GDP)

df <- df |>
  mutate(
    quarters_since_base = as.numeric(difftime(date, NGDP_BASE_DATE, units = "days")) / 91.25,
    ngdp_trend          = gdp_base * (1 + NGDP_TREND_RATE / 4) ^ quarters_since_base,
    ngdp_gap            = 100 * (GDP - ngdp_trend) / ngdp_trend
  )

# ── Meltzer k-percent rule (M2 YoY growth vs. 4% benchmark) ──────────────────

df <- df |>
  arrange(date) |>
  mutate(
    m2_yoy  = 100 * (M2SL / lag(M2SL, 4) - 1),
    k_target = K_PERCENT,
    m2_dev   = m2_yoy - k_target
  )

# ── Selgin productivity norm (NGDP growth vs. potential GDP growth) ───────────

df <- df |>
  mutate(
    gdppot_growth = 100 * (GDPPOT / lag(GDPPOT, 4) - 1),
    ngdp_growth   = 100 * (GDP    / lag(GDP,    4) - 1),
    selgin_dev    = ngdp_growth - gdppot_growth
  )

# ── Save ──────────────────────────────────────────────────────────────────────

saveRDS(df, file.path(DATA_DIR, "df_rules.rds"))
cat("Saved df_rules.rds\n")
