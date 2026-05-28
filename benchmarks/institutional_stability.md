# Benchmark: Institutional Stability Measurement

## Objective

Measure the stability of behavioral clusters and institutional patterns over time.

## Metrics

### 1. Cluster Persistence

- **Definition**: Fraction of cluster members remaining stable across time windows
- **Formula**: `persistence(t1, t2) = |members(t1) ∩ members(t2)| / |members(t1)|`
- **Target**: >0.7 for stable institutions

### 2. Behavioral Variance

- **Definition**: Within-cluster behavioral variance over time
- **Formula**: `variance = Σ(behavior_i - cluster_mean)² / n`
- **Target**: Low variance indicates strong norms

### 3. Transition Rate

- **Definition**: Rate at which agents switch between clusters
- **Formula**: `transition_rate = switches / (agents × time_periods)`
- **Target**: <0.1 for stable institutions

### 4. Norm Enforcement Frequency

- **Definition**: Rate of sanctioning or corrective actions
- **Measurement**: Count of moderation events, warnings, exclusions
- **Target**: Context-dependent

## Evaluation Protocol

1. Split data into consecutive time windows
2. Identify behavioral clusters in each window
3. Track cluster membership changes
4. Compute metrics above
5. Compare against baseline expectations

## Baseline Datasets

- Reddit community data
- Wikipedia editor behavior
- GitHub contribution patterns

## Success Criteria

- Accurate detection of known stable vs unstable communities
- Prediction of institutional breakdown before observable collapse
- Cross-platform generalization

## Related Simulations

- `simulations/institutions/stability_model.py`
- `simulations/transitions/drift_detection.py`

---

*Benchmark specification for Institutional Design Lab*
