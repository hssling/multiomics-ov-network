param(
  [string]$KaggleVersionNotes = "Initial public release",
  [string]$HFRepo = "jkhospital/tcga-ov-multiomics-network-derived-results",
  [switch]$PublishKaggle,
  [switch]$PublishHF
)

$ErrorActionPreference = "Stop"

Write-Host "Validating release folders..."
$kagglePath = "public_release/kaggle_dataset"
$hfPath = "public_release/hf_dataset"

if (!(Test-Path "$kagglePath/dataset-metadata.json")) {
  throw "Missing Kaggle metadata: $kagglePath/dataset-metadata.json"
}
if (!(Test-Path "$hfPath/README.md")) {
  throw "Missing HF dataset card: $hfPath/README.md"
}

if ($PublishKaggle) {
  Write-Host "Publishing to Kaggle..."
  kaggle datasets version -p $kagglePath -m $KaggleVersionNotes -r zip
}

if ($PublishHF) {
  Write-Host "Publishing to Hugging Face Hub..."
  hf repo create $HFRepo --type dataset --private false --exist-ok
  hf upload $HFRepo "$hfPath" . --repo-type dataset
}

Write-Host "Done."
