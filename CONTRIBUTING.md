# Contributing to the Institutional Design Lab

Thank you for your interest in contributing to the Institutional Design Lab! This document provides guidelines and instructions for contributing to our open computational research laboratory.

## 🎯 How to Contribute

We welcome contributions in many forms:

- **Code**: Implementing new features, fixing bugs, improving performance
- **Documentation**: Writing tutorials, improving existing docs, adding examples
- **Research**: Developing theoretical frameworks, conducting experiments
- **Data**: Curating datasets, creating benchmarks, validating data quality
- **Review**: Code reviews, documentation reviews, testing
- **Community**: Answering questions, organizing events, outreach

## 🚀 Getting Started

### 1. Set Up Your Environment

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/institutional_design.git
cd institutional_design

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Find Something to Work On

- Browse [open issues](https://github.com/aihlp/institutional_design/issues)
- Check issues labeled `good first issue` for beginner-friendly tasks
- Look at our [roadmap](ROADMAP.md) for strategic priorities
- Start a discussion if you have a new idea

### 3. Understand Our Structure

```
institutional_design/
├── lab/                    # Core research components
├── infrastructure/         # Data processing pipelines
├── datasets/              # Dataset tools and metadata
├── simulations/           # Simulation frameworks
├── prototypes/            # Working prototypes
├── notebooks/             # Jupyter notebooks
├── papers/                # Research papers
└── benchmarks/            # Benchmark suites
```

## 📝 Development Workflow

### Branch Naming Convention

```
feature/description          # New features
fix/description              # Bug fixes
docs/description             # Documentation changes
test/description             # Test additions
refactor/description         # Code refactoring
experiment/description       # Research experiments
```

### Commit Message Format

We follow conventional commits:

```
feat: add institutional cluster detector
fix: correct stability calculation in ADF tests
docs: update README with simulation examples
test: add unit tests for entropy monitor
refactor: simplify signal processing pipeline
```

### Pull Request Process

1. **Create a branch** from `main`
2. **Make your changes** with tests
3. **Run pre-commit hooks**: `pre-commit run --all-files`
4. **Ensure all tests pass**: `pytest`
5. **Update documentation** as needed
6. **Submit PR** with clear description
7. **Address review feedback**
8. **Squash commits** if requested
9. **Merge** after approval

## 🔬 Research Contributions

### Theoretical Frameworks

When contributing to the theoretical framework:

1. **Define primitives clearly** using the standard format:
   - Formal definition
   - Operational measurement
   - Empirical examples
   - Relationships to other primitives

2. **Provide mathematical formalization** where applicable

3. **Link to empirical evidence** or propose validation methods

4. **Consider implications** for the broader framework

### Simulation Development

For simulation contributions:

1. **Document assumptions** clearly
2. **Provide reproducible random seeds**
3. **Include sensitivity analysis**
4. **Compare with baseline models**
5. **Validate against empirical data** when possible

### Dataset Curation

When adding dataset metadata or loaders:

1. **Complete metadata documentation**
2. **Specify licensing and usage terms**
3. **Document preprocessing steps**
4. **Include quality metrics**
5. **Provide access instructions**

## 🧪 Testing Requirements

### Unit Tests

All new code must include unit tests:

```python
def test_institutional_stability_detection():
    """Test that stable behavioral clusters are correctly identified."""
    # Arrange
    reactions = generate_test_reactions(n=1000)
    
    # Act
    clusters = detect_institutions(reactions, method='adf')
    
    # Assert
    assert len(clusters) > 0
    assert all(c.stability_score > 0.95 for c in clusters)
```

### Integration Tests

For larger features, include integration tests:

```python
def test_full_pipeline():
    """Test complete institutional detection pipeline."""
    # Test from raw data to institutional map
    pass
```

### Performance Benchmarks

For performance-critical code:

```python
@pytest.mark.benchmark
def test_cluster_detector_performance(benchmark):
    """Benchmark institutional cluster detector."""
    result = benchmark(detect_institutions, large_dataset)
    assert result.processing_time < 5.0  # seconds
```

## 📚 Documentation Standards

### Code Documentation

All public functions and classes must have docstrings:

```python
def detect_institutional_clusters(
    reactions: List[Reaction],
    method: str = 'adf',
    threshold: float = 0.95
) -> InstitutionalMap:
    """
    Detect stable institutional clusters from behavioral reactions.
    
    Args:
        reactions: List of behavioral reactions to analyze
        method: Stability detection method ('adf', 'kpss', 'combined')
        threshold: Minimum stability score (0-1)
    
    Returns:
        InstitutionalMap containing detected clusters and metadata
    
    Raises:
        ValueError: If threshold is outside [0, 1]
        EmptyDataError: If no reactions provided
    
    Example:
        >>> reactions = load_reactions('dataset.csv')
        >>> inst_map = detect_institutional_clusters(reactions)
        >>> print(f"Found {len(inst_map.clusters)} institutions")
    """
```

### User Documentation

User-facing documentation should include:

- **Installation instructions**
- **Quick start guide**
- **Detailed tutorials**
- **API reference**
- **Troubleshooting guide**
- **FAQ**

## 🎨 Code Style

We use standard Python style guidelines:

- **PEP 8** for code style
- **Type hints** for all functions
- **Black** for formatting
- **isort** for imports
- **flake8** for linting
- **mypy** for type checking

Set up pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## 🔍 Review Process

### What Reviewers Look For

1. **Correctness**: Does the code work as intended?
2. **Tests**: Are there adequate tests?
3. **Documentation**: Is it well documented?
4. **Style**: Does it follow our style guidelines?
5. **Performance**: Is it reasonably efficient?
6. **Security**: Are there any security concerns?
7. **Ethics**: Does it comply with our ethics guidelines?

### Review Response Time

- We aim to review PRs within **1 week**
- Complex PRs may take longer
- Feel free to ping after 1 week if no response

## 🏷️ Issue Labels

We use labels to categorize issues:

### Type
- `bug`: Something isn't working
- `feature`: New feature request
- `documentation`: Documentation improvements
- `performance`: Performance improvements
- `refactor`: Code refactoring
- `question`: Question about the project

### Priority
- `critical`: Blocks major functionality
- `high`: Important but not blocking
- `medium`: Normal priority
- `low`: Nice to have
- `good first issue`: Good for newcomers

### Status
- `help wanted`: Extra attention is needed
- `in progress`: Currently being worked on
- `needs review`: Ready for review
- `blocked`: Waiting on something else

## 💬 Communication

### Where to Communicate

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Discord/Slack**: For real-time chat (link in README)
- **Email**: For sensitive matters (see GOVERNANCE.md)

### Asking Questions

When asking questions:

1. **Search first** to see if it's been answered
2. **Be specific** about what you're trying to do
3. **Include context** and what you've tried
4. **Provide examples** when possible
5. **Be patient** while waiting for a response

## 🎓 Learning Resources

### Recommended Reading

1. Core framework documentation in `lab/ontology/`
2. Key papers in `papers/` directory
3. Simulation examples in `notebooks/`
4. Benchmark documentation in `benchmarks/`

### Tutorials

Check our tutorial series:
- Getting started with institutional analysis
- Building your first simulation
- Working with behavioral datasets
- Understanding the primitive chain

## 🌟 Recognition

We recognize contributors through:

- **Contributor list** in README
- **Release notes** mentioning significant contributions
- **Annual report** highlighting key contributors
- **Co-authorship** on papers when appropriate
- **Speaking opportunities** at project events

## ❓ FAQ

**Q: Do I need a PhD to contribute?**  
A: No! We welcome contributors from all backgrounds. Different perspectives strengthen our research.

**Q: Can I contribute without coding?**  
A: Absolutely! Documentation, testing, community building, and research are all valuable contributions.

**Q: How long does it take to get a PR merged?**  
A: It varies. Simple fixes might be merged in days, while complex features may take weeks of discussion and refinement.

**Q: Who owns the code I contribute?**  
A: Contributors retain copyright but license their contributions under the project's open-source license. See LICENSE for details.

**Q: Can I use this for commercial purposes?**  
A: Yes, within the terms of our license. See LICENSE and ETHICS.md for restrictions on harmful uses.

---

Thank you for contributing to the Institutional Design Lab! Together, we're building open computational infrastructure for understanding institutional dynamics.

For more information, see:
- [GOVERNANCE.md](GOVERNANCE.md) - Governance framework
- [ETHICS.md](ETHICS.md) - Ethics principles
- [ROADMAP.md](ROADMAP.md) - Project roadmap
- [README.md](README.md) - Project overview
