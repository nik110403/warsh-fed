# In RStudio, anchor the working dir to this file's location. Under `Rscript`
# (rstudioapi unavailable) this is skipped — run from the repo root instead.
if (requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}

source("R/01_data.R")
source("R/02_rules.R")
source("R/03_export.R")
