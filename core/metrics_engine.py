"""
Institutional Metrics Engine

Computes measurable parameters for institutional analysis:
- Entropy (fragmentation, concentration, diversity)
- Density (signal frequency, interaction intensity)
- Volatility (cluster instability, transition frequency)
- Persistence (institutional stability over time)
- Polarization
- Convergence
"""

import numpy as np
from collections import Counter, defaultdict
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta


class InstitutionalMetrics:
    """Compute institutional metrics from behavioral data"""
    
    def __init__(self):
        self.metrics_history = []
    
    def compute_entropy(self, events: List[Dict[str, Any]], 
                        group_by: str = "agent_id") -> float:
        """
        Compute entropy of the information field.
        
        Measures fragmentation and diversity of sources.
        Higher entropy = more diverse/fragmented field.
        
        Args:
            events: List of normalized events
            group_by: Field to group by (agent_id, signal_type, reaction_type, context)
        
        Returns:
            Shannon entropy value
        """
        if not events:
            return 0.0
        
        # Count occurrences by grouping field
        counts = Counter(event.get(group_by, 'unknown') for event in events)
        total = len(events)
        
        # Compute Shannon entropy
        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def compute_density(self, events: List[Dict[str, Any]]) -> float:
        """
        Compute signal density (events per unit time).
        
        Measures activity intensity in the information field.
        
        Returns:
            Events per second
        """
        if len(events) < 2:
            return 0.0
        
        # Parse timestamps
        timestamps = []
        for event in events:
            ts = event.get('timestamp')
            if isinstance(ts, str):
                try:
                    timestamps.append(datetime.fromisoformat(ts))
                except:
                    pass
            elif isinstance(ts, datetime):
                timestamps.append(ts)
        
        if len(timestamps) < 2:
            return float(len(events))
        
        timestamps.sort()
        duration = (timestamps[-1] - timestamps[0]).total_seconds()
        
        if duration <= 0:
            return float(len(events))
        
        return len(events) / duration
    
    def compute_concentration(self, events: List[Dict[str, Any]],
                              group_by: str = "agent_id",
                              top_n: int = 5) -> float:
        """
        Compute concentration ratio (share of top N sources).
        
        Measures how concentrated activity is among few sources.
        Higher = more centralized/concentrated.
        
        Returns:
            Share of events from top N sources (0.0 to 1.0)
        """
        if not events:
            return 0.0
        
        counts = Counter(event.get(group_by, 'unknown') for event in events)
        total = len(events)
        
        if total == 0:
            return 0.0
        
        # Get top N
        top_counts = [count for _, count in counts.most_common(top_n)]
        
        return sum(top_counts) / total
    
    def compute_volatility(self, events: List[Dict[str, Any]],
                           window_size: int = 50) -> float:
        """
        Compute behavioral volatility.
        
        Measures how frequently behavior patterns change.
        Higher = more unstable/volatile.
        
        Args:
            events: Chronologically sorted events
            window_size: Number of events per window
        
        Returns:
            Volatility score (standard deviation of reaction distribution changes)
        """
        if len(events) < window_size * 2:
            return 0.0
        
        # Split into windows
        windows = []
        for i in range(0, len(events) - window_size, window_size // 2):
            window = events[i:i + window_size]
            reaction_dist = Counter(e.get('reaction_type', 'unknown') for e in window)
            windows.append(reaction_dist)
        
        if len(windows) < 2:
            return 0.0
        
        # Compute changes between consecutive windows
        changes = []
        for i in range(1, len(windows)):
            prev_dist = windows[i - 1]
            curr_dist = windows[i]
            
            # Compute total variation distance
            all_types = set(prev_dist.keys()) | set(curr_dist.keys())
            total_prev = sum(prev_dist.values())
            total_curr = sum(curr_dist.values())
            
            tv_distance = 0.0
            for rtype in all_types:
                p_prev = prev_dist.get(rtype, 0) / max(total_prev, 1)
                p_curr = curr_dist.get(rtype, 0) / max(total_curr, 1)
                tv_distance += abs(p_prev - p_curr)
            
            changes.append(tv_distance / 2)  # Normalize to [0, 1]
        
        return np.std(changes) if changes else 0.0
    
    def compute_polarization(self, events: List[Dict[str, Any]],
                             agent_field: str = "agent_id",
                             reaction_field: str = "reaction_type") -> float:
        """
        Compute polarization score.
        
        Measures tendency toward extreme/opposing behaviors.
        Higher = more polarized.
        
        Identifies opposing reaction pairs (e.g., amplify vs suppress).
        """
        if not events:
            return 0.0
        
        # Define opposing reaction pairs
        opposition_map = {
            'amplify': 'suppress',
            'engage': 'ignore',
            'adapt': 'counter'
        }
        
        # Count reactions per agent
        agent_reactions = defaultdict(Counter)
        for event in events:
            agent = event.get(agent_field, 'unknown')
            reaction = event.get(reaction_field, 'unknown')
            agent_reactions[agent][reaction] += 1
        
        # Compute polarization per agent
        polarizations = []
        for agent, reactions in agent_reactions.items():
            total = sum(reactions.values())
            if total < 3:  # Need minimum observations
                continue
            
            # Check for opposing behaviors
            opp_score = 0.0
            for r1, r2 in opposition_map.items():
                count1 = reactions.get(r1, 0)
                count2 = reactions.get(r2, 0)
                
                # Both behaviors present = polarization
                if count1 > 0 and count2 > 0:
                    # More balanced = more polarized
                    balance = 1 - abs(count1 - count2) / (count1 + count2)
                    opp_score += balance
            
            if opp_score > 0:
                polarizations.append(opp_score / len(opposition_map))
        
        return np.mean(polarizations) if polarizations else 0.0
    
    def compute_cluster_stability(self, clusters: List[Dict[str, Any]],
                                  time_windows: int = 5) -> Dict[str, float]:
        """
        Compute stability metrics for behavioral clusters.
        
        Args:
            clusters: List of cluster snapshots over time
            time_windows: Number of time periods to consider
        
        Returns:
            Dictionary with stability metrics
        """
        if len(clusters) < 2:
            return {'stability_score': 0.0, 'persistence': 0.0, 'turnover': 0.0}
        
        # Track cluster membership over time
        cluster_ids = [c.get('cluster_id') for c in clusters]
        cluster_sizes = [c.get('size', 0) for c in clusters]
        
        # Size stability (coefficient of variation)
        mean_size = np.mean(cluster_sizes)
        std_size = np.std(cluster_sizes)
        size_cv = std_size / mean_size if mean_size > 0 else 0.0
        size_stability = 1 / (1 + size_cv)  # Convert to stability score
        
        # Membership persistence (Jaccard similarity across windows)
        # Simplified: just check cluster ID consistency
        unique_ids = len(set(cluster_ids))
        persistence = 1 / unique_ids if unique_ids > 0 else 0.0
        
        # Turnover rate
        if len(clusters) > 1:
            size_changes = [abs(cluster_sizes[i] - cluster_sizes[i-1]) 
                           for i in range(1, len(cluster_sizes))]
            turnover = np.mean(size_changes) / max(mean_size, 1)
        else:
            turnover = 0.0
        
        return {
            'stability_score': size_stability,
            'persistence': persistence,
            'turnover': min(turnover, 1.0)
        }
    
    def compute_transition_matrix(self, trajectories: List[Dict[str, Any]]) -> np.ndarray:
        """
        Compute state transition matrix from trajectories.
        
        Shows probability of transitioning between reaction types.
        
        Args:
            trajectories: List of trajectory dictionaries with reaction sequences
        
        Returns:
            Transition probability matrix
        """
        # Collect all transitions
        reaction_types = set()
        transitions = defaultdict(lambda: defaultdict(int))
        
        for traj in trajectories:
            reactions = traj.get('reactions', [])
            if not reactions:
                continue
            
            for i in range(len(reactions) - 1):
                r1 = reactions[i].get('reaction_type', 'unknown')
                r2 = reactions[i + 1].get('reaction_type', 'unknown')
                reaction_types.add(r1)
                reaction_types.add(r2)
                transitions[r1][r2] += 1
        
        # Build matrix
        reaction_list = sorted(reaction_types)
        n = len(reaction_list)
        matrix = np.zeros((n, n))
        
        for i, r1 in enumerate(reaction_list):
            total = sum(transitions[r1].values())
            if total > 0:
                for j, r2 in enumerate(reaction_list):
                    matrix[i, j] = transitions[r1][r2] / total
        
        return matrix
    
    def compute_convergence(self, events: List[Dict[str, Any]],
                            window_size: int = 100) -> float:
        """
        Compute convergence score over time.
        
        Measures whether behavior is becoming more uniform.
        Positive = converging, Negative = diverging.
        
        Returns:
            Convergence trend (-1.0 to 1.0)
        """
        if len(events) < window_size * 2:
            return 0.0
        
        # Compute entropy in each window
        entropies = []
        for i in range(0, len(events) - window_size, window_size // 2):
            window = events[i:i + window_size]
            entropy = self.compute_entropy(window, group_by='reaction_type')
            entropies.append(entropy)
        
        if len(entropies) < 2:
            return 0.0
        
        # Fit linear trend
        x = np.arange(len(entropies))
        slope = np.polyfit(x, entropies, 1)[0]
        
        # Normalize to [-1, 1]
        # Negative slope = decreasing entropy = convergence
        max_slope = max(abs(slope), 0.001)
        convergence = -slope / max_slope
        
        return max(-1.0, min(1.0, convergence))
    
    def compute_all_metrics(self, events: List[Dict[str, Any]],
                            clusters: Optional[List[Dict[str, Any]]] = None) -> Dict[str, float]:
        """
        Compute complete metrics suite.
        
        Args:
            events: List of normalized events
            clusters: Optional cluster snapshots
        
        Returns:
            Dictionary of all computed metrics
        """
        metrics = {
            'entropy': self.compute_entropy(events),
            'density': self.compute_density(events),
            'concentration': self.compute_concentration(events),
            'volatility': self.compute_volatility(events),
            'polarization': self.compute_polarization(events),
            'convergence': self.compute_convergence(events),
            'unique_agents': len(set(e.get('agent_id') for e in events)),
            'unique_contexts': len(set(e.get('context') for e in events)),
            'event_count': len(events)
        }
        
        # Add cluster metrics if provided
        if clusters:
            cluster_metrics = self.compute_cluster_stability(clusters)
            metrics.update({
                f'cluster_{k}': v for k, v in cluster_metrics.items()
            })
        
        # Store history
        self.metrics_history.append({
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        })
        
        return metrics


def create_benchmark_output(dataset: str, metrics: Dict[str, Any],
                            clusters_detected: int,
                            predicted_drift: str = "",
                            intervention_effect: str = "") -> Dict[str, Any]:
    """
    Create standardized benchmark output.
    
    Matches required format:
    {
        "dataset": "",
        "clusters_detected": 0,
        "entropy_score": 0,
        "volatility_score": 0,
        "stability_score": 0,
        "predicted_drift": "",
        "intervention_effect": ""
    }
    """
    return {
        "dataset": dataset,
        "clusters_detected": clusters_detected,
        "entropy_score": metrics.get('entropy', 0.0),
        "volatility_score": metrics.get('volatility', 0.0),
        "stability_score": metrics.get('cluster_stability_score', 0.0),
        "polarization_score": metrics.get('polarization', 0.0),
        "convergence_score": metrics.get('convergence', 0.0),
        "predicted_drift": predicted_drift,
        "intervention_effect": intervention_effect,
        "full_metrics": metrics
    }
