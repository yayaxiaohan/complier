#!/usr/bin/env python3
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
sums={}
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1);p=ROOT/name;sums[name]=digest;checks.append(p.is_file() and sha(p)==digest)
rows=list(csv.DictReader((ROOT/'data/assignments.csv').open()))
density=json.load((ROOT/'data/density_clusters.json').open())
metrics=json.load((ROOT/'data/density_cluster_metrics.json').open())
model=json.load((ROOT/'data/stable_density_model.json').open())
selection=json.load((ROOT/'data/top30_cluster_prior_selection.json').open())
features=json.load((ROOT/'data/codesage_features_sanitized.json').open())
noise={r['program'] for r in rows if r['noise_flag']=='True'}
selected=selection['density_selection']['selected_members']
semantic={
 'hashes':all(checks), 'programs':len(rows)==len(features['programs'])==287,
 'dimensions':all(len(v['embedding'])==1024 for v in features['programs'].values()),
 'noise':noise==set(density['noise_programs']) and len(noise)==3,
 'core_counts':density['core_cluster_sizes']==model['core_cluster_sizes']==[67,6,26,18,22,95,50],
 'metric_rows':[x['program_count'] for x in metrics['clusters']]==[67,8,26,18,22,96,50],
 'selected_counts':[len(selected[str(c)]) for c in range(7)]==[30,6,26,18,22,30,30],
 'selected_total':sum(map(len,selected.values()))==162,
 'selection_excludes_noise':not noise.intersection(n for x in selected.values() for n in x),
 'feature_signature':features['signature']==density['feature_signature']==model['feature_signature'],
 'model_shape':len(model['pca_components'])==32 and len(model['pca_mean'])==1024 and len(model['cluster_centers'])==7,
}
print(json.dumps(semantic,indent=2,sort_keys=True))
raise SystemExit(0 if all(semantic.values()) else 1)
