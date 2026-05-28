# Core Concepts

## Overview

This category contains detailed entries on the fundamental concepts used in the behavioral cluster framework for institutional analysis.

## The Five Primitives (Tier 1)

These are the foundational building blocks that map directly to observable data:

### 1. [[Informational Signal]]
Any objectively recordable change in the information environment.
- Timestamped event with source and type
- Examples: notifications, content posts, UI changes, policy announcements
- Role: Triggers agent reactions

### 2. [[Reaction]]
A discrete, logged action or inaction by an agent in response to a signal.
- Both actions (clicks, purchases) and inactions (scroll-past, ignore) count
- No inference about mental states required
- Role: Basic unit of behavioral response

### 3. [[Behavioral Trajectory]]
Time-ordered sequence of reactions produced by a single agent.
- Individual-level analogue of "behavior"
- Fully specified by timestamped, observable actions
- Role: Input to clustering algorithms

### 4. [[Behavioral Spectrum]]
Full distribution of possible reactions to a signal within a population.
- Captures variation before clustering
- Serves as baseline for assessing cluster distinctiveness
- Role: Reference distribution

### 5. [[Behavioral Cluster]]
Grouping of similar behavioral trajectories identified through unsupervised learning.
- What the analyst identifies as sufficiently stable to call an "institution"
- Constructed using explicit, reproducible criteria
- Role: The institution itself in the new framework

## Derived Concepts

### Institutional Properties
- **Stability**: Temporal persistence measured by stationarity tests
- **Distinctiveness**: Separation from other clusters in trajectory space
- **Self-reinforcement**: Tendency to reproduce itself over time

### Analytical Tools
- **Clustering algorithms**: UMAP, HDBSCAN, k-means
- **Stationarity tests**: ADF, KPSS
- **Transition matrices**: Markov chains for measuring fluidity
- **Contagion models**: Network-based propagation simulation

## Philosophical Foundation

### [[Rapoport's Subjectivism]]
- Institutions are constructed by analysts, not discovered in nature
- Analyst's criteria are explicit methodological choices
- Operationalization is the primary conceptual act

## Relationship Map

```
INFORMATIONAL SIGNAL
        ↓ (triggers)
   REACTION
        ↓ (sequences form)
BEHAVIORAL TRAJECTORY
        ↓ (distribution = )
BEHAVIORAL SPECTRUM
        ↓ (clustered into)
BEHAVIORAL CLUSTER ← INSTITUTION IDENTIFIED
```

## Connection to Other Categories

| Related Category | Relationship |
|------------------|--------------|
| [[Classical Institutional Theory]] | These concepts replace classical vocabulary |
| [[New Empirical Foundation]] | These are the core concepts of that framework |
| [[Digital Platforms as Empirical Stress Tests]] | These concepts handle phenomena documented there |

## Why These Concepts Matter

The classical vocabulary (rules, norms, shared beliefs) cannot be operationalized because it refers to latent constructs beneath observable behavior.

The new vocabulary (signals, reactions, trajectories, clusters) maps directly to data that platforms already collect, enabling:
- Direct measurement without inference
- Reproducible identification procedures
- Falsifiable empirical claims
- Cumulative science building across studies

---

*Part of the [[Institutional Theory Wiki]]*
