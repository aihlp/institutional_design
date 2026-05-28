# Behavioral Cluster

## Definition

**A behavioral cluster is a grouping of similar behavioral trajectories identified through unsupervised learning techniques.**

In the proposed framework, **a cluster is what the analyst identifies as sufficiently stable and distinct to warrant the label "institution."**

## Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Constructed, not discovered** | Clusters are built by the analyst using explicit criteria |
| **Statistically defined** | Boundaries determined by mathematical properties |
| **Reproducible** | Same data + same criteria = same clusters |
| **Transparent** | Criteria for inclusion/exclusion are explicit |
| **Testable** | Cluster properties can be empirically verified |

## How Clusters Are Identified

### Step 1: Choose Clustering Algorithm

Common options:
- **HDBSCAN**: Density-based, handles noise well
- **UMAP + clustering**: Dimensionality reduction followed by grouping
- **k-means**: Partition-based (requires specifying k)
- **Hierarchical clustering**: Tree-based groupings

### Step 2: Define Similarity Metric

How do we measure if two trajectories are "similar"?
- **Edit distance**: Number of changes to transform one sequence into another
- **Dynamic Time Warping**: Aligns sequences with different timing
- **Embedding cosine similarity**: Compare vector representations
- **Jensen-Shannon divergence**: Compare probability distributions

### Step 3: Set Stability Threshold

What makes a cluster count as an "institution"?
- Minimum temporal persistence (e.g., 30 days)
- Maximum internal divergence (e.g., JSD < 0.15)
- Minimum population size (e.g., >1% of users)
- Stationarity test results (e.g., ADF p < 0.01)

### Step 4: Validate

- **Internal validation**: Silhouette scores, Davies-Bouldin index
- **External validation**: Comparison with known categories
- **Temporal validation**: Stability over time windows
- **Replication**: Same clusters emerge in independent samples

## Example: STEM Ad Exclusion

From [[Behavioral Cluster Analysis Example]]:

| Cluster | Dominant Demographic | Exposure Rate | Response Rate | Stability |
|---------|---------------------|---------------|---------------|-----------|
| **Cluster A** | Male users (~78%) | High (85%+) | High (12%+) | Stationary (ADF p < 0.01) |
| **Cluster B** | Female users (~82%) | Low (<30%) | Low (<3%) | Stationary (ADF p < 0.01) |

Each cluster represents a distinct **institution** in the new framework:
- Stable behavioral pattern
- Statistically distinguishable
- Temporally persistent
- Measurable and trackable

## Contrast with Classical Concepts

| Classical Concept | Behavioral Cluster |
|-------------------|-------------------|
| Rule (unobservable constraint) | Cluster (observable pattern) |
| Norm (shared expectation) | Cluster (statistical grouping) |
| Shared belief (mental state) | Cluster (behavioral regularity) |
| Inferred from behavior | Directly identified in data |
| Exists independently of measurement | Constructed through analytical act |

## The Analyst's Role

Following [[Rapoport's Subjectivism]], the analyst makes explicit choices:

```python
# Example: Explicit criteria for cluster-as-institution

CRITERIA = {
    "min_duration_days": 30,
    "max_internal_divergence": 0.15,  # Jensen-Shannon
    "min_population_pct": 0.01,       # 1% of users
    "stationarity_test": "ADF",
    "stationarity_threshold": 0.01,   # p-value
    "clustering_algorithm": "HDBSCAN",
    "similarity_metric": "embedding_cosine"
}

# These choices are:
# - Explicit (not hidden assumptions)
# - Testable (can be challenged empirically)
# - Reproducible (others can replicate)
# - Refinable (can adjust and compare)
```

## Properties That Make Clusters Institutional

Not every behavioral pattern is an institution. Clusters qualify as institutions when they exhibit:

1. **Temporal stability**: Persist across time windows
2. **Population coherence**: Members share recognizable pattern
3. **Distinctiveness**: Clearly bounded from other clusters
4. **Self-reinforcement**: Pattern tends to reproduce itself
5. **Signal-responsiveness**: Emerge in response to identifiable signals

## Measurement Pipeline

```
Raw behavioral logs
        ↓
Trajectory construction (Tier 1)
        ↓
Similarity computation
        ↓
Clustering algorithm (Tier 3)
        ↓
Stability testing (ADF, KPSS)
        ↓
BEHAVIORAL CLUSTER ← Institution identified
        ↓
Transition matrix analysis
        ↓
Temporal tracking
```

## Related Entries

- [[Behavioral Trajectory]] - What gets clustered
- [[Behavioral Spectrum]] - Full distribution before clustering
- [[From Rules to Behavioral Clusters]] - Core framework proposal
- [[Rapoport's Subjectivism]] - Philosophical foundation
- [[Tier 3: Mathematical Operationalization]] - Technical methods
- [[Behavioral Cluster Analysis Example]] - Worked example

## Categories

[[Core Concepts]], [[New Empirical Foundation]]
