"""
Institutional Clustering Engine

Detects behavioral clusters from trajectories using:
- Feature extraction from reaction patterns
- Similarity computation
- Cluster formation (DBSCAN-style)
- Stability scoring
"""

import numpy as np
from collections import Counter, defaultdict
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class BehavioralClusterDetector:
    """Detect and analyze behavioral clusters from trajectories"""
    
    def __init__(self, eps: float = 0.3, min_samples: int = 3):
        """
        Initialize cluster detector.
        
        Args:
            eps: Maximum distance for points to be considered neighbors
            min_samples: Minimum trajectories to form a cluster
        """
        self.eps = eps
        self.min_samples = min_samples
        self.clusters = []
    
    def extract_features(self, trajectory: Dict[str, Any]) -> np.ndarray:
        """
        Extract feature vector from a trajectory.
        
        Features:
        - Reaction type distribution
        - Average intensity
        - Average latency
        - Trajectory length
        - Temporal patterns
        """
        reactions = trajectory.get('reactions', [])
        
        if not reactions:
            return np.zeros(10)
        
        # Reaction type distribution (7 types)
        reaction_counts = Counter(r.get('reaction_type', 'unknown') for r in reactions)
        reaction_types = ['engage', 'ignore', 'amplify', 'suppress', 'counter', 'adapt', 'exit']
        reaction_dist = np.array([reaction_counts.get(rt, 0) / len(reactions) for rt in reaction_types])
        
        # Average intensity
        intensities = [r.get('intensity', 1.0) for r in reactions]
        avg_intensity = np.mean(intensities)
        
        # Average latency
        latencies = [r.get('latency', 0.0) for r in reactions]
        avg_latency = np.mean(latencies) / 100  # Normalize
        
        # Trajectory length (normalized)
        traj_length = min(len(reactions) / 50, 1.0)
        
        # Combine features
        features = np.concatenate([
            reaction_dist,
            [avg_intensity, avg_latency, traj_length]
        ])
        
        return features
    
    def compute_similarity(self, traj1: Dict[str, Any], 
                           traj2: Dict[str, Any]) -> float:
        """
        Compute similarity between two trajectories.
        
        Uses cosine similarity on feature vectors.
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        feat1 = self.extract_features(traj1)
        feat2 = self.extract_features(traj2)
        
        # Cosine similarity
        dot_product = np.dot(feat1, feat2)
        norm1 = np.linalg.norm(feat1)
        norm2 = np.linalg.norm(feat2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return max(0.0, min(1.0, similarity))
    
    def compute_distance_matrix(self, trajectories: List[Dict[str, Any]]) -> np.ndarray:
        """
        Compute pairwise distance matrix.
        
        Distance = 1 - similarity
        """
        n = len(trajectories)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.compute_similarity(trajectories[i], trajectories[j])
                dist = 1 - sim
                distances[i, j] = dist
                distances[j, i] = dist
        
        return distances
    
    def cluster_simple(self, trajectories: List[Dict[str, Any]],
                       context: str = "") -> List[Dict[str, Any]]:
        """
        Simple density-based clustering.
        
        Args:
            trajectories: List of trajectory dictionaries
            context: Context identifier
        
        Returns:
            List of cluster dictionaries
        """
        if len(trajectories) < self.min_samples:
            return []
        
        n = len(trajectories)
        distances = self.compute_distance_matrix(trajectories)
        
        # Find neighbors for each point
        neighbors = []
        for i in range(n):
            neighbor_ids = [j for j in range(n) if distances[i, j] <= self.eps]
            neighbors.append(neighbor_ids)
        
        # Cluster assignment
        cluster_assignments = [-1] * n  # -1 = unassigned/noise
        cluster_id = 0
        
        for i in range(n):
            if cluster_assignments[i] != -1:
                continue  # Already assigned
            
            if len(neighbors[i]) < self.min_samples:
                continue  # Noise point
            
            # Start new cluster
            cluster_assignments[i] = cluster_id
            
            # Expand cluster
            seed_set = list(neighbors[i])
            j = 0
            while j < len(seed_set):
                q = seed_set[j]
                
                if cluster_assignments[q] == -1:
                    cluster_assignments[q] = cluster_id
                    
                    if len(neighbors[q]) >= self.min_samples:
                        # Add neighbors to seed set
                        for neighbor in neighbors[q]:
                            if neighbor not in seed_set:
                                seed_set.append(neighbor)
                
                j += 1
            
            cluster_id += 1
        
        # Build cluster objects
        clusters = []
        for cid in range(cluster_id):
            member_indices = [i for i in range(n) if cluster_assignments[i] == cid]
            member_trajectories = [trajectories[i] for i in member_indices]
            
            if len(member_trajectories) < self.min_samples:
                continue
            
            # Compute cluster centroid
            centroid = self._compute_centroid(member_trajectories)
            
            # Compute stability score
            stability = self._compute_stability(member_trajectories)
            
            cluster = {
                'cluster_id': f"cluster_{cid}",
                'trajectories': member_trajectories,
                'centroid': centroid,
                'created_at': datetime.now().isoformat(),
                'context': context,
                'stability_score': stability,
                'size': len(member_trajectories),
                'unique_agents': len(set(t.get('agent_id') for t in member_trajectories)),
                'metadata': {
                    'member_indices': member_indices,
                    'avg_trajectory_length': np.mean([len(t.get('reactions', [])) for t in member_trajectories])
                }
            }
            clusters.append(cluster)
        
        self.clusters = clusters
        return clusters
    
    def _compute_centroid(self, trajectories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute representative centroid for cluster"""
        if not trajectories:
            return {}
        
        # Aggregate reaction types
        all_reactions = []
        for t in trajectories:
            all_reactions.extend(t.get('reactions', []))
        
        reaction_counts = Counter(r.get('reaction_type', 'unknown') for r in all_reactions)
        total = len(all_reactions)
        
        # Dominant reaction
        dominant = reaction_counts.most_common(1)[0][0] if reaction_counts else 'unknown'
        
        # Feature averages
        intensities = [r.get('intensity', 1.0) for r in all_reactions]
        latencies = [r.get('latency', 0.0) for r in all_reactions]
        
        return {
            'dominant_reaction': dominant,
            'reaction_distribution': dict(reaction_counts),
            'avg_intensity': np.mean(intensities) if intensities else 0.0,
            'avg_latency': np.mean(latencies) if latencies else 0.0,
            'total_reactions': total
        }
    
    def _compute_stability(self, trajectories: List[Dict[str, Any]]) -> float:
        """
        Compute cluster stability score.
        
        Based on:
        - Internal cohesion (similarity within cluster)
        - Temporal consistency
        - Agent diversity
        """
        if len(trajectories) < 2:
            return 0.5
        
        # Internal cohesion
        similarities = []
        for i in range(min(len(trajectories), 10)):
            for j in range(i + 1, min(len(trajectories), 10)):
                sim = self.compute_similarity(trajectories[i], trajectories[j])
                similarities.append(sim)
        
        cohesion = np.mean(similarities) if similarities else 0.0
        
        # Agent diversity (some diversity is good for stability)
        unique_agents = len(set(t.get('agent_id') for t in trajectories))
        agent_diversity = min(unique_agents / len(trajectories), 1.0)
        
        # Combined stability
        stability = 0.6 * cohesion + 0.4 * agent_diversity
        
        return max(0.0, min(1.0, stability))
    
    def detect_institutions(self, clusters: List[Dict[str, Any]],
                            stability_threshold: float = 0.6) -> List[Dict[str, Any]]:
        """
        Identify potential institutions from stable clusters.
        
        Args:
            clusters: List of detected clusters
            stability_threshold: Minimum stability for institution status
        
        Returns:
            List of institution candidates
        """
        institutions = []
        
        for cluster in clusters:
            if cluster.get('stability_score', 0) >= stability_threshold:
                institution = {
                    'institution_id': f"inst_{cluster['cluster_id']}",
                    'name': f"Institution_{cluster['cluster_id']}",
                    'cluster_id': cluster['cluster_id'],
                    'emergence_time': cluster.get('created_at'),
                    'context': cluster.get('context'),
                    'norm_strength': cluster.get('stability_score', 0),
                    'participant_count': cluster.get('unique_agents', 0),
                    'is_stable': True,
                    'metadata': {
                        'cluster_size': cluster.get('size'),
                        'centroid': cluster.get('centroid')
                    }
                }
                institutions.append(institution)
        
        return institutions


