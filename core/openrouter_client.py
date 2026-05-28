"""
OpenRouter LLM Client for Institutional Analysis

This module provides integration with OpenRouter-connected LLMs for:
- Semantic cluster interpretation
- Institutional drift explanation
- Ontology assistance
- Anomaly detection and explanation

IMPORTANT: LLMs are used ONLY for interpretation and semantic labeling,
NOT for generating measurable metrics or replacing computational analysis.
"""

import os
import json
import yaml
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime


class OpenRouterClient:
    """Client for interacting with OpenRouter API for institutional analysis"""
    
    def __init__(self, config_path: str = "config/openrouter.yaml"):
        """Initialize client with configuration"""
        self.config = self._load_config(config_path)
        self.api_key = os.environ.get('OPENROUTER_API_KEY', '')
        self.base_url = "https://openrouter.ai/api/v1"
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        
        # Request logging
        self.request_count = 0
        self.token_count = 0
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            # Expand environment variables
            if 'api_key' in config and config['api_key'].startswith('${'):
                env_var = config['api_key'][2:-1]
                config['api_key'] = os.environ.get(env_var, '')
            return config
        except FileNotFoundError:
            # Return default config
            return {
                'provider': {'primary': 'anthropic/claude-3-5-sonnet'},
                'temperature': 0.3,
                'max_tokens': 4096
            }
    
    def _make_request(self, messages: List[Dict[str, str]], 
                      model: Optional[str] = None,
                      temperature: Optional[float] = None,
                      max_tokens: Optional[int] = None,
                      response_format: str = "json") -> Dict[str, Any]:
        """Make API request to OpenRouter"""
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        # Use configured model or default
        model = model or self.config.get('provider', {}).get('primary', 'anthropic/claude-3-5-sonnet')
        temperature = temperature or self.config.get('temperature', 0.3)
        max_tokens = max_tokens or self.config.get('max_tokens', 4096)
        
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        if response_format == "json":
            payload['response_format'] = {'type': 'json_object'}
        
        try:
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=self.config.get('timeout', 60)
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Track usage
            self.request_count += 1
            if 'usage' in result:
                self.token_count += result['usage'].get('total_tokens', 0)
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def interpret_cluster(self, cluster_data: Dict[str, Any], 
                          context: str = "") -> Dict[str, Any]:
        """
        Interpret a behavioral cluster using LLM.
        
        Args:
            cluster_data: Dictionary containing cluster characteristics
            context: Additional context about the dataset/source
        
        Returns:
            Interpretation including institution type, characteristics, confidence
        """
        
        system_prompt = """You are an institutional science analyst. Your task is to interpret behavioral clusters and identify potential institutions.

Analyze the provided cluster data and provide:
1. A descriptive name for the behavioral pattern
2. The likely institution type (e.g., "collaborative governance", "competitive signaling", "norm enforcement")
3. Key characteristics observed
4. Confidence level (0.0-1.0)
5. Suggested follow-up analysis

Respond ONLY with valid JSON in this format:
{
    "institution_name": "...",
    "institution_type": "...",
    "characteristics": ["...", "..."],
    "confidence": 0.0,
    "interpretation": "...",
    "follow_up_suggestions": ["...", "..."]
}"""
        
        user_message = f"""Analyze this behavioral cluster:

Context: {context}

Cluster Data:
{json.dumps(cluster_data, indent=2)}

Provide your institutional interpretation."""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        # Use cluster interpretation settings
        use_case_config = self.config.get('use_cases', {}).get('cluster_interpretation', {})
        
        result = self._make_request(
            messages,
            model=use_case_config.get('model'),
            temperature=use_case_config.get('temperature'),
            max_tokens=use_case_config.get('max_tokens')
        )
        
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    
    def explain_drift(self, metrics_before: Dict[str, float],
                      metrics_after: Dict[str, float],
                      intervention: Optional[str] = None) -> Dict[str, Any]:
        """
        Explain detected institutional drift.
        
        Args:
            metrics_before: Metrics before the change
            metrics_after: Metrics after the change
            intervention: Description of any intervention applied
        
        Returns:
            Explanation of the drift, possible causes, implications
        """
        
        system_prompt = """You are an institutional dynamics expert. Analyze changes in institutional metrics and provide explanations for observed drift.

Consider:
- Changes in entropy (fragmentation/concentration)
- Changes in density (activity levels)
- Changes in volatility (stability)
- Potential external factors

Respond ONLY with valid JSON in this format:
{
    "drift_type": "...",
    "magnitude": "low|medium|high",
    "key_changes": ["...", "..."],
    "possible_causes": ["...", "..."],
    "implications": ["...", "..."],
    "confidence": 0.0
}"""
        
        intervention_text = f"\nIntervention applied: {intervention}" if intervention else "\nNo specific intervention applied."
        
        user_message = f"""Analyze the institutional drift:

Metrics Before:
{json.dumps(metrics_before, indent=2)}

Metrics After:
{json.dumps(metrics_after, indent=2)}
{intervention_text}

Explain the observed drift."""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        use_case_config = self.config.get('use_cases', {}).get('drift_explanation', {})
        
        result = self._make_request(
            messages,
            model=use_case_config.get('model'),
            temperature=use_case_config.get('temperature'),
            max_tokens=use_case_config.get('max_tokens')
        )
        
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    
    def map_to_ontology(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map raw event data to institutional ontology primitives.
        
        Args:
            event_data: Raw event or behavior data
        
        Returns:
            Mapping to Signal, Reaction, and other primitives
        """
        
        system_prompt = """You are an ontology mapping specialist for institutional science. Map raw behavioral events to the institutional ontology.

The ontology includes:
- Signal: Informational stimulus
- Reaction: Agent response (engage, ignore, amplify, suppress, counter, adapt, exit)
- BehavioralTrajectory: Sequence of reactions over time
- BehavioralCluster: Group of similar trajectories
- Institution: Stable cluster with normative force

Respond ONLY with valid JSON in this format:
{
    "signal_type": "...",
    "reaction_type": "...",
    "signal_characteristics": {...},
    "reaction_characteristics": {...},
    "confidence": 0.0,
    "notes": "..."
}"""
        
        user_message = f"""Map this event to institutional ontology:

Event Data:
{json.dumps(event_data, indent=2)}

Identify the signal type and likely reaction type."""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        use_case_config = self.config.get('use_cases', {}).get('ontology_mapping', {})
        
        result = self._make_request(
            messages,
            model=use_case_config.get('model'),
            temperature=use_case_config.get('temperature'),
            max_tokens=use_case_config.get('max_tokens')
        )
        
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    
    def detect_anomalies(self, time_series: List[Dict[str, Any]],
                         metric_name: str) -> Dict[str, Any]:
        """
        Detect and explain anomalies in institutional metrics.
        
        Args:
            time_series: Time series of metric values
            metric_name: Name of the metric being analyzed
        
        Returns:
            Detected anomalies with explanations
        """
        
        system_prompt = """You are an anomaly detection specialist for institutional metrics. Identify and explain unusual patterns in time series data.

Look for:
- Sudden spikes or drops
- Unusual volatility
- Pattern breaks
- Seasonal deviations

Respond ONLY with valid JSON in this format:
{
    "anomalies_detected": [...],
    "severity": "low|medium|high",
    "possible_explanations": ["...", "..."],
    "recommended_actions": ["...", "..."]
}"""
        
        user_message = f"""Detect anomalies in this {metric_name} time series:

Data points: {len(time_series)}
Time series:
{json.dumps(time_series[:50], indent=2)}  # Limit to first 50 points

Identify any anomalies and provide explanations."""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        use_case_config = self.config.get('use_cases', {}).get('anomaly_detection', {})
        
        result = self._make_request(
            messages,
            model=use_case_config.get('model'),
            temperature=use_case_config.get('temperature'),
            max_tokens=use_case_config.get('max_tokens')
        )
        
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    
    def generate_summary(self, experiment_results: Dict[str, Any]) -> str:
        """
        Generate a natural language summary of experiment results.
        
        Args:
            experiment_results: Complete experiment results dictionary
        
        Returns:
            Human-readable summary
        """
        
        system_prompt = """You are a research communication specialist. Summarize institutional science experiment results in clear, accessible language.

Include:
- Main findings
- Key metrics
- Notable patterns
- Implications

Keep it concise (2-3 paragraphs)."""
        
        user_message = f"""Summarize these experiment results:

{json.dumps(experiment_results, indent=2)}

Provide a clear, concise summary suitable for researchers."""
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
        
        result = self._make_request(messages, temperature=0.4, max_tokens=1024)
        return result['choices'][0]['message']['content']
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return {
            'request_count': self.request_count,
            'token_count': self.token_count,
            'estimated_cost': self.token_count * 0.00001  # Rough estimate
        }


# Convenience function for quick cluster interpretation
def quick_interpret_cluster(cluster_data: Dict[str, Any], 
                            api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick cluster interpretation without full client setup.
    
    Args:
        cluster_data: Cluster characteristics
        api_key: OpenRouter API key (or set OPENROUTER_API_KEY env var)
    
    Returns:
        Interpretation results
    """
    if api_key:
        os.environ['OPENROUTER_API_KEY'] = api_key
    
    client = OpenRouterClient()
    return client.interpret_cluster(cluster_data)
