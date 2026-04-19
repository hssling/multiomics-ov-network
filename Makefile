SHELL := /bin/bash

.PHONY: all setup dryrun run report clean

all: dryrun

setup:
	conda env create -f environment/environment-python.yml || true
	conda env create -f environment/environment-r.yml || true

dryrun:
	snakemake -n --cores 1

run:
	snakemake --cores 4 --rerun-incomplete

report:
	snakemake results/reports/final_report.html --cores 2 --rerun-incomplete

clean:
	rm -rf data/interim/* data/processed/* results/tables/* results/figures/* results/models/* results/networks/* results/reports/*
