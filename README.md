# Institutional Design Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Status: Active Development](https://img.shields.io/badge/status-active%20development-success)](.)

**Open computational infrastructure for measuring, modeling, simulating, and forecasting institutional dynamics from behavioral data in AI-mediated systems.**

---

## 🎯 Mission

The Institutional Design Lab transforms institutional theory into a **computational science**. We replace unobservable constructs (rules, norms, shared beliefs) with **observable, measurable behavioral primitives**, enabling:

- 🔬 **Empirical measurement** of institutional phenomena
- 📊 **Quantitative analysis** of institutional change
- 🤖 **Simulation** of institutional evolution
- 🔮 **Forecasting** of institutional transitions
- 🧪 **Testing** of governance interventions before deployment

This is **not just a research project**—it's infrastructure for a new scientific paradigm.

---

## 🌍 Research Vision

### The Problem

Classical institutional theory relies on **unobservable latent constructs**:
- "Rules of the game" (North)
- "Three pillars" (Scott)
- "Shared beliefs" (Aoki)

These cannot be directly measured, tracked, or modeled computationally, creating a **measurement crisis** that prevents rigorous empirical testing, predictive modeling, computational simulation, and cross-context comparison.

### Our Solution

We reconstitute institutional theory using **7 behavioral primitives** that are observable, measurable, computable, and composable:

```
Informational Signal → Perception Filter → Stimulus → Reaction → Pattern → Stability → Spectrum
```

An **institution** emerges as a *stable cluster of behavioral reactions* to identifiable signals.

### Core Research Directions

| Direction | Focus | Key Questions |
|-----------|-------|---------------|
| **Institutional Dynamics** | Emergence, stability, change | How do institutions form? What makes them stable? Why do they collapse? |
| **Information Fields** | Environmental parameters | How does information density affect institutions? What role does entropy play? |
| **Behavioral Forecasting** | Prediction & early warning | Can we predict institutional transitions? What are leading indicators? |
| **Institutional Drift** | Gradual change & transformation | How do institutions evolve over time? |
| **Governance Simulation** | Intervention testing | How can we test policies before deployment? |
| **Signal Interventions** | Deliberate design | How do we design signals to achieve desired outcomes? |

---

## 🏗️ Repository Architecture

```
institutional_design/
│
├── 📄 Core Documentation
│   ├── README.md              # Project overview
│   ├── ROADMAP.md             # Strategic plan & milestones
│   ├── CONTRIBUTING.md        # How to contribute
│   ├── GOVERNANCE.md          # Governance framework
│   ├── ETHICS.md              # Ethics principles & safeguards
│   └── CITATION.cff           # Citation information
│
├── 🔬 lab/                    # Core research components
│   ├── ontology/              # Formal definitions & relationships
│   ├── primitives/            # 7 behavioral primitives
│   ├── mechanisms/            # Selection, transmission, evolution
│   ├── institutional_models/  # Lifecycle, drift models
│   ├── forecasting/           # Prediction algorithms
│   └── references/            # Bibliography
│
├── ⚙️ infrastructure/         # Data pipelines & automation
│   ├── ingestion/             # Data source connectors
│   ├── extraction/            # Feature extraction
│   ├── processing/            # Data transformation
│   ├── wiki_sync/             # Wiki integration
│   ├── graph_generation/      # Knowledge graphs
│   └── automation/            # CI/CD & workflows
│
├── 📊 datasets/               # Dataset registry & tools
│   ├── registry/              # Dataset documentation
│   ├── loaders/               # Data loading utilities
│   ├── schemas/               # Data schemas
│   ├── synthetic/             # Synthetic data generators
│   ├── benchmarks/            # Benchmark datasets
│   └── metadata/              # Metadata standards
│
├── 🎮 simulations/            # Simulation frameworks
│   ├── agents/                # Agent architectures
│   ├── signals/               # Signal generation
│   ├── filters/               # Filter models
│   ├── reactions/             # Reaction mechanisms
│   ├── institutions/          # Institutional emergence
│   ├── entropy/               # Information field dynamics
│   ├── transitions/           # State transitions
│   ├── interventions/         # Policy interventions
│   └── visualization/         # Visualization tools
│
├── 🛠️ prototypes/             # Working prototypes
│   ├── institutional_cluster_detector/
│   ├── entropy_monitor/
│   ├── drift_forecaster/
│   └── intervention_simulator/
│
├── 📓 notebooks/              # Jupyter notebooks
├── 📑 papers/                 # Research papers
├── 📏 benchmarks/             # Benchmark suites
└── 🧰 wiki_tools/             # Wiki synchronization tools
    └── archive/               # Historical files
```

---

## 📚 Datasets

We support an **open-first** data strategy providing metadata, loaders, preprocessing pipelines, quality metrics, and documentation.

### Supported Data Sources

