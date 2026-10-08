# Density-aware K=7 result

- Corpus: 287 programs
- Encoder: `codesage/codesage-base-v2`, pinned revision `92eac4f44c8674638f039f1b0d8280f2539cb4c7`
- Embedding dimension: 1,024
- Geometry: PCA32, then K-means K=7 on the 284-program density core
- Density rule: 10-nearest-neighbor distance; noise threshold `median + 3*MAD`
- Core cluster sizes: `[67, 6, 26, 18, 22, 95, 50]`
- Noise count: 3
- Historical Top-15 selected counts: `[15, 6, 15, 15, 15, 15, 15]` (96 contributors)

`analysis/index.html` combines the published 2D view, per-cluster metrics and historical Top-15 selection in one self-contained page. The Top-15 and earlier Top-30 policies are archived stages, not the current training design or completed fitted probabilities. Numerical source assets are preserved unchanged.

[Open the combined HTML preview](https://htmlpreview.github.io/?https://github.com/yayaxiaohan/complier/blob/main/results/codesage_k7_density/analysis/index.html).
