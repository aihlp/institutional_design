"""
Dataset Loaders for Institutional Analysis

This module provides loaders for open behavioral datasets:
- Reddit (via Pushshift/public dumps)
- Wikipedia edit histories
- GitHub repository activity
- Synthetic data generation

All loaders convert raw data into the normalized schema:
{
    "event_id": "",
    "timestamp": "",
    "agent_id": "",
    "signal_type": "",
    "reaction_type": "",
    "context": "",
    "source": "",
    "target": "",
    "weight": 0,
    "metadata": {}
}
"""

import json
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Iterator
from pathlib import Path


class NormalizedEvent:
    """Factory for creating normalized events"""
    
    @staticmethod
    def create(
        timestamp: str,
        agent_id: str,
        signal_type: str,
        reaction_type: str,
        context: str,
        source: str,
        target: Optional[str] = None,
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a normalized event record"""
        event_data = {
            "timestamp": timestamp,
            "agent_id": agent_id,
            "signal_type": signal_type,
            "reaction_type": reaction_type,
            "context": context,
            "source": source,
            "target": target,
            "weight": weight,
            "metadata": metadata or {}
        }
        # Generate deterministic ID
        event_id = hashlib.md5(
            json.dumps(event_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        event_data["event_id"] = event_id
        return event_data


class RedditLoader:
    """
    Loader for Reddit interaction data.
    
    For initial experiments, uses small sample data.
    In production, would connect to Pushshift API or local archives.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path) if data_path else None
    
    def load_sample(self, subreddit: str = "science", 
                    num_interactions: int = 1000) -> List[Dict[str, Any]]:
        """
        Load or generate sample Reddit interactions.
        
        For initial experiments without actual API access.
        """
        events = []
        base_time = datetime.now() - timedelta(days=30)
        
        # Simulated user pool
        users = [f"user_{i}" for i in range(50)]
        
        # Simulated post types
        post_types = ["question", "finding", "discussion", "announcement"]
        
        # Simulated reaction patterns
        reactions = [
            ("comment", "engage"),
            ("upvote", "amplify"),
            ("downvote", "suppress"),
            ("award", "amplify"),
            ("report", "counter"),
            ("ignore", "ignore")
        ]
        
        for i in range(num_interactions):
            timestamp = base_time + timedelta(
                hours=random.randint(0, 720),
                minutes=random.randint(0, 59)
            )
            
            user = random.choice(users)
            post_type = random.choice(post_types)
            reaction_type = random.choice(reactions)
            
            event = NormalizedEvent.create(
                timestamp=timestamp.isoformat(),
                agent_id=user,
                signal_type="post" if i % 5 == 0 else "comment",
                reaction_type=reaction_type[1],
                context=f"r/{subreddit}",
                source=user,
                target=f"post_{i % 100}",
                weight=random.uniform(0.5, 1.0),
                metadata={
                    "post_type": post_type,
                    "karma_delta": random.randint(-10, 100),
                    "thread_depth": random.randint(0, 5)
                }
            )
            events.append(event)
        
        # Sort by timestamp
        events.sort(key=lambda e: e['timestamp'])
        return events
    
    def load_from_file(self, filepath: str) -> Iterator[Dict[str, Any]]:
        """Load events from JSONL file"""
        with open(filepath, 'r') as f:
            for line in f:
                raw_data = json.loads(line)
                yield self._normalize_reddit_event(raw_data)
    
    def _normalize_reddit_event(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw Reddit event to canonical schema"""
        # Determine reaction type from action
        action = raw.get('action', 'comment')
        if action == 'upvote':
            reaction = 'amplify'
        elif action == 'downvote':
            reaction = 'suppress'
        elif action == 'report':
            reaction = 'counter'
        elif action == 'delete':
            reaction = 'exit'
        else:
            reaction = 'engage'
        
        return NormalizedEvent.create(
            timestamp=raw.get('created_utc', datetime.now().isoformat()),
            agent_id=raw.get('author', 'unknown'),
            signal_type=raw.get('type', 'comment'),
            reaction_type=reaction,
            context=raw.get('subreddit', 'unknown'),
            source=raw.get('author', 'unknown'),
            target=raw.get('link_id') or raw.get('parent_id'),
            weight=raw.get('score', 1) / 100,  # Normalize score
            metadata={
                'score': raw.get('score', 0),
                'awards': raw.get('awards', []),
                'is_submitter': raw.get('is_submitter', False)
            }
        )


class WikipediaLoader:
    """
    Loader for Wikipedia edit history data.
    
    Focuses on collaborative governance patterns.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path) if data_path else None
    
    def load_sample(self, article_title: str = "Climate_change",
                    num_edits: int = 500) -> List[Dict[str, Any]]:
        """
        Load or generate sample Wikipedia edits.
        """
        events = []
        base_time = datetime.now() - timedelta(days=90)
        
        # Simulated editor pool
        editors = [f"editor_{i}" for i in range(30)]
        
        # Edit types
        edit_types = ["content", "fix", "revert", "discussion", "vandalism"]
        
        for i in range(num_edits):
            timestamp = base_time + timedelta(
                hours=random.randint(0, 2160),
                minutes=random.randint(0, 59)
            )
            
            editor = random.choice(editors)
            edit_type = random.choice(edit_types)
            
            # Determine reaction based on edit type
            if edit_type == "revert":
                reaction = "counter"
            elif edit_type == "vandalism":
                reaction = "suppress"
            elif edit_type == "discussion":
                reaction = "engage"
            else:
                reaction = "adapt"
            
            event = NormalizedEvent.create(
                timestamp=timestamp.isoformat(),
                agent_id=editor,
                signal_type="edit",
                reaction_type=reaction,
                context=f"wiki:{article_title}",
                source=editor,
                target=f"revision_{i}",
                weight=1.0,
                metadata={
                    "edit_type": edit_type,
                    "bytes_changed": random.randint(-1000, 5000),
                    "is_minor": random.choice([True, False]),
                    "is_revert": edit_type == "revert"
                }
            )
            events.append(event)
        
        events.sort(key=lambda e: e['timestamp'])
        return events
    
    def _normalize_edit_event(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw Wikipedia edit event"""
        comment = raw.get('comment', '').lower()
        
        # Detect revert
        is_revert = 'revert' in comment or 'undo' in comment
        
        # Detect vandalism fight
        is_vandalism = 'vandal' in comment or 'spam' in comment
        
        if is_revert:
            reaction = 'counter'
        elif is_vandalism:
            reaction = 'suppress'
        elif raw.get('minor', False):
            reaction = 'adapt'
        else:
            reaction = 'engage'
        
        return NormalizedEvent.create(
            timestamp=raw.get('timestamp', datetime.now().isoformat()),
            agent_id=raw.get('user', 'anonymous'),
            signal_type="edit",
            reaction_type=reaction,
            context=f"wiki:{raw.get('title', 'unknown')}",
            source=raw.get('user', 'anonymous'),
            target=f"rev:{raw.get('revid', 0)}",
            weight=1.0,
            metadata={
                'comment': raw.get('comment', ''),
                'bytes': raw.get('bytes', 0),
                'minor': raw.get('minor', False),
                'is_revert': is_revert
            }
        )


class GitHubLoader:
    """
    Loader for GitHub repository activity.
    
    Focuses on coordination and contribution norms.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path) if data_path else None
    
    def load_sample(self, repo_name: str = "institutional_design",
                    num_events: int = 300) -> List[Dict[str, Any]]:
        """
        Load or generate sample GitHub activity.
        """
        events = []
        base_time = datetime.now() - timedelta(days=60)
        
        # Simulated contributor pool
        contributors = [f"contributor_{i}" for i in range(20)]
        
        # Activity types
        activity_types = ["commit", "pr_open", "pr_review", "issue", "comment"]
        
        for i in range(num_events):
            timestamp = base_time + timedelta(
                hours=random.randint(0, 1440),
                minutes=random.randint(0, 59)
            )
            
            contributor = random.choice(contributors)
            activity = random.choice(activity_types)
            
            # Map activity to signal/reaction
            if activity == "commit":
                signal = "commit"
                reaction = "adapt"
            elif activity == "pr_open":
                signal = "pr"
                reaction = "engage"
            elif activity == "pr_review":
                signal = "review"
                reaction = random.choice(["engage", "counter", "adapt"])
            elif activity == "issue":
                signal = "issue"
                reaction = "engage"
            else:  # comment
                signal = "comment"
                reaction = random.choice(["engage", "amplify", "counter"])
            
            event = NormalizedEvent.create(
                timestamp=timestamp.isoformat(),
                agent_id=contributor,
                signal_type=signal,
                reaction_type=reaction,
                context=f"github:{repo_name}",
                source=contributor,
                target=f"{activity}_{i}",
                weight=1.0,
                metadata={
                    "activity_type": activity,
                    "additions": random.randint(0, 500) if activity == "commit" else 0,
                    "deletions": random.randint(0, 200) if activity == "commit" else 0,
                    "is_first_contribution": random.choice([True, False, False, False])
                }
            )
            events.append(event)
        
        events.sort(key=lambda e: e['timestamp'])
        return events


