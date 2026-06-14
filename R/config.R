FRED_API_KEY <- Sys.getenv("FRED_API_KEY")
if (!nzchar(FRED_API_KEY)) {
  stop("Set FRED_API_KEY in .Renviron (free key: https://fredaccount.stlouisfed.org/apikeys)")
}

PROJECT_ROOT     <- getwd()
OUTPUT_DIR       <- file.path(PROJECT_ROOT, "output")
WIDGETS_DIR      <- file.path(PROJECT_ROOT, "output/widgets")
DATA_DIR         <- file.path(PROJECT_ROOT, "output/data")
FIGURES_DIR      <- file.path(PROJECT_ROOT, "output/figures")

START_DATE       <- as.Date("2018-01-01")
END_DATE         <- as.Date("2026-03-31")

PI_STAR          <- 2.0    # inflation target, %
R_STAR_BASE      <- 0.5    # real neutral rate, post-GFC Laubach-Williams → nominal neutral = 2.5%
R_STAR_ORIG      <- 2.0    # original Taylor (1993) assumption → nominal neutral = 4.5%
K_PERCENT        <- 4.0    # Meltzer k-percent M2 growth benchmark
NGDP_BASE_DATE   <- as.Date("2019-10-01")   # 2019 Q4 baseline
NGDP_TREND_RATE  <- 0.04   # 4% annual NGDP trend
