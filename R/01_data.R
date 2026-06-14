source("R/config.R")
source("R/setup.R")

fredr_set_key(FRED_API_KEY)

# ── Pull helpers ──────────────────────────────────────────────────────────────

pull <- function(series_id, units = "lin") {
  fredr_series_observations(
    series_id         = series_id,
    observation_start = START_DATE,
    observation_end   = END_DATE,
    frequency         = NULL,
    units             = units
  ) |>
    dplyr::select(date, value) |>
    dplyr::rename(!!series_id := value)
}

to_quarterly <- function(df) {
  col <- names(df)[2]
  df |>
    dplyr::mutate(quarter = as.Date(as.yearqtr(date))) |>
    dplyr::group_by(quarter) |>
    dplyr::slice_tail(n = 1) |>
    dplyr::ungroup() |>
    dplyr::select(date = quarter, !!col := !!dplyr::sym(col))
}

# ── Download series ───────────────────────────────────────────────────────────

raw_fedfunds <- pull("FEDFUNDS")
raw_pcepilfe <- pull("PCEPILFE", units = "pc1")   # core PCE, YoY %
raw_gdpc1    <- pull("GDPC1")                      # real GDP, quarterly
raw_gdppot   <- pull("GDPPOT")                     # potential GDP, quarterly
raw_gdp      <- pull("GDP")                        # nominal GDP, quarterly
raw_m2sl     <- pull("M2SL")                       # M2, monthly

# ── Convert to quarterly ──────────────────────────────────────────────────────

q_fedfunds <- to_quarterly(raw_fedfunds)
q_pcepilfe <- to_quarterly(raw_pcepilfe)
q_gdpc1    <- to_quarterly(raw_gdpc1)
q_gdppot   <- to_quarterly(raw_gdppot)
q_gdp      <- to_quarterly(raw_gdp)
q_m2sl     <- to_quarterly(raw_m2sl)

# ── Merge ─────────────────────────────────────────────────────────────────────

df <- q_gdpc1 |>
  dplyr::full_join(q_gdppot,   by = "date") |>
  dplyr::full_join(q_fedfunds, by = "date") |>
  dplyr::full_join(q_pcepilfe, by = "date") |>
  dplyr::full_join(q_gdp,      by = "date") |>
  dplyr::full_join(q_m2sl,     by = "date") |>
  dplyr::arrange(date)

# Forward-fill any NAs from series with different release lags
df <- df |>
  dplyr::mutate(dplyr::across(where(is.numeric), ~ zoo::na.locf(.x, na.rm = FALSE))) |>
  dplyr::filter(dplyr::if_any(c(FEDFUNDS, PCEPILFE, GDPC1), ~ !is.na(.x)))

# ── Save ──────────────────────────────────────────────────────────────────────

dir.create(DATA_DIR, recursive = TRUE, showWarnings = FALSE)
saveRDS(df, file.path(DATA_DIR, "df_raw.rds"))

cat(sprintf("\nDate range : %s  →  %s\n", min(df$date), max(df$date)))
cat(sprintf("Rows       : %d\n", nrow(df)))
cat("NA counts:\n")
print(colSums(is.na(df)))
