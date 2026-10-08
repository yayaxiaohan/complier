#!/usr/bin/env python3
"""Recover and serialize the previously published density-core K=7 model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--density", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.metrics import adjusted_rand_score

    feature_doc = json.loads(args.features.read_text())
    density = json.loads(args.density.read_text())
    programs = feature_doc["programs"]
    names = sorted(programs)
    if set(names) != set(density["assignments"]) or len(names) != 287:
        raise RuntimeError("density/features membership mismatch")
    x = np.asarray([programs[n]["embedding"] for n in names], dtype=float)
    if x.shape != (287, 1024) or not np.isfinite(x).all():
        raise RuntimeError("unexpected CodeSage feature matrix")
    norms = np.linalg.norm(x, axis=1)
    if np.max(np.abs(norms - 1)) > 1e-4:
        raise RuntimeError("features are not unit normalized")
    pca = PCA(n_components=32, svd_solver="full")
    z = pca.fit_transform(x)
    noise = set(density["noise_programs"])
    core = np.asarray([n not in noise for n in names])
    expected = np.asarray([density["assignments"][n] for n in names], dtype=int)
    candidates = []
    exact = None
    for n_init in (10, 20, 50):
        for seed in range(101):
            km = KMeans(n_clusters=7, n_init=n_init, random_state=seed).fit(z[core])
            observed = km.predict(z)
            matrix = np.zeros((7, 7), dtype=int)
            for want, got in zip(expected[core], observed[core]):
                matrix[want, got] += 1
            want_labels, got_labels = linear_sum_assignment(-matrix)
            mapping = {int(got): int(want) for want, got in zip(want_labels, got_labels)}
            aligned = np.asarray([mapping[int(v)] for v in observed])
            accuracy = float(np.mean(aligned[core] == expected[core]))
            ari = float(adjusted_rand_score(expected[core], observed[core]))
            candidates.append({"n_init": n_init, "seed": seed, "accuracy": accuracy, "ari": ari})
            if accuracy == 1.0:
                exact = (n_init, seed, km, mapping, aligned)
                break
        if exact is not None:
            break
    if exact is None:
        best = max(candidates, key=lambda row: (row["accuracy"], row["ari"]))
        raise RuntimeError(f"could not exactly reconstruct density partition; best={best}")
    n_init, seed, km, mapping, aligned = exact
    centers = [None] * 7
    for observed_label, expected_label in mapping.items():
        centers[expected_label] = km.cluster_centers_[observed_label].tolist()
    if list(np.bincount(expected[core], minlength=7)) != density["core_cluster_sizes"]:
        raise RuntimeError("published core counts disagree")
    output = {
        "status": "EXACT_PARTITION_RECONSTRUCTION",
        "feature_signature": density["feature_signature"],
        "features_sha256": sha(args.features),
        "density_assignments_sha256": sha(args.density),
        "program_count": 287,
        "core_count": 284,
        "noise_programs": sorted(noise),
        "pca_dimensions": 32,
        "pca_mean": pca.mean_.tolist(),
        "pca_components": pca.components_.tolist(),
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "kmeans_clusters": 7,
        "kmeans_n_init": n_init,
        "kmeans_seed": seed,
        "cluster_centers": centers,
        "core_cluster_sizes": density["core_cluster_sizes"],
        "assignments": density["assignments"],
        "core_members": {str(c): [n for n in names if n not in noise and density["assignments"][n] == c] for c in range(7)},
        "reconstruction_accuracy": 1.0,
        "reconstruction_ari": 1.0,
        "candidate_search": {"n_init": [10, 20, 50], "seed": [0, 100], "tested": len(candidates)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: output[k] for k in ("status", "program_count", "core_count", "kmeans_n_init", "kmeans_seed", "reconstruction_accuracy")}))


if __name__ == "__main__":
    main()