def build_trajectories_from_events(events: List[Dict[str, Any]],
                                   context: str = "") -> List[Dict[str, Any]]:
    """
    Build behavioral trajectories from event stream.
    
    Groups events by agent and creates trajectory objects.
    """
    from core.institutional_primitives import Reaction, ReactionType, BehavioralTrajectory
    
    # Group by agent
    agent_events = defaultdict(list)
    for event in events:
        agent = event.get('agent_id', 'unknown')
        agent_events[agent].append(event)
    
    trajectories = []
    for agent_id, agent_event_list in agent_events.items():
        if len(agent_event_list) < 2:
            continue
        
        # Sort by timestamp
        agent_event_list.sort(key=lambda e: e.get('timestamp', ''))
        
        # Convert to Reaction objects
        reactions = []
        for event in agent_event_list:
            try:
                reaction = Reaction(
                    reaction_id=event.get('event_id', ''),
                    signal_id='',
                    agent_id=agent_id,
                    timestamp=datetime.fromisoformat(event.get('timestamp', datetime.now().isoformat())),
                    reaction_type=ReactionType(event.get('reaction_type', 'custom')),
                    intensity=event.get('weight', 1.0),
                    latency=0.0,
                    metadata=event.get('metadata', {})
                )
                reactions.append(reaction)
            except:
                pass
        
        if not reactions:
            continue
        
        # Create trajectory
        try:
            trajectory = BehavioralTrajectory.from_reactions(
                agent_id=agent_id,
                reactions=reactions,
                context=context or event.get('context', '')
            )
            trajectories.append(trajectory.to_dict())
        except:
            pass
    
    return trajectories
