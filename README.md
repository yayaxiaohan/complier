# CodeSage clustering results

This repository publishes the verified density-aware K=7 clustering of 287 generated Simulink C programs.

Open the [combined HTML preview](https://htmlpreview.github.io/?https://github.com/yayaxiaohan/complier/blob/main/results/codesage_k7_density/analysis/index.html) to view the 2D plot and per-cluster analysis together. The local entry file is [analysis/index.html](results/codesage_k7_density/analysis/index.html).

The package contains:

- 287 normalized 1,024-dimensional CodeSage vectors, with private machine paths removed;
- PCA32 and K-means K=7 model parameters;
- all program assignments, 10-nearest-neighbor density distances, metrics, and member lists;
- three declared low-density points, excluded from cluster-prior estimation;
- historical Top-30 and Top-15 density-selection evidence.

The prior-selection policies in this published package are historical snapshots, not the current training design. They do not establish completed probability fitting or optimizer performance.

Run the integrity and semantic checks with:

```bash
python3 results/codesage_k7_density/scripts/verify_results.py
```

Reconstructing the PCA/K-means model also requires NumPy, SciPy, and scikit-learn:

```bash
python3 results/codesage_k7_density/scripts/reconstruct_density_model.py \
  --features results/codesage_k7_density/data/codesage_features_sanitized.json \
  --density results/codesage_k7_density/data/density_clusters.json \
  --output /tmp/reconstructed_model.json
```
