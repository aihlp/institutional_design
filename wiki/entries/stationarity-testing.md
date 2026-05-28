# Stationarity Testing

## Summary

**Stationarity testing** refers to statistical methods for determining whether behavioral clusters remain stable over time—a critical requirement for identifying something as an "institution" rather than transient behavior.

## Why Stationarity Matters

For behavioral clusters to qualify as institutions, they must exhibit:
1. **Temporal stability**: Patterns persist beyond individual interactions
2. **Statistical stationarity**: Distribution properties don't change over time
3. **Resistance to perturbation**: Clusters reform after disruptions

Without stationarity, we cannot distinguish:
- Institutions from temporary conventions
- Structural patterns from random fluctuations
- Meaningful regularities from noise

## Testing Methods

### Visual Inspection
- Plot cluster assignments over time
- Look for stable groupings vs. chaotic reassignment

### Statistical Tests
- **Augmented Dickey-Fuller (ADF)**: Test for unit roots in cluster membership
- **KPSS test**: Complement to ADF, tests for trend stationarity
- **Chow test**: Detect structural breaks in cluster structure
- **Rolling window analysis**: Track cluster stability across time periods

### Metrics
- **Cluster persistence rate**: % of individuals remaining in same cluster
- **Centroid drift**: Movement of cluster centers over time
- **Silhouette score stability**: Consistency of cluster cohesion

## Application to Institutional Analysis

Stationarity testing addresses the [[Measurement crisis]] by providing:
- Operational criteria for "institution exists"
- Quantitative measures of institutional strength
- Early warning of institutional change

## Challenges

1. **Platform dynamics**: Digital platforms constantly change, affecting stationarity
2. **Multiple timescales**: Different institutions stabilize at different rates
3. **External shocks**: Policy changes, technology shifts disrupt stationarity

## Related Concepts

- [[Tier 3: Mathematical Operationalization]] - Technical details
- [[Behavioral Cluster]] - What we're testing for stationarity
- [[Trajectory Clustering]] - Method for identifying clusters
- [[Behavioral Cluster Analysis Example]] - Worked example

---

*This page addresses the broken link [[Stationarity Testing]] referenced in 3 files.*
