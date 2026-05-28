#!/usr/bin/env python3
"""
Institutional Analysis Experiment Pipeline

Main executable pipeline that:
1. Loads/generates dataset
2. Normalizes to canonical schema
3. Builds behavioral trajectories
4. Detects clusters and institutions
5. Computes metrics
6. Generates visualizations
7. Runs forecasting experiments
8. Produces benchmark output

Usage:
    python experiments/run_experiment.py --dataset synthetic --scenario baseline
    python experiments/run_experiment.py --dataset reddit --subreddit science
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.dataset_loaders import (
    RedditLoader, WikipediaLoader, GitHubLoader, 
    SyntheticDataGenerator, get_loader
)
from core.clustering_engine import BehavioralClusterDetector, build_trajectories_from_events
from core.metrics_engine import InstitutionalMetrics, create_benchmark_output
from core.visualization_engine import InstitutionalVisualizer
from core.institutional_primitives import InformationField


def run_experiment(dataset_type: str, 
                   scenario: str = "baseline",
                   subreddit: str = "science",
                   num_events: int = 1000,
                   output_dir: str = "experiments/output",
                   use_llm: bool = False):
    """
    Run complete institutional analysis experiment.
    
    Args:
        dataset_type: Type of dataset (synthetic, reddit, wikipedia, github)
        scenario: For synthetic - baseline, intervention, drift
        subreddit: For Reddit - which subreddit
        num_events: Number of events to process
        output_dir: Output directory for results
        use_llm: Whether to use OpenRouter LLM for interpretation
    
    Returns:
        Experiment results dictionary
    """
    
    print(f"\n{'='*60}")
    print(f"INSTITUTIONAL ANALYSIS EXPERIMENT")
    print(f"{'='*60}")
    print(f"Dataset: {dataset_type}")
    print(f"Scenario: {scenario}")
    print(f"Events: {num_events}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"{'='*60}\n")
    
    # Initialize components
    metrics_engine = InstitutionalMetrics()
    cluster_detector = BehavioralClusterDetector(eps=0.3, min_samples=3)
    visualizer = InstitutionalVisualizer(output_dir=output_dir)
    
    # Setup output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load/Generate Dataset
    print("Step 1: Loading dataset...")
    events = load_dataset(dataset_type, scenario, subreddit, num_events)
    print(f"  Loaded {len(events)} events")
    
    if not events:
        return {"error": "No events loaded"}
    
    # Step 2: Compute Information Field Metrics
    print("\nStep 2: Computing information field metrics...")
    info_field = InformationField.from_signals([], context=events[0].get('context', ''))
    metrics = metrics_engine.compute_all_metrics(events)
    print(f"  Entropy: {metrics['entropy']:.4f}")
    print(f"  Density: {metrics['density']:.6f}")
    print(f"  Concentration: {metrics['concentration']:.4f}")
    print(f"  Volatility: {metrics['volatility']:.4f}")
    print(f"  Polarization: {metrics['polarization']:.4f}")
    
    # Step 3: Build Behavioral Trajectories
    print("\nStep 3: Building behavioral trajectories...")
    context = events[0].get('context', 'unknown')
    trajectories = build_trajectories_from_events(events, context=context)
    print(f"  Built {len(trajectories)} trajectories")
    
    # Step 4: Detect Behavioral Clusters
    print("\nStep 4: Detecting behavioral clusters...")
    clusters = cluster_detector.cluster_simple(trajectories, context=context)
    print(f"  Detected {len(clusters)} clusters")
    
    # Step 5: Identify Institutions
    print("\nStep 5: Identifying institutions...")
    institutions = cluster_detector.detect_institutions(clusters, stability_threshold=0.6)
    print(f"  Identified {len(institutions)} potential institutions")
    
    for inst in institutions:
        print(f"    - {inst['name']} (strength={inst['norm_strength']:.2f}, participants={inst['participant_count']})")
    
    # Step 6: Generate Visualizations
    print("\nStep 6: Generating visualizations...")
    viz_files = []
    
    viz_files.append(visualizer.generate_cluster_graph(clusters, institutions))
    print(f"  Generated cluster graph")
    
    # Create metrics history for timeline
    metrics_history = [{
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics
    }]
    viz_files.append(visualizer.generate_entropy_timeline(metrics_history))
    print(f"  Generated entropy timeline")
    
    if trajectories:
        viz_files.append(visualizer.generate_trajectory_map(trajectories[:20], context))
        print(f"  Generated trajectory map")
    
    # Step 7: LLM Interpretation (optional)
    interpretation = {}
    if use_llm and clusters:
        print("\nStep 7: Getting LLM interpretation...")
        try:
            from core.openrouter_client import OpenRouterClient
            client = OpenRouterClient()
            
            # Interpret largest cluster
            largest_cluster = max(clusters, key=lambda c: c.get('size', 0))
            cluster_data = {
                'size': largest_cluster.get('size'),
                'stability': largest_cluster.get('stability_score'),
                'centroid': largest_cluster.get('centroid'),
                'unique_agents': largest_cluster.get('unique_agents')
            }
            
            interpretation = client.interpret_cluster(cluster_data, context=context)
            print(f"  Institution type: {interpretation.get('institution_type')}")
            print(f"  Confidence: {interpretation.get('confidence', 0):.2f}")
        except Exception as e:
            print(f"  LLM interpretation skipped: {e}")
            interpretation = {'error': str(e)}
    
    # Step 8: Forecasting (simple trend extrapolation)
    print("\nStep 8: Running forecasting experiment...")
    forecast = generate_forecast(metrics, clusters, institutions)
    print(f"  Predicted drift: {forecast.get('predicted_drift')}")
    
    # Step 9: Create Benchmark Output
    print("\nStep 9: Creating benchmark output...")
    benchmark = create_benchmark_output(
        dataset=f"{dataset_type}:{scenario}",
        metrics=metrics,
        clusters_detected=len(clusters),
        predicted_drift=forecast.get('predicted_drift', ''),
        intervention_effect=forecast.get('intervention_effect', '')
    )
    
    # Save benchmark
    benchmark_file = output_path / "benchmark_output.json"
    with open(benchmark_file, 'w') as f:
        json.dump(benchmark, f, indent=2)
    print(f"  Saved benchmark to {benchmark_file}")
    
    # Step 10: Save Complete Results
    print("\nStep 10: Saving complete results...")
    results = {
        'experiment_id': f"{dataset_type}_{scenario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'dataset': dataset_type,
        'scenario': scenario,
        'timestamp': datetime.now().isoformat(),
        'parameters': {
            'num_events': num_events,
            'subreddit': subreddit,
            'use_llm': use_llm
        },
        'metrics': metrics,
        'clusters_detected': len(clusters),
        'institutions': institutions,
        'trajectories_count': len(trajectories),
        'benchmark': benchmark,
        'interpretation': interpretation,
        'forecast': forecast,
        'visualizations': viz_files,
        'status': 'complete'
    }
    
    results_file = output_path / "experiment_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary
    summary_file = visualizer.generate_experiment_summary(results)
    
    print(f"\n{'='*60}")
    print(f"EXPERIMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {results_file}")
    print(f"Benchmark: {benchmark_file}")
    print(f"Summary: {summary_file}")
    print(f"Visualizations: {len(viz_files)} files")
    print(f"{'='*60}\n")
    
    return results


def load_dataset(dataset_type: str, scenario: str, 
                 subreddit: str, num_events: int):
    """Load or generate dataset based on type"""
    
    if dataset_type == "synthetic":
        generator = SyntheticDataGenerator(seed=42)
        
        if scenario == "baseline":
            events = generator.generate_baseline(num_agents=100, num_steps=num_events)
        elif scenario == "intervention":
            events = generator.generate_intervention_scenario(
                num_agents=100, 
                num_steps=num_events,
                intervention_step=num_events // 2,
                intervention_type="moderation"
            )
        elif scenario == "drift":
            events = generator.generate_drift_scenario(
                num_agents=100,
                num_steps=num_events,
                drift_type="fragmentation"
            )
        else:
            events = generator.generate_baseline(num_agents=100, num_steps=num_events)
    
    elif dataset_type == "reddit":
        loader = RedditLoader()
        events = loader.load_sample(subreddit=subreddit, num_interactions=num_events)
    
    elif dataset_type == "wikipedia":
        loader = WikipediaLoader()
        events = loader.load_sample(num_edits=num_events)
    
    elif dataset_type == "github":
        loader = GitHubLoader()
        events = loader.load_sample(num_events=num_events)
    
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
    
    return events


def generate_forecast(metrics: dict, clusters: list, institutions: list) -> dict:
    """Generate simple forecast based on current state"""
    
    # Simple heuristic forecasting
    volatility = metrics.get('volatility', 0)
    entropy = metrics.get('entropy', 0)
    convergence = metrics.get('convergence', 0)
    
    if volatility > 0.3:
        predicted_drift = "high_instability"
        confidence = 0.6
    elif convergence > 0.3:
        predicted_drift = "convergence_expected"
        confidence = 0.7
    elif convergence < -0.3:
        predicted_drift = "fragmentation_expected"
        confidence = 0.7
    elif entropy > 3.0:
        predicted_drift = "diversification"
        confidence = 0.5
    else:
        predicted_drift = "stable"
        confidence = 0.8
    
    # Check for intervention effects
    intervention_effect = ""
    if any('intervention' in str(c.get('context', '')) for c in clusters):
        if volatility < 0.2:
            intervention_effect = "stabilizing"
        elif metrics.get('polarization', 0) > 0.5:
            intervention_effect = "polarizing"
        else:
            intervention_effect = "mixed"
    
    return {
        'predicted_drift': predicted_drift,
        'confidence': confidence,
        'time_horizon': '7d',
        'basis': ['volatility', 'entropy', 'convergence'],
        'intervention_effect': intervention_effect
    }


def main():
    parser = argparse.ArgumentParser(description='Run Institutional Analysis Experiment')
    
    parser.add_argument('--dataset', type=str, default='synthetic',
                       choices=['synthetic', 'reddit', 'wikipedia', 'github'],
                       help='Dataset type')
    parser.add_argument('--scenario', type=str, default='baseline',
                       choices=['baseline', 'intervention', 'drift'],
                       help='Scenario (for synthetic data)')
    parser.add_argument('--subreddit', type=str, default='science',
                       help='Subreddit (for Reddit data)')
    parser.add_argument('--events', type=int, default=500,
                       help='Number of events to process')
    parser.add_argument('--output', type=str, default='experiments/output',
                       help='Output directory')
    parser.add_argument('--llm', action='store_true',
                       help='Use OpenRouter LLM for interpretation')
    
    args = parser.parse_args()
    
    results = run_experiment(
        dataset_type=args.dataset,
        scenario=args.scenario,
        subreddit=args.subreddit,
        num_events=args.events,
        output_dir=args.output,
        use_llm=args.llm
    )
    
    # Exit with appropriate code
    if 'error' in results:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
