# Behavioral Trajectory

## Definition

**A behavioral trajectory is the time-ordered sequence of reactions produced by a single agent in response to a stream of identifiable informational signals.**

## Formal Specification

```
Trajectory T_i for agent i:
  T_i = [(t_1, s_1, r_1), (t_2, s_2, r_2), ..., (t_n, s_n, r_n)]

Where:
  t_k = timestamp of k-th interaction
  s_k = informational signal encountered
  r_k = reaction (action or inaction)
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Time-ordered** | Sequence preserves temporal structure |
| **Individual-level** | One trajectory per agent |
| **Fully specified** | No unobservable mental states required |
| **Observable** | Composed entirely of logged actions/inactions |
| **Granular** | Captures fine-grained behavioral variation |

## Contrast with Classical "Behavior"

| Classical Concept | Behavioral Trajectory |
|-------------------|----------------------|
| Vague, aggregate notion | Precise, individual sequence |
| Inferred from outcomes | Directly observed in logs |
| Requires interpretation of intentions | Requires only timestamped records |
| "User engaged with content" | [(t₁, notification_A, click), (t₂, post_B, scroll_past), ...] |

## Example: E-commerce Platform

```
User_ID: U_12847

Trajectory segment (2025-01-15):
  09:23:14 - Signal: "Flash sale" email → Reaction: Opened
  09:24:01 - Signal: Product page (headphones) → Reaction: Viewed 47 seconds
  09:24:48 - Signal: "Add to cart" prompt → Reaction: Clicked
  09:25:12 - Signal: Checkout page → Reaction: Abandoned
  14:32:00 - Signal: Retargeting ad → Reaction: Ignored
  18:45:33 - Signal: Push notification → Reaction: Dismissed
```

## Role in the Framework

### Tier 1: Base Definitions
- Foundational primitive
- Maps directly to platform data logs
- No inference required

### Tier 2: Theoretical Scaffold
- Input to perception filter models
- Unit of analysis for habituation studies
- Basis for social learning mechanisms

### Tier 3: Mathematical Operationalization
- Input to clustering algorithms (UMAP, HDBSCAN)
- Subject of stationarity tests
- Element of transition matrices

## Measurement Requirements

To construct behavioral trajectories, platforms must log:

1. **Signal metadata**
   - Signal type (notification, ad, UI element, etc.)
   - Signal source (algorithm, user, system)
   - Signal content (or content ID)

2. **Reaction data**
   - Action type (click, scroll, purchase, skip, etc.)
   - Timestamp (millisecond precision recommended)
   - Context (device, location, session state)

3. **Agent identifier**
   - Persistent user ID
   - Session identifiers
   - Cross-device linkage (where available)

## Analytical Uses

### Clustering
Group similar trajectories to identify behavioral clusters (institutions).

### Stationarity Testing
Determine if trajectory patterns remain stable over time.

### Transition Analysis
Track how agents move between different trajectory types.

### Counterfactual Comparison
Compare trajectories under different signal conditions.

## Related Entries

- [[Behavioral Cluster]] - Groupings of similar trajectories
- [[Behavioral Spectrum]] - Distribution of all possible trajectories
- [[From Rules to Behavioral Clusters]] - Core framework proposal
- [[Tier 1: Base Definitions]] - Foundational layer
- [[Tier 3: Mathematical Operationalization]] - Clustering methods

## Categories

[[Core Concepts]], [[New Empirical Foundation]]
