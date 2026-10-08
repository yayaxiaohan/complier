# CodeSage clustering results

This repository publishes the verified density-aware K=7 clustering of 287 generated Simulink C programs.

Open [`results/codesage_k7_density/analysis/index.html`](results/codesage_k7_density/analysis/index.html) to view the 2D plot and the per-cluster analysis together.

The package contains:

- 287 normalized 1,024-dimensional CodeSage vectors, with private machine paths removed;
- PCA32 and K-means K=7 model parameters;
- all program assignments, 10-nearest-neighbor density distances, metrics, and member lists;
- three declared low-density points, excluded from cluster-prior estimation;
- a frozen top-30-by-density selection per cluster for initial probabilities.

The global optimizer prior still requires all 287 programs. Cluster-specific priors use the densest `min(30, n_c)` core members, yielding counts `[30, 6, 26, 18, 22, 30, 30]` and 162 contributors total. Selection uses ascending 10-nearest-neighbor distance and exact program ID as the tie-break.

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
