"""
Visualization Engine for Institutional Analysis

Generates visualizations:
- Institutional cluster graphs
- Entropy timelines
- Behavioral trajectory maps
- Intervention comparison dashboards
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path


class InstitutionalVisualizer:
    """Generate institutional visualizations"""
    
    def __init__(self, output_dir: str = "visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_cluster_graph(self, clusters: List[Dict[str, Any]],
                               institutions: Optional[List[Dict[str, Any]]] = None,
                               filename: str = "cluster_graph.json") -> str:
        """
        Generate institutional cluster graph.
        
        Creates a JSON representation suitable for network visualization.
        Nodes: agents, clusters, institutions
        Edges: transitions, interactions
        """
        graph = {
            'nodes': [],
            'links': [],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'cluster_count': len(clusters),
                'institution_count': len(institutions) if institutions else 0
            }
        }
        
        # Add cluster nodes
        for i, cluster in enumerate(clusters):
            node = {
                'id': f"cluster_{i}",
                'type': 'cluster',
                'size': cluster.get('size', 0),
                'stability': cluster.get('stability_score', 0),
                'unique_agents': cluster.get('unique_agents', 0),
                'label': f"Cluster {i}\n(n={cluster.get('size', 0)})"
            }
            graph['nodes'].append(node)
        
        # Add institution nodes
        if institutions:
            for inst in institutions:
                node = {
                    'id': inst.get('institution_id'),
                    'type': 'institution',
                    'name': inst.get('name'),
                    'norm_strength': inst.get('norm_strength', 0),
                    'participants': inst.get('participant_count', 0),
                    'label': f"★ {inst.get('name')}\n(strength={inst.get('norm_strength', 0):.2f})"
                }
                graph['nodes'].append(node)
                
                # Link to underlying cluster
                cluster_id = inst.get('cluster_id')
                if cluster_id:
                    graph['links'].append({
                        'source': inst.get('institution_id'),
                        'target': cluster_id,
                        'type': 'emerges_from',
                        'value': inst.get('norm_strength', 0)
                    })
        
        # Add agent-cluster links
        for i, cluster in enumerate(clusters):
            trajectories = cluster.get('trajectories', [])
            agents = set(t.get('agent_id') for t in trajectories)
            
            for agent in list(agents)[:10]:  # Limit for readability
                graph['links'].append({
                    'source': agent,
                    'target': f"cluster_{i}",
                    'type': 'member_of',
                    'value': 1
                })
        
        # Save graph
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(graph, f, indent=2)
        
        return str(filepath)
    
    def generate_entropy_timeline(self, metrics_history: List[Dict[str, Any]],
                                   filename: str = "entropy_timeline.json") -> str:
        """
        Generate entropy timeline data.
        
        Shows information field instability over time.
        """
        timeline = {
            'metric': 'entropy',
            'data_points': [],
            'metadata': {
                'generated_at': datetime.now().isoformat()
            }
        }
        
        for entry in metrics_history:
            point = {
                'timestamp': entry.get('timestamp'),
                'entropy': entry.get('metrics', {}).get('entropy', 0),
                'density': entry.get('metrics', {}).get('density', 0),
                'volatility': entry.get('metrics', {}).get('volatility', 0)
            }
            timeline['data_points'].append(point)
        
        # Compute trend
        if len(timeline['data_points']) > 1:
            entropies = [p['entropy'] for p in timeline['data_points']]
            timeline['trend'] = 'increasing' if entropies[-1] > entropies[0] else 'decreasing'
            timeline['min_entropy'] = min(entropies)
            timeline['max_entropy'] = max(entropies)
            timeline['avg_entropy'] = sum(entropies) / len(entropies)
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(timeline, f, indent=2)
        
        return str(filepath)
    
    def generate_trajectory_map(self, trajectories: List[Dict[str, Any]],
                                 context: str = "",
                                 filename: str = "trajectory_map.json") -> str:
        """
        Generate behavioral trajectory map.
        
        Shows movement between reaction states over time.
        """
        traj_map = {
            'context': context,
            'trajectories': [],
            'state_transitions': {},
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'trajectory_count': len(trajectories)
            }
        }
        
        # Process trajectories
        for i, traj in enumerate(trajectories[:50]):  # Limit for readability
            reactions = traj.get('reactions', [])
            
            # Extract reaction sequence
            sequence = [r.get('reaction_type', 'unknown') for r in reactions]
            
            simplified = {
                'trajectory_id': traj.get('trajectory_id', f'traj_{i}'),
                'agent_id': traj.get('agent_id'),
                'length': len(sequence),
                'dominant_reaction': max(set(sequence), key=sequence.count) if sequence else 'none',
                'sequence_sample': sequence[:10],  # First 10 reactions
                'start_time': traj.get('start_time'),
                'end_time': traj.get('end_time')
            }
            traj_map['trajectories'].append(simplified)
            
            # Count transitions
            for j in range(len(sequence) - 1):
                src, dst = sequence[j], sequence[j + 1]
                key = f"{src}->{dst}"
                traj_map['state_transitions'][key] = traj_map['state_transitions'].get(key, 0) + 1
        
        # Sort transitions by frequency
        sorted_transitions = sorted(
            traj_map['state_transitions'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        traj_map['top_transitions'] = sorted_transitions[:10]
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(traj_map, f, indent=2)
        
        return str(filepath)
    
    def generate_intervention_dashboard(self, 
                                         baseline_metrics: Dict[str, float],
                                         intervention_metrics: Dict[str, float],
                                         intervention_type: str = "",
                                         filename: str = "intervention_comparison.json") -> str:
        """
        Generate intervention comparison dashboard.
        
        Compares baseline vs intervention state.
        """
        dashboard = {
            'intervention_type': intervention_type,
            'comparison': {},
            'changes': {},
            'summary': {},
            'metadata': {
                'generated_at': datetime.now().isoformat()
            }
        }
        
        # Compare each metric
        metrics_to_compare = ['entropy', 'density', 'concentration', 'volatility', 
                              'polarization', 'convergence']
        
        for metric in metrics_to_compare:
            baseline_val = baseline_metrics.get(metric, 0)
            intervention_val = intervention_metrics.get(metric, 0)
            
            change = intervention_val - baseline_val
            pct_change = (change / baseline_val * 100) if baseline_val > 0 else 0
            
            dashboard['comparison'][metric] = {
                'baseline': baseline_val,
                'intervention': intervention_val,
                'absolute_change': change,
                'percent_change': pct_change
            }
            
            # Categorize change
            if abs(pct_change) < 5:
                impact = 'minimal'
            elif abs(pct_change) < 20:
                impact = 'moderate'
            else:
                impact = 'significant'
            
            direction = 'increase' if change > 0 else 'decrease' if change < 0 else 'no_change'
            
            dashboard['changes'][metric] = {
                'direction': direction,
                'impact': impact,
                'magnitude': abs(pct_change)
            }
        
        # Generate summary
        significant_changes = [
            m for m, c in dashboard['changes'].items() 
            if c['impact'] == 'significant'
        ]
        
        dashboard['summary'] = {
            'significant_changes': significant_changes,
            'total_metrics_changed': len(significant_changes),
            'overall_impact': 'high' if len(significant_changes) >= 3 else 
                             'medium' if len(significant_changes) >= 1 else 'low'
        }
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        return str(filepath)
    
    def generate_experiment_summary(self, experiment_results: Dict[str, Any],
                                     filename: str = "experiment_summary.json") -> str:
        """
        Generate complete experiment summary.
        
        Combines all visualizations and metrics into single report.
        """
        summary = {
            'experiment_id': experiment_results.get('experiment_id', 'unknown'),
            'dataset': experiment_results.get('dataset', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            
            'metrics': experiment_results.get('metrics', {}),
            'clusters_detected': experiment_results.get('clusters_detected', 0),
            'institutions_identified': experiment_results.get('institutions', []),
            
            'benchmark_output': experiment_results.get('benchmark', {}),
            'llm_interpretation': experiment_results.get('interpretation', {}),
            
            'visualizations_generated': experiment_results.get('visualizations', []),
            
            'status': experiment_results.get('status', 'complete')
        }
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return str(filepath)


def create_sample_visualization_data():
    """Create sample data for testing visualizations"""
    
    # Sample clusters
    clusters = [
        {
            'cluster_id': 'cluster_0',
            'size': 15,
            'stability_score': 0.75,
            'unique_agents': 12,
            'trajectories': [
                {'agent_id': f'agent_{i}', 'reactions': []}
                for i in range(12)
            ]
        },
        {
            'cluster_id': 'cluster_1',
            'size': 8,
            'stability_score': 0.62,
            'unique_agents': 7,
            'trajectories': [
                {'agent_id': f'user_{i}', 'reactions': []}
                for i in range(7)
            ]
        }
    ]
    
    # Sample institutions
    institutions = [
        {
            'institution_id': 'inst_cluster_0',
            'name': 'Collaborative_Norm',
            'cluster_id': 'cluster_0',
            'norm_strength': 0.75,
            'participant_count': 12
        }
    ]
    
    # Sample metrics history
    metrics_history = [
        {
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'entropy': 2.5 + i * 0.1,
                'density': 0.5,
                'volatility': 0.3
            }
        }
        for i in range(10)
    ]
    
    return clusters, institutions, metrics_history


if __name__ == "__main__":
    # Test visualization generation
    visualizer = InstitutionalVisualizer()
    
    clusters, institutions, metrics_history = create_sample_visualization_data()
    
    # Generate all visualizations
    files = []
    files.append(visualizer.generate_cluster_graph(clusters, institutions))
    files.append(visualizer.generate_entropy_timeline(metrics_history))
    files.append(visualizer.generate_trajectory_map(clusters[0]['trajectories']))
    files.append(visualizer.generate_intervention_dashboard(
        {'entropy': 2.5, 'volatility': 0.3},
        {'entropy': 2.8, 'volatility': 0.4},
        'moderation'
    ))
    
    print(f"Generated {len(files)} visualization files:")
    for f in files:
        print(f"  - {f}")
