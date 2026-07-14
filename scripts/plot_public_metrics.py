from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "figures" / "nature_lightrag_metrics_source_data.csv"
OUTPUT = ROOT / "figures" / "nature_lightrag_metrics_reproduced.png"


def main() -> None:
    data = pd.read_csv(SOURCE)
    metrics = data["metric"].drop_duplicates().tolist()
    methods = ["LLM", "RAG", "LightRAG"]
    labels = {
        "key_point_recall": "Key-point recall",
        "all_keypoints_correct": "All-key-point accuracy",
        "clause_citation_accuracy": "Clause-citation accuracy",
    }
    colors = {"LLM": "#B7B7B7", "RAG": "#4C78A8", "LightRAG": "#E45756"}

    plt.rcParams.update({
        "font.family": "Times New Roman",
        "font.size": 15,
        "axes.labelsize": 17,
        "axes.titlesize": 18,
        "xtick.labelsize": 15,
        "ytick.labelsize": 15,
        "legend.fontsize": 15,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    figure, axis = plt.subplots(figsize=(10.8, 6.8), constrained_layout=True)
    x = range(len(metrics))
    width = 0.23
    offsets = [-width, 0, width]
    for offset, method in zip(offsets, methods):
        subset = data[data["method"] == method].set_index("metric").loc[metrics]
        axis.bar(
            [value + offset for value in x], subset["value"], width=width,
            yerr=[subset["value"] - subset["ci_low"], subset["ci_high"] - subset["value"]],
            capsize=4, color=colors[method], edgecolor="#333333", linewidth=0.7,
            label=method,
        )
    axis.set_xticks(list(x), [labels[item] for item in metrics])
    axis.set_ylabel("Score")
    axis.set_ylim(0, 1.10)
    axis.grid(axis="y", color="#D9D9D9", linewidth=0.7)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, ncol=3, loc="upper left")
    figure.savefig(OUTPUT, dpi=600, bbox_inches="tight")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
