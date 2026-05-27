# Behavioral Spectrum

## Definition

**A behavioral spectrum is the full distribution of possible reactions to a given informational signal within a defined population at a given time.**

## Purpose

The behavioral spectrum serves two critical functions in the framework:

1. **Baseline measurement**: Captures the range of behavioral variation *before* clustering
2. **Distinctiveness assessment**: Provides reference against which cluster stability and separation can be evaluated

## Formal Specification

```
Spectrum S for signal s at time t:
  S(s,t) = {r_i | agent i ∈ Population, reaction r_i to signal s}

Distribution D over reactions:
  D(r|s,t) = P(reaction = r | signal = s, time = t)
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Population-level** | Aggregates across all agents in defined population |
| **Signal-specific** | Tied to particular informational signal |
| **Time-indexed** | Can be tracked across temporal windows |
| **Pre-clustering** | Represents raw variation before grouping |
| **Comparative baseline** | Used to assess cluster distinctiveness |

## Example: Push Notification Campaign

Consider a platform sending a push notification about a new feature:

### The Signal
```
Signal: Push notification
Content: "Try our new dark mode!"
Sent: 2025-01-15 10:00:00 UTC
Population: All active mobile users (N = 1,000,000)
```

### The Spectrum (Reaction Distribution)

| Reaction | Count | Percentage |
|----------|-------|------------|
| Immediate open + enable | 45,000 | 4.5% |
| Immediate open + dismiss | 180,000 | 18.0% |
| Delayed open (>1hr) + enable | 12,000 | 1.2% |
| Delayed open (>1hr) + dismiss | 63,000 | 6.3% |
| No open, but enabled later | 28,000 | 2.8% |
| Dismissed notification | 320,000 | 32.0% |
| No interaction | 352,000 | 35.2% |

**Total**: 1,000,000 users

### Spectrum Visualization

```
Reaction Type                          │ Users (%)
                                       │
Immediate open + enable     ██████████ │ 4.5%
Immediate open + dismiss    ███████████████████████████████ │ 18.0%
Delayed open + enable       ███ │ 1.2%
Delayed open + dismiss      ███████████ │ 6.3%
No open, enabled later      ██████ │ 2.8%
Dismissed notification      ███████████████████████████████████████████████████████ │ 32.0%
No interaction              ███████████████████████████████████████████████████████████████ │ 35.2%
                                       │
└────────────────────────────────────────────────────────┘
                    BEHAVIORAL SPECTRUM
```

## Relationship to Clusters

The spectrum is the **input** to clustering; clusters are the **output**.

```
BEHAVIORAL SPECTRUM              →  CLUSTERING ALGORITHM  →  BEHAVIORAL CLUSTERS
(Raw distribution)                  (UMAP, HDBSCAN, etc.)     (Grouped patterns)
     │                                                        │
     └────────────────────────────────────────────────────────┘
                         Comparison: Are clusters distinct from spectrum?
```

### Assessing Cluster Quality

A good clustering should:
1. **Capture spectrum structure**: Major modes in spectrum become cluster centers
2. **Explain variance**: Within-cluster variance < Total spectrum variance
3. **Maintain interpretability**: Clusters map to recognizable pattern types

## Temporal Dynamics

Spectra can change over time, revealing institutional evolution:

```
Time Window 1 (Week 1):          Time Window 2 (Week 4):
                                 
Bimodal distribution             Unimodal distribution
│                                │
│    ██            ██            │         ████████
│    ██            ██            │         ████████
│    ██            ██            │         ████████
│____██____________██____        │_________████████________
     Enable   Dismiss                     Enable
                                             
Interpretation: Norm has shifted; dark mode now default expectation
```

## Measurement Requirements

To construct behavioral spectra:

1. **Signal identification**
   - Unique signal ID
   - Signal type classification
   - Delivery timestamp

2. **Reaction taxonomy**
   - Predefined reaction categories
   - Consistent coding across signals
   - Granularity appropriate to research question

3. **Population definition**
   - Clear inclusion/exclusion criteria
   - Demographic stratification (optional)
   - Sample size documentation

## Analytical Uses

### Baseline Comparison
Compare spectra across:
- Different signals (which produces more varied responses?)
- Different populations (do demographics react differently?)
- Different time periods (is behavior stabilizing?)

### Cluster Validation
- Do identified clusters capture major spectrum modes?
- Is residual variance within acceptable bounds?

### Institutional Change Detection
- Spectrum narrowing = increasing homogeneity (institution solidifying)
- Spectrum widening = increasing diversity (institution weakening)
- Mode shifts = behavioral norm changing

### Intervention Assessment
Measure how policy changes affect the spectrum:
- Before intervention: Wide spectrum, multiple modes
- After intervention: Narrow spectrum, single dominant mode

## Related Entries

- [[Behavioral Trajectory]] - Individual sequences that compose spectrum
- [[Behavioral Cluster]] - Groupings derived from spectrum
- [[From Rules to Behavioral Clusters]] - Core framework proposal
- [[Tier 1: Base Definitions]] - Foundational primitives
- [[Tier 3: Mathematical Operationalization]] - Statistical methods

## Categories

[[Core Concepts]], [[New Empirical Foundation]]
