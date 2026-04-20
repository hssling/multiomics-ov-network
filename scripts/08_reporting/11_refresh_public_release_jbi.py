from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    jbi = ROOT / "manuscript" / "submission_package" / "targets" / "journal_of_biomedical_informatics"
    hf = ROOT / "public_release" / "hf_dataset"
    kaggle = ROOT / "public_release" / "kaggle_dataset"

    for base in [hf, kaggle]:
        target = base / "manuscript" / "journal_of_biomedical_informatics"
        target.mkdir(parents=True, exist_ok=True)
        for name in [
            "JBI_Main_Manuscript.docx",
            "JBI_Title_Page.docx",
            "JBI_Cover_Letter.docx",
            "JBI_Declarations.docx",
            "JBI_Supplementary_Appendix.docx",
            "JBI_Submission_Checklist.docx",
            "JBI_Graphical_Abstract.png",
            "JBI_submission_bundle_readme.md",
            "JBI_Suggested_Reviewers.md",
            "JBI_Response_To_Reviewers_Template.md",
            "JBI_Submission_Metadata.md",
        ]:
            src = jbi / name
            if src.exists():
                copy_file(src, target / name)

        for rel in [
            Path("results/tables/external_ovarian_immune_summary.csv"),
            Path("results/tables/cart_direct_benchmark_qc.csv"),
            Path("results/tables/cart_motif_benchmark.csv"),
            Path("results/tables/cart_reference_alignment_readiness.csv"),
            Path("results/tables/external_validation_file_inventory.csv"),
            Path("results/figures/external_ovarian_immune_scores.png"),
            Path("results/figures/external_ovarian_immune_heatmap.png"),
            Path("results/reports/external_validation_and_cart_benchmark.md"),
            Path("results/reports/cart_motif_benchmark.md"),
            Path("results/reports/cart_reference_alignment_plan.md"),
            Path("results/reports/cart_reference_alignment_commands.sh"),
        ]:
            src = ROOT / rel
            if src.exists():
                copy_file(src, base / rel)

    print("Public release refreshed with JBI package")


if __name__ == "__main__":
    main()
