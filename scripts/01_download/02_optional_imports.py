from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.common import parse_args, read_yaml, setup_logger, write_flag


def main():
    args = parse_args()
    cfg = read_yaml(args.config)
    log = setup_logger("optional_imports")

    cbio = Path(cfg["paths"]["raw_cbioportal"])
    pdc = Path(cfg["paths"]["raw_pdc"])
    cbio.mkdir(parents=True, exist_ok=True)
    pdc.mkdir(parents=True, exist_ok=True)

    readme_cbio = cbio / "README_IMPORT.txt"
    readme_pdc = pdc / "README_IMPORT.txt"

    if not readme_cbio.exists():
        readme_cbio.write_text(
            "Place cBioPortal OV PanCancer Atlas exports here.\n"
            "Expected optional files: data_clinical_sample.txt, data_mrna_seq_v2_rsem.txt, data_cna.txt\n",
            encoding="utf-8",
        )
    if not readme_pdc.exists():
        readme_pdc.write_text(
            "Place PDC ovarian proteomics tables here (optional).\n"
            "Expected optional files: protein_abundance.tsv with sample_id and gene/protein columns.\n",
            encoding="utf-8",
        )

    write_flag(str(cbio / "import_complete.flag"))
    write_flag(str(pdc / "import_complete.flag"))
    log.info("Optional source import stubs are ready.")


if __name__ == "__main__":
    main()
