# Institutional Analysis Experiments

This directory contains the executable experimental pipeline for institutional science research.

## Quick Start

### Run Synthetic Baseline Experiment

```bash
python experiments/run_experiment.py --dataset synthetic --scenario baseline --events 500
```

### Run Intervention Experiment

```bash
python experiments/run_experiment.py --dataset synthetic --scenario intervention --events 1000
```

### Run with Reddit Data

```bash
python experiments/run_experiment.py --dataset reddit --subreddit science --events 500
```

### Run with LLM Interpretation

```bash
export OPENROUTER_API_KEY="your-api-key"
python experiments/run_experiment.py --dataset synthetic --scenario baseline --llm
```

## Pipeline Stages

The experiment pipeline executes these stages:

1. **Dataset Download/Generation** - Load or generate behavioral traces
2. **Normalization** - Convert to canonical schema
3. **Metrics Calculation** - Compute entropy, density, volatility, etc.
4. **Institutional Mapping** - Build trajectories and detect clusters
5. **Visualization Generation** - Create graphs and timelines
6. **Forecasting Experiment** - Predict drift patterns
7. **LLM Interpretation** (optional) - Semantic analysis of clusters
8. **Benchmark Output** - Standardized results format

## Available Datasets

| Dataset | Type | Purpose |
|---------|------|---------|
| `synthetic` | Simulated | Controlled experiments, baseline testing |
| `reddit` | Social media | Norm emergence, moderation effects |
| `wikipedia` | Collaborative | Governance, edit wars, conflict resolution |
| `github` | Development | Coordination norms, contribution patterns |

## Synthetic Scenarios

- `baseline` - Natural institutional emergence
- `intervention` - Mid-stream moderation/ranking change
- `drift` - Gradual fragmentation or convergence

## Output Files

Experiments produce these outputs in `experiments/output/`:

- `experiment_results.json` - Complete results
- `benchmark_output.json` - Standardized benchmark format
- `experiment_summary.json` - Summary report
- `cluster_graph.json` - Network visualization data
- `entropy_timeline.json` - Temporal metrics
- `trajectory_map.json` - Behavioral patterns
- `intervention_comparison.json` - Before/after analysis

## Benchmark Output Format

```json
{
  "dataset": "synthetic:baseline",
  "clusters_detected": 3,
  "entropy_score": 2.45,
  "volatility_score": 0.12,
  "stability_score": 0.78,
  "polarization_score": 0.23,
  "convergence_score": 0.15,
  "predicted_drift": "stable",
  "intervention_effect": ""
}
```

## GitHub Actions Integration

Experiments can be triggered automatically via GitHub Actions:

1. Push to main branch triggers baseline experiment
2. Manual workflow dispatch allows custom parameters
3. Results uploaded as artifacts for download

## API Reference

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--dataset` | synthetic | Dataset type |
| `--scenario` | baseline | Scenario (synthetic only) |
| `--subreddit` | science | Subreddit (Reddit only) |
| `--events` | 500 | Number of events |
| `--output` | experiments/output | Output directory |
| `--llm` | false | Enable LLM interpretation |

## Success Criteria

The pipeline is operational when it can:

- ✅ Download/generate open datasets automatically
- ✅ Normalize behavioral traces to canonical schema
- ✅ Build institutional trajectories
- ✅ Detect stable behavioral clusters
- ✅ Measure entropy and volatility
- ✅ Generate institutional visualizations
- ✅ Run intervention simulations
- ✅ Forecast simple drift patterns
- ✅ Produce reproducible metrics
- ✅ Generate semantic interpretations (with LLM)
