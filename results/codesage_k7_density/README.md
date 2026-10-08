# Density-aware K=7 result

- Corpus: 287 programs
- Encoder: `codesage/codesage-base-v2`, pinned revision `92eac4f44c8674638f039f1b0d8280f2539cb4c7`
- Embedding dimension: 1,024
- Geometry: PCA32, then K-means K=7 on the 284-program density core
- Density rule: 10-nearest-neighbor distance; noise threshold `median + 3*MAD`
- Core cluster sizes: `[67, 6, 26, 18, 22, 95, 50]`
- Noise count: 3
- Cluster-prior selected counts: `[30, 6, 26, 18, 22, 30, 30]`

`analysis/index.html` combines the 2D view and per-cluster metrics. `data/assignments.csv` is the compact row-level result. `data/top30_cluster_prior_selection.json` records every density rank and selected member.
