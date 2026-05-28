"""
Core Institutional Science Library

This package provides the core infrastructure for institutional analysis:

- institutional_primitives: Signal, Reaction, Trajectory, Cluster, Institution
- dataset_loaders: Reddit, Wikipedia, GitHub, Synthetic data generators
- metrics_engine: Entropy, density, volatility, polarization metrics
- clustering_engine: Behavioral cluster detection
- visualization_engine: Graph and timeline generation
- openrouter_client: LLM integration for semantic analysis
"""

from .institutional_primitives import (
    Signal, Reaction, BehavioralTrajectory, BehavioralCluster,
    Institution, InformationField, Intervention, Forecast,
    SignalType, ReactionType, create_normalized_event
)

from .dataset_loaders import (
    RedditLoader, WikipediaLoader, GitHubLoader, SyntheticDataGenerator,
    NormalizedEvent, get_loader
)

from .metrics_engine import InstitutionalMetrics, create_benchmark_output

from .clustering_engine import BehavioralClusterDetector, build_trajectories_from_events

from .visualization_engine import InstitutionalVisualizer

__version__ = "0.1.0"
__all__ = [
    # Primitives
    'Signal', 'Reaction', 'BehavioralTrajectory', 'BehavioralCluster',
    'Institution', 'InformationField', 'Intervention', 'Forecast',
    'SignalType', 'ReactionType', 'create_normalized_event',
    
    # Loaders
    'RedditLoader', 'WikipediaLoader', 'GitHubLoader', 'SyntheticDataGenerator',
    'NormalizedEvent', 'get_loader',
    
    # Metrics
    'InstitutionalMetrics', 'create_benchmark_output',
    
    # Clustering
    'BehavioralClusterDetector', 'build_trajectories_from_events',
    
    # Visualization
    'InstitutionalVisualizer'
]
