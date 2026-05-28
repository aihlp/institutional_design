# Benchmark: Institutional Drift Prediction

## Objective

Predict upcoming shifts in institutional norms and behavioral patterns before they occur.

## Prediction Targets

### 1. Norm Shift Detection

- **Horizon**: 7-30 days ahead
- **Signal**: Changes in behavioral cluster composition
- **Metric**: Precision/Recall on shift detection

### 2. Fragmentation Forecasting

- **Horizon**: 14-60 days ahead
- **Signal**: Increasing behavioral variance, cluster splitting
- **Metric**: AUC-ROC on fragmentation events

### 3. Convergence Prediction

- **Horizon**: 7-30 days ahead
- **Signal**: Decreasing inter-cluster distance
- **Metric**: Accuracy on convergence identification

## Features

### Leading Indicators

- Behavioral trajectory changes
- Information field entropy shifts
- Reaction pattern modifications
- Signal distribution changes

### Contextual Features

- External events
- Policy changes
- Leadership transitions
- Platform interventions

## Evaluation Protocol

1. Train on historical data up to time t
2. Predict institutional state at t+h
3. Compare predictions to observed outcomes
4. Compute accuracy metrics
5. Repeat with rolling windows

## Baseline Models

- Autoregressive baselines
- Simple trend extrapolation
- Random walk null model

## Success Criteria

- Outperform baseline models significantly
- Provide calibrated uncertainty estimates
- Generalize across platform types
- Actionable lead time for interventions

## Related Prototypes

- `prototypes/drift_forecasting_engine.py`

---

*Benchmark specification for Institutional Design Lab*
