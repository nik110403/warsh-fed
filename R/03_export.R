source("R/config.R")
library(dplyr)

df <- readRDS(file.path(DATA_DIR, "df_rules.rds"))

df_export <- df |>
  filter(date >= as.Date("2018-01-01")) |>
  select(
    date, FEDFUNDS, PCEPILFE,
    taylor_base, taylor_orig, taylor_dev_base, taylor_dev_orig,
    GDP, ngdp_trend, ngdp_gap,
    m2_yoy, k_target, m2_dev,
    ngdp_growth, gdppot_growth, selgin_dev
  )

write.csv(df_export, file.path(DATA_DIR, "rules_export.csv"), row.names = FALSE)

# ── Summary: numbers to cite in prose ────────────────────────────────────────

cat("\n═══ KEY NUMBERS FOR PROSE ═══════════════════════════════════════════════\n")

latest <- tail(df_export, 1)
cat(sprintf("Latest quarter      : %s\n", latest$date))
cat(sprintf("Actual FFR          : %.2f%%\n", latest$FEDFUNDS))
cat(sprintf("Taylor (r*=0.5%%)    : %.2f%%  (gap: %+.2fpp)\n", latest$taylor_base, latest$taylor_dev_base))
cat(sprintf("Taylor (r*=2.0%%)    : %.2f%%  (gap: %+.2fpp)\n", latest$taylor_orig, latest$taylor_dev_orig))
cat(sprintf("NGDP gap vs trend   : %+.2f%%\n", latest$ngdp_gap))
cat(sprintf("M2 YoY growth       : %.2f%%  (k-target: %.1f%%, dev: %+.2fpp)\n",
            latest$m2_yoy, latest$k_target, latest$m2_dev))
cat(sprintf("NGDP growth         : %.2f%%  (potential: %.2f%%, Selgin dev: %+.2fpp)\n",
            latest$ngdp_growth, latest$gdppot_growth, latest$selgin_dev))

cat("\n── Peak deviations ──────────────────────────────────────────────────────\n")
pk_taylor <- df_export[which.max(df_export$taylor_dev_base), ]
cat(sprintf("Peak Taylor gap (r*=0.5%%) : %+.2fpp in %s\n", pk_taylor$taylor_dev_base, pk_taylor$date))
pk_taylor2 <- df_export[which.max(df_export$taylor_dev_orig), ]
cat(sprintf("Peak Taylor gap (r*=2.0%%) : %+.2fpp in %s\n", pk_taylor2$taylor_dev_orig, pk_taylor2$date))
pk_m2 <- df_export[which.max(df_export$m2_yoy), ]
cat(sprintf("Peak M2 YoY growth        : %.1f%% in %s (dev: %+.1fpp vs k)\n",
            pk_m2$m2_yoy, pk_m2$date, pk_m2$m2_dev))
pk_ngdp_gap <- df_export[which.max(df_export$ngdp_gap), ]
cat(sprintf("Peak NGDP overshoot       : %+.2f%% in %s\n", pk_ngdp_gap$ngdp_gap, pk_ngdp_gap$date))
pk_selgin <- df_export[which.max(df_export$selgin_dev), ]
cat(sprintf("Peak Selgin deviation     : %+.2fpp in %s\n", pk_selgin$selgin_dev, pk_selgin$date))

cat("\n── Recent 6 quarters ────────────────────────────────────────────────────\n")
print(tail(df_export |> select(date, FEDFUNDS, taylor_base, taylor_dev_base, ngdp_gap, m2_dev, selgin_dev), 6),
      row.names = FALSE)
cat("═════════════════════════════════════════════════════════════════════════\n\n")
