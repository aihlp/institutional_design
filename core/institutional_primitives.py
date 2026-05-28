"""
Core Institutional Primitives

This module defines the fundamental building blocks for institutional analysis:
- Signal: Informational stimuli in the system
- Reaction: Agent responses to signals
- BehavioralTrajectory: Temporal sequence of reactions
- BehavioralCluster: Grouped similar trajectories
- Institution: Stable behavioral cluster with normative force
- InformationField: Contextual environment for signals
- Intervention: External modification to the system
- Forecast: Predicted future state
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import hashlib
import json


class SignalType(Enum):
    """Types of informational signals"""
    POST = "post"
    COMMENT = "comment"
    EDIT = "edit"
    VOTE = "vote"
    MODERATION = "moderation"
    RULE_CHANGE = "rule_change"
    SYSTEM_MESSAGE = "system_message"
    CUSTOM = "custom"


class ReactionType(Enum):
    """Types of agent reactions"""
    ENGAGE = "engage"
    IGNORE = "ignore"
    AMPLIFY = "amplify"
    SUPPRESS = "suppress"
    COUNTER = "counter"
    ADAPT = "adapt"
    EXIT = "exit"
    CUSTOM = "custom"


@dataclass
class Signal:
    """
    Fundamental unit of information in the institutional system.
    
    A signal is any informational stimulus that can potentially trigger
    a reaction from an agent.
    """
    signal_id: str
    timestamp: datetime
    source: str  # Agent or system ID
    target: Optional[str]  # Target agent/content ID
    signal_type: SignalType
    content: str
    context: str  # Subreddit, article, repo, etc.
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Signal':
        """Create Signal from dictionary"""
        return cls(
            signal_id=data.get('signal_id', cls._generate_id(data)),
            timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp'],
            source=data['source'],
            target=data.get('target'),
            signal_type=SignalType(data.get('signal_type', 'custom')),
            content=data.get('content', ''),
            context=data.get('context', ''),
            weight=data.get('weight', 1.0),
            metadata=data.get('metadata', {})
        )
    
    @staticmethod
    def _generate_id(data: Dict[str, Any]) -> str:
        """Generate unique ID from signal data"""
        content = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'signal_id': self.signal_id,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'target': self.target,
            'signal_type': self.signal_type.value,
            'content': self.content,
            'context': self.context,
            'weight': self.weight,
            'metadata': self.metadata
        }


@dataclass
class Reaction:
    """
    Agent response to a signal.
    
    Reactions are the observable behaviors that result from
    processing signals through individual filters.
    """
    reaction_id: str
    signal_id: str
    agent_id: str
    timestamp: datetime
    reaction_type: ReactionType
    intensity: float  # 0.0 to 1.0
    latency: float  # Time from signal to reaction (seconds)
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reaction':
        """Create Reaction from dictionary"""
        return cls(
            reaction_id=data.get('reaction_id', cls._generate_id(data)),
            signal_id=data['signal_id'],
            agent_id=data['agent_id'],
            timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp'],
            reaction_type=ReactionType(data.get('reaction_type', 'custom')),
            intensity=data.get('intensity', 1.0),
            latency=data.get('latency', 0.0),
            content=data.get('content'),
            metadata=data.get('metadata', {})
        )
    
    @staticmethod
    def _generate_id(data: Dict[str, Any]) -> str:
        """Generate unique ID from reaction data"""
        content = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'reaction_id': self.reaction_id,
            'signal_id': self.signal_id,
            'agent_id': self.agent_id,
            'timestamp': self.timestamp.isoformat(),
            'reaction_type': self.reaction_type.value,
            'intensity': self.intensity,
            'latency': self.latency,
            'content': self.content,
            'metadata': self.metadata
        }


@dataclass
class BehavioralTrajectory:
    """
    Temporal sequence of reactions by a single agent.
    
    Trajectories capture the evolution of individual behavior
    over time, revealing patterns and tendencies.
    """
    trajectory_id: str
    agent_id: str
    reactions: List[Reaction]
    start_time: datetime
    end_time: datetime
    context: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def reaction_count(self) -> int:
        return len(self.reactions)
    
    @property
    def duration_seconds(self) -> float:
        return (self.end_time - self.start_time).total_seconds()
    
    @property
    def dominant_reaction_type(self) -> Optional[ReactionType]:
        if not self.reactions:
            return None
        from collections import Counter
        types = [r.reaction_type for r in self.reactions]
        return Counter(types).most_common(1)[0][0]
    
    @classmethod
    def from_reactions(cls, agent_id: str, reactions: List[Reaction], context: str) -> 'BehavioralTrajectory':
        """Create trajectory from list of reactions"""
        if not reactions:
            raise ValueError("Cannot create trajectory from empty reactions")
        
        sorted_reactions = sorted(reactions, key=lambda r: r.timestamp)
        return cls(
            trajectory_id=cls._generate_id(agent_id, sorted_reactions),
            agent_id=agent_id,
            reactions=sorted_reactions,
            start_time=sorted_reactions[0].timestamp,
            end_time=sorted_reactions[-1].timestamp,
            context=context
        )
    
    @staticmethod
    def _generate_id(agent_id: str, reactions: List[Reaction]) -> str:
        """Generate unique ID for trajectory"""
        content = f"{agent_id}:{len(reactions)}:{reactions[0].timestamp if reactions else ''}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'trajectory_id': self.trajectory_id,
            'agent_id': self.agent_id,
            'reactions': [r.to_dict() for r in self.reactions],
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'context': self.context,
            'reaction_count': self.reaction_count,
            'duration_seconds': self.duration_seconds,
            'dominant_reaction_type': self.dominant_reaction_type.value if self.dominant_reaction_type else None,
            'metadata': self.metadata
        }


@dataclass
class BehavioralCluster:
    """
    Group of similar behavioral trajectories.
    
    Clusters represent emergent patterns of behavior that may
    indicate proto-institutions or established institutions.
    """
    cluster_id: str
    trajectories: List[BehavioralTrajectory]
    centroid: Dict[str, Any]  # Representative characteristics
    created_at: datetime
    context: str
    stability_score: float = 0.0  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def size(self) -> int:
        return len(self.trajectories)
    
    @property
    def unique_agents(self) -> int:
        return len(set(t.agent_id for t in self.trajectories))
    
    @property
    def avg_trajectory_length(self) -> float:
        if not self.trajectories:
            return 0.0
        return sum(t.reaction_count for t in self.trajectories) / len(self.trajectories)
    
    @classmethod
    def from_trajectories(cls, trajectories: List[BehavioralTrajectory], 
                          centroid: Dict[str, Any], context: str) -> 'BehavioralCluster':
        """Create cluster from list of trajectories"""
        return cls(
            cluster_id=cls._generate_id(trajectories),
            trajectories=trajectories,
            centroid=centroid,
            created_at=datetime.now(),
            context=context
        )
    
    @staticmethod
    def _generate_id(trajectories: List[BehavioralTrajectory]) -> str:
        """Generate unique ID for cluster"""
        ids = sorted(t.trajectory_id for t in trajectories)
        content = ":".join(ids)
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'cluster_id': self.cluster_id,
            'trajectories': [t.to_dict() for t in self.trajectories],
            'centroid': self.centroid,
            'created_at': self.created_at.isoformat(),
            'context': self.context,
            'size': self.size,
            'unique_agents': self.unique_agents,
            'avg_trajectory_length': self.avg_trajectory_length,
            'stability_score': self.stability_score,
            'metadata': self.metadata
        }


@dataclass
class Institution:
    """
    Stable behavioral cluster with normative force.
    
    An institution is a behavioral cluster that has achieved
    sufficient stability and persistence to exert influence
    on agent behavior.
    """
    institution_id: str
    name: str
    cluster: BehavioralCluster
    emergence_time: datetime
    context: str
    norm_strength: float = 0.0  # 0.0 to 1.0
    enforcement_mechanism: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def age_days(self) -> float:
        return (datetime.now() - self.emergence_time).total_seconds() / 86400
    
    @property
    def participant_count(self) -> int:
        return self.cluster.unique_agents
    
    def is_stable(self, threshold: float = 0.7) -> bool:
        """Check if institution is stable above threshold"""
        return self.cluster.stability_score >= threshold
    
    @classmethod
    def from_cluster(cls, cluster: BehavioralCluster, name: str, 
                     context: str, norm_strength: float = 0.5) -> 'Institution':
        """Create institution from stable cluster"""
        return cls(
            institution_id=cls._generate_id(name, cluster),
            name=name,
            cluster=cluster,
            emergence_time=cluster.created_at,
            context=context,
            norm_strength=norm_strength
        )
    
    @staticmethod
    def _generate_id(name: str, cluster: BehavioralCluster) -> str:
        """Generate unique ID for institution"""
        content = f"{name}:{cluster.cluster_id}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'institution_id': self.institution_id,
            'name': self.name,
            'cluster_id': self.cluster.cluster_id,
            'emergence_time': self.emergence_time.isoformat(),
            'context': self.context,
            'norm_strength': self.norm_strength,
            'enforcement_mechanism': self.enforcement_mechanism,
            'age_days': self.age_days,
            'participant_count': self.participant_count,
            'is_stable': self.is_stable(),
            'metadata': self.metadata
        }


@dataclass
class InformationField:
    """
    Contextual environment for signals and reactions.
    
    The information field represents the total informational
    environment within which institutional dynamics occur.
    """
    field_id: str
    context: str
    signals: List[Signal]
    entropy: float = 0.0
    density: float = 0.0
    polarization: float = 0.0
    concentration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def signal_count(self) -> int:
        return len(self.signals)
    
    @property
    def unique_sources(self) -> int:
        return len(set(s.source for s in self.signals))
    
    @classmethod
    def from_signals(cls, signals: List[Signal], context: str) -> 'InformationField':
        """Create information field from signals"""
        return cls(
            field_id=cls._generate_id(signals, context),
            context=context,
            signals=signals
        )
    
    @staticmethod
    def _generate_id(signals: List[Signal], context: str) -> str:
        """Generate unique ID for field"""
        ids = sorted(s.signal_id for s in signals[:100])  # Sample for ID
        content = f"{context}:{':'.join(ids)}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def compute_metrics(self) -> Dict[str, float]:
        """Compute field metrics"""
        if not self.signals:
            return {'entropy': 0.0, 'density': 0.0, 'polarization': 0.0, 'concentration': 0.0}
        
        # Entropy: diversity of sources
        from collections import Counter
        source_counts = Counter(s.source for s in self.signals)
        total = len(self.signals)
        entropy = 0.0
        for count in source_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * (p and (p * 0.6931471805599453))  # log2 approximation
        
        # Density: signals per unit time
        if len(self.signals) > 1:
            timestamps = sorted(s.timestamp for s in self.signals)
            duration = (timestamps[-1] - timestamps[0]).total_seconds()
            density = len(self.signals) / max(duration, 1)
        else:
            density = 0.0
        
        # Concentration: top sources share
        if source_counts:
            top_count = source_counts.most_common(1)[0][1]
            concentration = top_count / total
        else:
            concentration = 0.0
        
        self.entropy = entropy
        self.density = density
        self.concentration = concentration
        
        return {
            'entropy': entropy,
            'density': density,
            'polarization': self.polarization,
            'concentration': concentration
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'field_id': self.field_id,
            'context': self.context,
            'signal_count': self.signal_count,
            'unique_sources': self.unique_sources,
            'entropy': self.entropy,
            'density': self.density,
            'polarization': self.polarization,
            'concentration': self.concentration,
            'metrics_computed': self.entropy > 0 or self.density > 0,
            'metadata': self.metadata
        }


@dataclass
class Intervention:
    """
    External modification to the institutional system.
    
    Interventions are deliberate changes to the system
    designed to test causal relationships or achieve
    specific outcomes.
    """
    intervention_id: str
    intervention_type: str
    description: str
    start_time: datetime
    end_time: Optional[datetime]
    target_context: str
    parameters: Dict[str, Any]
    expected_effect: Optional[str] = None
    actual_effect: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_seconds(self) -> Optional[float]:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def is_active(self) -> bool:
        return self.end_time is None
    
    @classmethod
    def create(cls, intervention_type: str, description: str,
               target_context: str, parameters: Dict[str, Any],
               expected_effect: Optional[str] = None) -> 'Intervention':
        """Create a new intervention"""
        return cls(
            intervention_id=cls._generate_id(intervention_type, target_context),
            intervention_type=intervention_type,
            description=description,
            start_time=datetime.now(),
            end_time=None,
            target_context=target_context,
            parameters=parameters,
            expected_effect=expected_effect
        )
    
    @staticmethod
    def _generate_id(intervention_type: str, target_context: str) -> str:
        """Generate unique ID for intervention"""
        content = f"{intervention_type}:{target_context}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def complete(self, actual_effect: Optional[str] = None) -> None:
        """Mark intervention as complete"""
        self.end_time = datetime.now()
        if actual_effect:
            self.actual_effect = actual_effect
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'intervention_id': self.intervention_id,
            'intervention_type': self.intervention_type,
            'description': self.description,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'target_context': self.target_context,
            'parameters': self.parameters,
            'expected_effect': self.expected_effect,
            'actual_effect': self.actual_effect,
            'duration_seconds': self.duration_seconds,
            'is_active': self.is_active,
            'metadata': self.metadata
        }


@dataclass
class Forecast:
    """
    Predicted future state of the institutional system.
    
    Forecasts are generated based on current trajectories,
    cluster dynamics, and historical patterns.
    """
    forecast_id: str
    target: str  # What is being forecasted
    prediction: str
    confidence: float  # 0.0 to 1.0
    time_horizon: str  # e.g., "7d", "30d", "90d"
    created_at: datetime
    basis: List[str]  # Evidence/features used
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_high_confidence(self) -> bool:
        return self.confidence >= 0.7
    
    @classmethod
    def create(cls, target: str, prediction: str, confidence: float,
               time_horizon: str, basis: List[str]) -> 'Forecast':
        """Create a new forecast"""
        return cls(
            forecast_id=cls._generate_id(target, prediction),
            target=target,
            prediction=prediction,
            confidence=confidence,
            time_horizon=time_horizon,
            created_at=datetime.now(),
            basis=basis
        )
    
    @staticmethod
    def _generate_id(target: str, prediction: str) -> str:
        """Generate unique ID for forecast"""
        content = f"{target}:{prediction}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'forecast_id': self.forecast_id,
            'target': self.target,
            'prediction': self.prediction,
            'confidence': self.confidence,
            'time_horizon': self.time_horizon,
            'created_at': self.created_at.isoformat(),
            'basis': self.basis,
            'is_high_confidence': self.is_high_confidence,
            'metadata': self.metadata
        }


# Convenience function for creating normalized event records
def create_normalized_event(
    event_id: str,
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
    """
    Create a normalized event record following the canonical schema.
    
    This ensures all datasets can be converted to a unified format.
    """
    return {
        "event_id": event_id,
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