class SyntheticDataGenerator:
    """
    Generator for synthetic institutional simulation data.
    
    Creates controlled experimental conditions for testing
    institutional emergence, drift, and intervention effects.
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate_baseline(self, 
                          num_agents: int = 100,
                          num_steps: int = 1000) -> List[Dict[str, Any]]:
        """
        Generate baseline institutional emergence scenario.
        
        Agents interact randomly, forming natural clusters.
        """
        events = []
        base_time = datetime.now()
        
        agents = [f"agent_{i}" for i in range(num_agents)]
        
        # Predefined behavioral archetypes
        archetypes = {
            'collaborator': {'engage': 0.7, 'amplify': 0.2, 'adapt': 0.1},
            'critic': {'engage': 0.3, 'counter': 0.5, 'suppress': 0.2},
            'observer': {'ignore': 0.6, 'engage': 0.3, 'amplify': 0.1},
            'instigator': {'engage': 0.4, 'counter': 0.3, 'amplify': 0.3}
        }
        
        # Assign archetypes to agents
        agent_archetypes = {
            agent: random.choice(list(archetypes.keys()))
            for agent in agents
        }
        
        for step in range(num_steps):
            timestamp = base_time + timedelta(seconds=step * 60)
            
            # Select random agent and target
            agent = random.choice(agents)
            target = random.choice([a for a in agents if a != agent])
            
            # Get agent's archetype probabilities
            archetype = agent_archetypes[agent]
            probs = archetypes[archetype]
            
            # Sample reaction based on archetype
            reaction = random.choices(
                list(probs.keys()),
                weights=list(probs.values())
            )[0]
            
            event = NormalizedEvent.create(
                timestamp=timestamp.isoformat(),
                agent_id=agent,
                signal_type="interaction",
                reaction_type=reaction,
                context="synthetic:baseline",
                source=agent,
                target=target,
                weight=1.0,
                metadata={
                    "archetype": archetype,
                    "step": step,
                    "interaction_count": step // num_agents
                }
            )
            events.append(event)
        
        return events
    
    def generate_intervention_scenario(self,
                                       num_agents: int = 100,
                                       num_steps: int = 1000,
                                       intervention_step: int = 500,
                                       intervention_type: str = "moderation") -> List[Dict[str, Any]]:
        """
        Generate scenario with mid-stream intervention.
        
        Args:
            num_agents: Number of simulated agents
            num_steps: Total simulation steps
            intervention_step: Step at which intervention occurs
            intervention_type: Type of intervention (moderation, ranking, amplification)
        
        Returns:
            List of normalized events
        """
        events = []
        base_time = datetime.now()
        
        agents = [f"agent_{i}" for i in range(num_agents)]
        
        # Archetypes with different responses to intervention
        archetypes = {
            'collaborator': {'engage': 0.7, 'amplify': 0.2, 'adapt': 0.1},
            'critic': {'engage': 0.3, 'counter': 0.5, 'suppress': 0.2},
            'observer': {'ignore': 0.6, 'engage': 0.3, 'amplify': 0.1},
            'instigator': {'engage': 0.4, 'counter': 0.3, 'amplify': 0.3}
        }
        
        agent_archetypes = {
            agent: random.choice(list(archetypes.keys()))
            for agent in agents
        }
        
        for step in range(num_steps):
            timestamp = base_time + timedelta(seconds=step * 60)
            is_post_intervention = step >= intervention_step
            
            agent = random.choice(agents)
            target = random.choice([a for a in agents if a != agent])
            
            archetype = agent_archetypes[agent]
            probs = archetypes[archetype].copy()
            
            # Modify probabilities based on intervention
            if is_post_intervention:
                if intervention_type == "moderation":
                    # Reduce counter/suppress behaviors
                    probs['counter'] = probs.get('counter', 0) * 0.5
                    probs['suppress'] = probs.get('suppress', 0) * 0.5
                    # Increase adapt
                    probs['adapt'] = probs.get('adapt', 0) + 0.2
                elif intervention_type == "amplification":
                    # Increase amplify
                    probs['amplify'] = probs.get('amplify', 0) * 1.5
                elif intervention_type == "ranking_change":
                    # Shift toward engagement
                    probs['engage'] = probs.get('engage', 0) * 1.3
                
                # Renormalize probabilities
                total = sum(probs.values())
                probs = {k: v/total for k, v in probs.items()}
            
            reaction = random.choices(
                list(probs.keys()),
                weights=list(probs.values())
            )[0]
            
            event = NormalizedEvent.create(
                timestamp=timestamp.isoformat(),
                agent_id=agent,
                signal_type="interaction",
                reaction_type=reaction,
                context=f"synthetic:intervention:{intervention_type}",
                source=agent,
                target=target,
                weight=1.0,
                metadata={
                    "archetype": archetype,
                    "step": step,
                    "is_post_intervention": is_post_intervention,
                    "intervention_type": intervention_type if is_post_intervention else None
                }
            )
            events.append(event)
        
        return events
    
    def generate_drift_scenario(self,
                                num_agents: int = 100,
                                num_steps: int = 1500,
                                drift_type: str = "fragmentation") -> List[Dict[str, Any]]:
        """
        Generate scenario showing institutional drift over time.
        
        Args:
            drift_type: Type of drift (fragmentation, convergence, polarization)
        """
        events = []
        base_time = datetime.now()
        
        agents = [f"agent_{i}" for i in range(num_agents)]
        
        # Initial homogeneous behavior
        initial_probs = {'engage': 0.6, 'amplify': 0.2, 'adapt': 0.2}
        
        for step in range(num_steps):
            timestamp = base_time + timedelta(seconds=step * 60)
            
            # Calculate drift progress (0.0 to 1.0)
            drift_progress = step / num_steps
            
            agent = random.choice(agents)
            target = random.choice([a for a in agents if a != agent])
            
            # Evolve probabilities based on drift type
            if drift_type == "fragmentation":
                # Increase diversity of reactions
                probs = {
                    'engage': 0.6 * (1 - drift_progress) + 0.2 * drift_progress,
                    'counter': 0.4 * drift_progress,
                    'ignore': 0.3 * drift_progress,
                    'adapt': 0.2
                }
            elif drift_type == "convergence":
                # Move toward uniform behavior
                probs = {
                    'engage': 0.6 + 0.3 * drift_progress,
                    'amplify': 0.2 + 0.1 * drift_progress,
                    'adapt': 0.2
                }
            elif drift_type == "polarization":
                # Split into two camps
                camp = hash(agent) % 2
                if camp == 0:
                    probs = {'engage': 0.7, 'amplify': 0.3}
                else:
                    probs = {'counter': 0.6, 'suppress': 0.4}
            else:
                probs = initial_probs
            
            # Normalize
            total = sum(probs.values())
            probs = {k: v/total for k, v in probs.items()}
            
            reaction = random.choices(
                list(probs.keys()),
                weights=list(probs.values())
            )[0]
            
            event = NormalizedEvent.create(
                timestamp=timestamp.isoformat(),
                agent_id=agent,
                signal_type="interaction",
                reaction_type=reaction,
                context=f"synthetic:drift:{drift_type}",
                source=agent,
                target=target,
                weight=1.0,
                metadata={
                    "step": step,
                    "drift_progress": drift_progress,
                    "drift_type": drift_type
                }
            )
            events.append(event)
        
        return events


def get_loader(dataset_type: str, data_path: Optional[str] = None):
    """Factory function to get appropriate loader"""
    loaders = {
        'reddit': RedditLoader,
        'wikipedia': WikipediaLoader,
        'github': GitHubLoader,
        'synthetic': SyntheticDataGenerator
    }
    
    if dataset_type not in loaders:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
    
    return loaders[dataset_type](data_path)
