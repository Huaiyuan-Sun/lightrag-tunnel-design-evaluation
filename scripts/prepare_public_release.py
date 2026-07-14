"""Prepare the public release without redistributing standards or raw outputs."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


SOURCE_ROOT = Path(r"C:\\D\\daima\\ACtest")
RELEASE_ROOT = Path(__file__).resolve().parents[1]


def copy(source: Path, relative_target: str) -> None:
    target = RELEASE_ROOT / relative_target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    release_files = {
        SOURCE_ROOT / "combined200" / "summary_by_method.csv": "results/summary_by_method_200.csv",
        SOURCE_ROOT / "combined200" / "summary_by_split_method.csv": "results/summary_by_split_method_200.csv",
        SOURCE_ROOT / "combined200" / "summary_by_category.csv": "results/summary_by_category_200.csv",
        SOURCE_ROOT / "combined200" / "experiment_report.md": "results/experiment_report_200.md",
        SOURCE_ROOT / "holdout170" / "summary_by_method.csv": "results/summary_by_method_holdout170.csv",
        SOURCE_ROOT / "holdout170" / "summary_by_category.csv": "results/summary_by_category_holdout170.csv",
        SOURCE_ROOT / "holdout170" / "experiment_report.md": "results/experiment_report_holdout170.md",
        SOURCE_ROOT / "combined200" / "nature_lightrag_metrics.png": "figures/nature_lightrag_metrics.png",
        SOURCE_ROOT / "combined200" / "nature_lightrag_metrics.tiff": "figures/nature_lightrag_metrics.tiff",
        SOURCE_ROOT / "combined200" / "nature_lightrag_metrics.svg": "figures/nature_lightrag_metrics.svg",
        SOURCE_ROOT / "combined200" / "nature_lightrag_metrics.pdf": "figures/nature_lightrag_metrics.pdf",
        SOURCE_ROOT / "combined200" / "nature_lightrag_metrics_source_data.csv": "figures/nature_lightrag_metrics_source_data.csv",
        SOURCE_ROOT / "combined200" / "nature_lightrag_metrics_legend.txt": "figures/nature_lightrag_metrics_legend.txt",
    }
    for source, target in release_files.items():
        copy(source, target)

    with (SOURCE_ROOT / "combined200_questions.json").open(encoding="utf-8") as handle:
        questions = json.load(handle)
    metadata_path = RELEASE_ROOT / "data" / "question_metadata_200.csv"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with metadata_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "split", "standard", "category", "clause", "page", "question"])
        writer.writeheader()
        for index, item in enumerate(questions):
            writer.writerow({
                "id": item["id"],
                "split": "development" if index < 30 else "independent_holdout",
                "standard": item["standard"],
                "category": item["category"],
                "clause": item["clause"],
                "page": item["page"],
                "question": item["question"],
            })

    manifest = {
        "title": "Optimized LightRAG Evaluation for Drill-and-Blast Tunnel Excavation and Support Design",
        "questions": len(questions),
        "public_contents": ["aggregate metrics", "question metadata", "figures", "plotting code", "reports"],
        "excluded": [
            "copyrighted standards and full source text",
            "gold answers and extracted evidence snippets",
            "complete model responses and retrieval contexts",
            "API keys and local environment configuration",
        ],
    }
    (RELEASE_ROOT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
