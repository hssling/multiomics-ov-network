suppressPackageStartupMessages({
  library(optparse)
  library(yaml)
  library(data.table)
  library(ggplot2)
})

option_list <- list(make_option(c("--config"), type="character", help="Path to config yaml"))
opt <- parse_args(OptionParser(option_list=option_list))
cfg <- yaml::read_yaml(opt$config)

processed <- cfg$paths$processed
out_models <- cfg$paths$results_models
out_figs <- cfg$paths$results_figures

if (!dir.exists(out_models)) dir.create(out_models, recursive = TRUE)
if (!dir.exists(out_figs)) dir.create(out_figs, recursive = TRUE)

rna <- as.data.frame(data.table::fread(file.path(processed, "rna_modules.csv")))
burden <- as.data.frame(data.table::fread(file.path(processed, "burden_features.csv")))
outcomes <- data.table::fread(file.path(processed, "outcomes.csv"))
protein_mod_file <- file.path(processed, "protein_modules.csv")
has_protein <- file.exists(protein_mod_file)
if (has_protein) {
  protein_mod <- as.data.frame(data.table::fread(protein_mod_file))
}

if (has_protein) {
  ids <- Reduce(intersect, list(rna$patient_id, burden$patient_id, outcomes$patient_id, protein_mod$patient_id))
} else {
  ids <- Reduce(intersect, list(rna$patient_id, burden$patient_id, outcomes$patient_id))
}
rna <- rna[rna$patient_id %in% ids, ]
burden <- burden[burden$patient_id %in% ids, ]
outcomes <- outcomes[outcomes$patient_id %in% ids, ]
if (has_protein) {
  protein_mod <- protein_mod[protein_mod$patient_id %in% ids, ]
}

if (has_protein) {
  X <- cbind(
    rna[, !(colnames(rna) %in% c("sample_id", "patient_id")), drop=FALSE],
    burden[, !(colnames(burden) %in% c("sample_id", "patient_id")), drop=FALSE],
    protein_mod[, !(colnames(protein_mod) %in% c("sample_id", "patient_id")), drop=FALSE]
  )
} else {
  X <- cbind(
    rna[, !(colnames(rna) %in% c("sample_id", "patient_id")), drop=FALSE],
    burden[, !(colnames(burden) %in% c("sample_id", "patient_id")), drop=FALSE]
  )
}

y <- factor(outcomes$survival_risk_group)
X <- as.matrix(X)
keep <- apply(X, 2, function(v) sd(v, na.rm = TRUE) > 0)
X <- X[, keep, drop=FALSE]
X <- as.matrix(scale(X))

if (length(unique(y)) >= 2 && requireNamespace("mixOmics", quietly = TRUE)) {
  # Minimal supervised projection with PLS-DA style representation
  fit <- mixOmics::plsda(X, y, ncomp = cfg$integration$diablo$ncomp)
  comps <- as.data.frame(fit$variates$X)
} else {
  # Fallback to PCA if mixOmics is unavailable in runtime
  p <- prcomp(X, center = TRUE, scale. = TRUE)
  comps <- as.data.frame(p$x[, 1:2, drop=FALSE])
  colnames(comps) <- c("comp1", "comp2")
}

comps$patient_id <- outcomes$patient_id
comps$survival_risk_group <- as.character(y)

if (!"comp1" %in% colnames(comps)) colnames(comps)[1] <- "comp1"
if (!"comp2" %in% colnames(comps)) colnames(comps)[2] <- "comp2"

data.table::fwrite(comps, file.path(out_models, "diablo_scores.csv"))

plt <- ggplot(comps, aes(x = comp1, y = comp2, color = survival_risk_group)) +
  geom_point(alpha = 0.8) +
  theme_minimal() +
  labs(title = "DIABLO-like Component Plot", x = "Component 1", y = "Component 2")

ggsave(file.path(out_figs, "diablo_components.png"), plt, width = 7, height = 5, dpi = 150)
