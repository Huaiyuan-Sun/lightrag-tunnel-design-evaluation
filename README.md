# Optimized LightRAG Evaluation for Drill-and-Blast Tunnel Excavation and Support Design

This repository publishes the auditable aggregate results, question metadata, figures, and plotting code for a three-method question-answering evaluation on tunnel excavation and support design standards.

## Headline result

The primary result is the independent 170-question holdout set. The optimized LightRAG hybrid achieved a **0.683 key-point recall**, compared with **0.478** for conventional vector RAG and **0.134** for the context-free LLM baseline. The paired improvement of optimized LightRAG over RAG was **+0.205** (95% bootstrap CI: **[0.138, 0.272]**).

| Dataset | LLM | Vector RAG | Optimized LightRAG hybrid |
| --- | ---: | ---: | ---: |
| Independent holdout (170 questions) | 0.134 | 0.478 | 0.683 |
| Combined set (200 questions) | 0.177 | 0.533 | 0.726 |

Values are key-point recall. The first 30 questions were used during retrieval-strategy development; therefore, the 170-question holdout is the main confirmatory evidence. The 200-question result is provided as a descriptive aggregate.

## Compared methods

- **LLM:** identical generation model and prompt, without external retrieval context.
- **Vector RAG:** LightRAG `naive` vector retrieval over the same indexed standards.
- **Optimized LightRAG hybrid:** lexical retrieval from the legally obtained preprocessed standards, LightRAG `naive` source retrieval, and LightRAG `mix` graph/entity-relation retrieval. Evidence is ordered as lexical source text, vector source text, then graph evidence; when graph-derived summaries conflict with source text, the source text takes precedence.

All methods used `qwen3-vl-plus`, `temperature = 0`, and a 14,000-character retrieval-context budget for the two retrieval methods. The optimized method used a 5,200-character lexical-source budget, a 6,000-character vector-source budget, and a 2,800-character graph-evidence budget. This is an optimized hybrid system, not an ablation of unmodified LightRAG.

## Contents

- `data/question_metadata_200.csv` — 200 question prompts and non-copyright-sensitive metadata. Gold answers, source excerpts, complete model answers, and retrieved contexts are intentionally excluded.
- `results/` — aggregate method, category, and split summaries plus Chinese experimental reports.
- `figures/` — publication-ready comparison figure (`PNG`, `TIFF`, `SVG`, `PDF`) and figure source data.
- `scripts/plot_public_metrics.py` — regenerates the metrics figure from the released source data.
- `MANIFEST.json` — release inventory and exclusions.

## Evaluation protocol

Each question was annotated with a standard identifier, clause/page reference, and groups of required answer key points. The automatic metrics are:

- **Key-point recall:** fraction of required key-point groups matched in an answer.
- **All-key-point accuracy:** fraction of questions for which all required groups were matched.
- **Clause-citation accuracy:** fraction of answers citing the correct clause.
- **Retrieval-evidence recall:** fraction of retrieval cases containing the annotated evidence terms.

Pairwise uncertainty was estimated with paired non-parametric bootstrap confidence intervals (10,000 resamples).

## Source standards and reproducibility

The evaluation used three standards: GB 50086-2015, JTG 3370.1-2018 (Part 1), and JTG/T 3660-2020. Their full text is not distributed here. Users must obtain the standards from legitimate sources and comply with the applicable copyright and licensing terms before reproducing retrieval or generation experiments.

To regenerate the released figure:

```bash
python -m pip install pandas matplotlib
python scripts/plot_public_metrics.py
```

## Limitations

The results are based on automated key-point matching and should be supplemented by independent blind expert assessment before engineering deployment. The benchmark is limited to three standards and should not be interpreted as a general performance guarantee for all tunnelling tasks or all RAG configurations.

## License

The code, question metadata, aggregate metrics, and original figures in this repository are released under the [MIT License](LICENSE). Third-party standards are not included and remain subject to their own rights.
