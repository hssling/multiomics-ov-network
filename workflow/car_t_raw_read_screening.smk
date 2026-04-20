configfile: "configs/cohort.yaml"

rule all:
    input:
        "results/tables/car_t_architecture_metadata.csv",
        "results/tables/car_t_raw_read_inventory.csv",
        "results/reports/car_t_architecture_summary.md",
        "results/reports/car_t_raw_read_screening_plan.md"

rule car_t_assets:
    input:
        "results/tables/car_t_public_sequence_catalog.csv"
    output:
        "results/tables/car_t_architecture_metadata.csv",
        "results/reports/car_t_architecture_summary.md"
    log:
        "results/tables/log_car_t_assets.txt"
    shell:
        "python scripts/09_cart/01_build_car_t_assets.py --config configs/cohort.yaml > {log} 2>&1"

rule car_t_raw_read_screen:
    input:
        "results/tables/car_t_architecture_metadata.csv"
    output:
        "results/tables/car_t_raw_read_inventory.csv",
        "results/reports/car_t_raw_read_screening_plan.md",
        "results/reports/car_t_raw_read_commands.sh"
    log:
        "results/tables/log_car_t_raw_read_screen.txt"
    shell:
        "python scripts/09_cart/02_screen_car_raw_reads.py --config configs/cohort.yaml > {log} 2>&1"

