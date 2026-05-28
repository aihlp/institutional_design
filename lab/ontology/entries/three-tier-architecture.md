# Three-Tier Research Architecture

## Summary

The redefinition of institutions as behavioral clusters supports a full research architecture organized into three interdependent tiers.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Tier 3: Mathematical Operationalization                │
│  (Computational & Statistical Toolkit)                  │
├─────────────────────────────────────────────────────────┤
│  Tier 2: Theoretical Scaffold                           │
│  (Explanatory Mechanisms)                               │
├─────────────────────────────────────────────────────────┤
│  Tier 1: Base Definitions                               │
│  (Primitives Translatable to Digital Traces)            │
└─────────────────────────────────────────────────────────┘
```

**Key principle**: Tiers are not sequential stages but **interdependent layers**. Progress in any tier creates new possibilities—and obligations—in the others.

---

## Tier 1: Base Definitions

### Purpose
Foundational layer consisting of primitives directly translatable into digital behavioral traces.

### Core Primitives

| Primitive | Definition | Data Mapping |
|-----------|------------|--------------|
| **Informational Signal** | Any objectively recordable change in information environment | Timestamped event with source and type |
| **Reaction** | Discrete, logged action or inaction | Click, scroll, purchase, skip, etc. |
| **Behavioral Cluster** | Grouping of similar reaction trajectories | Output of unsupervised learning |

### Key Feature
**No unobservable constructs required.** Each primitive maps onto specific data types that platforms already collect.

### See Also
[[Tier 1: Base Definitions]] - Detailed treatment

---

## Tier 2: Theoretical Scaffold

### Purpose
Provides explanatory mechanisms connecting the primitives.

### Core Mechanisms

#### 1. Perception Filters
- Agent-specific transformation of signal into subjective stimulus
- Explains why same signal produces different reactions across agents

#### 2. Habituation and Social Learning
- Micro-foundations of pattern stability
- How repeated exposure produces stable trajectories
- How observation of others shapes individual behavior

#### 3. Opportunism
- Behavioral premise following **Williamson (1985)**
- Agents interpret signals through hierarchy of personal-to-societal interests
- Explains strategic adaptation within institutional patterns

#### 4. Signal-to-Norm Dynamics
- Institutional patterns, once stabilized, feed back to reshape informational environment
- New signals processed through lens of existing clusters
- Explains institutional evolution and path dependence

### Convergent Support

**Trumble (2025)**:
- Platform metrics function as "gravitational centers of behavior"
- Produces stable behavioral patterns directly measurable
- Emerges from different theoretical tradition but arrives at compatible conclusion

**Entsminger and Westgren (2019)**:
- Demonstrated cluster analysis can operationalize institutional taxonomy
- Used observational data on organizational forms
- Provides precedent for Tier 3 toolkit application

### See Also
[[Tier 2: Theoretical Scaffold]] - Detailed treatment

---

## Tier 3: Mathematical Operationalization

### Purpose
Computational and statistical toolkit for making framework empirically verifiable.

### Core Tools

| Tool | Function | Purpose |
|------|----------|---------|
| **Trajectory Clustering** (UMAP, HDBSCAN) | Identify behavioral clusters | Unsupervised grouping of similar trajectories |
| **Stationarity Testing** (ADF, KPSS) | Measure temporal stability | Determine if cluster persists over time |
| **Inter-cluster Transition Matrices** (Markov chains) | Measure institutional fluidity | Track movement between clusters, competition |
| **Network-based Contagion Models** | Simulate social propagation | Model cascade dynamics, diffusion patterns |

### Complete Measurement System

Taken together, these tools constitute:
- From raw behavioral logs → identified institutions
- With **quantified uncertainty at every step**
- Fully reproducible pipeline

### See Also
[[Tier 3: Mathematical Operationalization]] - Detailed treatment

---

## Interdependence Principle

The three tiers are **not** a linear pipeline:

| Relationship | Description |
|--------------|-------------|
| **Tier 1 → Tier 2** | Primitives constrain what theory can explain |
| **Tier 2 → Tier 3** | Scaffold determines what questions are worth asking |
| **Tier 3 → Tier 1** | Operationalization tools determine what can be empirically adjudicated |

### Example of Interdependence

1. **Tier 3 advance**: New clustering algorithm detects finer-grained patterns
   → **Tier 1 obligation**: Refine definition of "behavioral trajectory"
   → **Tier 2 question**: What mechanisms produce these finer patterns?

2. **Tier 2 insight**: Signal-to-norm dynamics suggest feedback loops
   → **Tier 3 requirement**: Need time-series models with feedback
   → **Tier 1 implication**: Must track signal history alongside trajectories

## Related Entries

- [[From Rules to Behavioral Clusters]] - Foundation of the architecture
- [[Rapoport's Subjectivism]] - Philosophical basis
- [[Tier 1: Base Definitions]] - Detailed Tier 1
- [[Tier 2: Theoretical Scaffold]] - Detailed Tier 2
- [[Tier 3: Mathematical Operationalization]] - Detailed Tier 3
- [[The Paradox at the Heart of Institutional Theory]] - Main crisis overview

## Categories

[[New Empirical Foundation]], [[Core Concepts]]
