# Trajectory Clustering

## Summary

**Trajectory clustering** is the methodological core of the [[New Empirical Foundation]]—the process of grouping individual [[Behavioral Trajectory|behavioral trajectories]] (see [[Behavioral Trajectory]]) into clusters that constitute institutions.

## What Is Being Clustered?

Unlike traditional clustering of static attributes, trajectory clustering analyzes:
- **Sequences of actions** over time
- **Temporal patterns** in behavior
- **Response patterns** to informational signals
- **Evolution** of individual behavior across contexts

## Why Trajectories?

Individual trajectories capture:
1. **Dynamic behavior**: How actions unfold over time
2. **Context sensitivity**: Responses to different signals
3. **Learning and adaptation**: Changes in response patterns
4. **Institutional influence**: Constraints and enablements visible in patterns

## Clustering Methods

### Distance Metrics for Trajectories
- **Dynamic Time Warping (DTW)**: Aligns trajectories of different lengths
- **Edit distance**: Counts operations to transform one sequence to another
- **Fréchet distance**: Measures similarity between curves
- **Custom behavioral distance**: Domain-specific metrics

### Clustering Algorithms
- **k-shape**: Clustering for time series data
- **DBSCAN**: Density-based, finds arbitrary cluster shapes
- **Hierarchical clustering**: Builds tree of cluster relationships
- **Gaussian mixture models**: Probabilistic cluster assignment

### Determining Number of Clusters
- **Elbow method**: Plot within-cluster variance vs. k
- **Silhouette analysis**: Measure cluster cohesion/separation
- **Gap statistic**: Compare to null reference distribution
- **Domain knowledge**: Theoretical expectations

## From Clusters to Institutions

Once trajectories are clustered:
1. **Identify cluster characteristics**: What defines each group?
2. **Assess stationarity**: Are clusters stable over time? (see [[Stationarity Testing]])
3. **Map to theory**: Do clusters correspond to theoretical categories?
4. **Analyze boundaries**: Who is included/excluded? (see [[Algorithmic Exclusion]])

## Example Application

See [[Behavioral Cluster Analysis Example]] for a complete worked example using synthetic platform data.

## Challenges

1. **High dimensionality**: Trajectories have many timepoints × many features
2. **Missing data**: Users drop out, platforms change tracking
3. **Concept drift**: Clusters may legitimately change over time
4. **Interpretation**: Statistical clusters need theoretical meaning

## Related Concepts

- [[Behavioral Trajectory]] - Individual-level sequences being clustered
- [[Behavioral Cluster]] - Result of clustering process
- [[Tier 3: Mathematical Operationalization]] - Technical details
- [[The Measurement Dead End]] - Problem this method solves

---

*This page addresses the broken link [[Trajectory Clustering]] referenced in 3 files.*
