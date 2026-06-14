pkgs <- c("fredr", "dplyr", "zoo", "lubridate")
for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) install.packages(p)
  library(p, character.only = TRUE)
}
