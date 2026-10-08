#!/usr/bin/env python3
"""Verify the frozen Top-15 density selection without private source paths."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXPECTED_CORE_COUNTS = [67, 6, 26, 18, 22, 95, 50]
EXPECTED_SELECTED_COUNTS = [15, 6, 15, 15, 15, 15, 15]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


selection = json.loads((DATA / "top15_cluster_prior_selection.json").read_text())
rows = list(csv.DictReader((DATA / "top15_selected_members.csv").open(newline="")))
section = selection["selection"]
ranked = section["ranked_core_members"]
selected = section["selected_members"]

expected = {
    str(cluster): members[: min(15, len(members))]
    for cluster, members in ranked.items()
}
expected_names = {
    cluster: [member["program"] for member in members]
    for cluster, members in expected.items()
}

csv_members = {str(cluster): [] for cluster in range(7)}
csv_rank_ok = True
csv_distance_ok = True
for row in rows:
    cluster = row["cluster"]
    csv_members[cluster].append(row["program"])
    index = len(csv_members[cluster]) - 1
    csv_rank_ok &= int(row["rank"]) == index + 1
    csv_distance_ok &= float(row["density_distance"]) == float(expected[cluster][index]["density_distance"])

noise = {
    row["program"]
    for row in section["ranking_rows"]
    if str(row["noise_flag"]).lower() == "true"
}
selected_names = {program for members in selected.values() for program in members}

checks = {
    "status_pending_observations": selection["status"] == "FROZEN_SELECTION_PENDING_ALL287_OBSERVATIONS",
    "global_population_287": selection["global_count"] == 287,
    "ranking_population_287": len(section["ranking_rows"]) == 287,
    "core_counts": selection["core_counts"] == EXPECTED_CORE_COUNTS,
    "selected_counts": selection["selected_counts"] == section["selected_counts"] == EXPECTED_SELECTED_COUNTS,
    "selected_total_96": selection["selected_total"] == section["selected_total"] == len(rows) == 96,
    "seven_clusters": set(ranked) == set(selected) == set(csv_members) == {str(i) for i in range(7)},
    "top15_exact": selected == expected_names,
    "csv_members_exact": all(
        csv_members[str(cluster)] == expected_names[str(cluster)]
        for cluster in range(7)
    ),
    "csv_ranks": csv_rank_ok,
    "csv_distances": csv_distance_ok,
    "three_noise_candidates": len(noise) == 3,
    "selection_excludes_noise": not selected_names.intersection(noise),
    "outcomes_not_consulted": section["outcomes_consulted"] is False,
    "ranking_frozen": section["density_ranking_frozen_before_collection"] is True,
    "prior_not_yet_fitted": selection["prior_fitted"] is False,
    "live_collection_not_restarted": selection["live_collection_restarted"] is False,
}

sums = {}
for line in (ROOT / "SHA256SUMS.TOP15").read_text().splitlines():
    digest, name = line.split("  ", 1)
    sums[name] = digest
checks["top15_file_hashes"] = all(
    (ROOT / name).is_file() and sha256(ROOT / name) == digest
    for name, digest in sums.items()
)

print(json.dumps(checks, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