| Source | Type | Scale | Status |
|--------|------|-------|--------|
| **Reddit** | Discussions, comments, votes | 10M+ interactions | 🟡 In Progress |
| **Wikipedia** | Edit histories, talk pages | 50M+ edits | 🟡 In Progress |
| **GitHub** | Issues, PRs, discussions | 5M+ events | 🟡 In Progress |
| **Gaming Platforms** | Player behaviors, guilds | Coming Soon | ⚪ Planned |
| **Mobility Systems** | Transit usage patterns | Coming Soon | ⚪ Planned |
| **Financial Systems** | Trading behaviors | Coming Soon | ⚪ Planned |

📖 See `datasets/registry/` for detailed documentation.

---

## 🎮 Simulations

Our simulation framework enables **virtual experimentation** with institutional dynamics:

| Type | Description | Use Cases |
|------|-------------|-----------|
| **Institutional Emergence** | Norm formation and stabilization | Study how institutions arise |
| **Institutional Drift** | Gradual change and fragmentation | Understand long-term evolution |
| **Intervention Testing** | Policy changes before deployment | Evaluate moderation, ranking |
| **Information Field Dynamics** | Entropy, polarization, propagation | Analyze information effects |

📖 See `simulations/` for full documentation.

---

## 🛠️ Prototypes

### 1. Institutional Cluster Detector
Detects stable behavioral clusters representing institutions using ADF/KPSS stationarity tests.

### 2. Information Field Entropy Monitor
Measures density, entropy, polarization, and concentration with real-time dashboards.

### 3. Institutional Drift Forecasting Engine
Predicts norm shifts, convergence, radicalization, and decay.

### 4. Signal Intervention Simulator
Tests interventions (moderation, ranking, nudges) before real-world deployment.

---

## 🔬 The 7 Behavioral Primitives

1. **Informational Signal** - Objectively recordable change (timestamp, source, type)
2. **Perception Filter** - Agent-specific decoding (cognitive, cultural)
3. **Stimulus** - Subjective meaning after filtering
4. **Reaction** - Discrete action/inaction (atomic unit)
5. **Behavioral Pattern** - Reproducible sequence over time
6. **Stability** - Statistical stationarity (ADF/KPSS tests)
7. **Behavioral Spectrum** - Full distribution of stable reactions

**Definition**: An *institution* is a stable, empirically distinguishable cluster of behavioral reactions representing one alternative from the spectrum of responses to an identifiable informational signal.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/aihlp/institutional_design.git
cd institutional_design

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from lab.primitives import Signal, Reaction
from prototypes.institutional_cluster_detector import detect_institutions

data = load_dataset('example_reddit')
signals = Signal.extract(data)
reactions = Reaction.classify(data)
institutions = detect_institutions(reactions)
institutions.plot_network()
```

---

## 🤝 Contributing

We welcome contributions in code, documentation, research, datasets, testing, and community engagement.

### Getting Started
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [open issues](https://github.com/aihlp/institutional_design/issues)
3. Join [Discussions](https://github.com/aihlp/institutional_design/discussions)
4. Review [ROADMAP.md](ROADMAP.md)

Look for issues labeled `good first issue` to get started!

---

## 📜 Governance & Ethics

### Ethical Commitments - We Prohibit:
- ❌ Authoritarian misuse and surveillance
- ❌ Covert manipulation without consent
- ❌ Harmful behavioral exploitation
- ❌ Discriminatory targeting
- ❌ Democratic institution undermining

### Governance Principles:
- ✅ Transparency in methods and findings
- ✅ Open science and reproducibility
- ✅ Community-driven decision making
- ✅ Regular ethics review
- ✅ Responsible innovation

📖 See [ETHICS.md](ETHICS.md) and [GOVERNANCE.md](GOVERNANCE.md).

---

## 📈 Roadmap

### Current Phase: Foundation (Q2-Q3 2025)
- ✅ Repository restructuring
- ✅ Governance documents
- 🟡 Ontology documentation
- 🟡 Core primitives implementation

### Upcoming Milestones
| Quarter | Focus | Key Deliverables |
|---------|-------|------------------|
| Q3 2025 | Core Infrastructure | Primitives library, cluster detector |
| Q4 2025 | Simulation Framework | Agent-based models |
| Q1 2026 | Dataset Expansion | Reddit, Wikipedia, GitHub |
| Q2 2026 | Research Program | First papers |

📖 See [ROADMAP.md](ROADMAP.md).

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [ROADMAP.md](ROADMAP.md) | Strategic plan |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [GOVERNANCE.md](GOVERNANCE.md) | Governance framework |
| [ETHICS.md](ETHICS.md) | Ethics principles |
| [Wiki](https://github.com/aihlp/institutional_design/wiki) | Knowledge base |

---

## 🔗 Resources

- **Wiki**: [github.com/aihlp/institutional_design/wiki](https://github.com/aihlp/institutional_design/wiki)
- **Issues**: [github.com/aihlp/institutional_design/issues](https://github.com/aihlp/institutional_design/issues)
- **Discussions**: [github.com/aihlp/institutional_design/discussions](https://github.com/aihlp/institutional_design/discussions)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

*Last updated: May 2025 | Version: 2.0 - Institutional Design Lab Edition*

**Together, we're building the future of computational institutional science.**
