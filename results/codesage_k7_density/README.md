# Density-aware K=7 result

- Corpus: 287 programs
- Encoder: `codesage/codesage-base-v2`, pinned revision `92eac4f44c8674638f039f1b0d8280f2539cb4c7`
- Embedding dimension: 1,024
- Geometry: PCA32, then K-means K=7 on the 284-program density core
- Density rule: 10-nearest-neighbor distance; noise threshold `median + 3*MAD`
- Core cluster sizes: `[67, 6, 26, 18, 22, 95, 50]`
- Noise count: 3
- Active cluster-prior selected counts: `[15, 6, 15, 15, 15, 15, 15]` (96 contributors)

`analysis/index.html` combines the 2D view, per-cluster metrics, and the active Top-15 prior-selection analysis. The global prior still uses all 287 programs. Cluster priors use the 96 density-selected contributors recorded in `data/top15_cluster_prior_selection.json`; the earlier Top-30 artifact remains as historical evidence.
