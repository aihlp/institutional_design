#!/usr/bin/env python3
"""
Test script to demonstrate knowledge extraction without API calls
"""
import json
from pathlib import Path

# Read the input text
input_file = Path("inbox/institutional_theory_paper.txt")
text = input_file.read_text(encoding="utf-8")

print(f"Input text length: {len(text)} characters")
print(f"First 500 chars: {text[:500]}...")

# Simulated extraction result (what the API would return)
extracted_data = {
    "definitions": [
        {"text": "Institutions are empirically distinguishable, statistically stable clusters of behavioral trajectories", "context": "New empirical framework"},
        {"text": "Behavioral trajectory: time-ordered sequence of reactions produced by a single agent in response to informational signals", "context": "Tier 1 primitive"},
        {"text": "Behavioral cluster: grouping of similar behavioral trajectories identified through unsupervised learning", "context": "Tier 1 primitive"},
        {"text": "Behavioral spectrum: full distribution of possible reactions to a given informational signal", "context": "Tier 1 primitive"},
        {"text": "Informational signal: objectively recordable change in the information environment", "context": "Tier 1 primitive"}
    ],
    "facts": [
        {"text": "Digital platforms mediate substantial share of social and economic life", "context": "Empirical reality"},
        {"text": "Platform A/B tests systematically violate random assignment principle", "context": "Cornil and Hardisty 2025"},
        {"text": "Women are significantly less likely to be targeted by STEM education ads", "context": "Lambrecht and Tucker 2018"},
        {"text": "Every Facebook user participates in approximately 10 simultaneous experiments", "context": "Platform experimentation"},
        {"text": "Classical institutional theory cannot operationalize its central constructs", "context": "Measurement crisis"}
    ],
    "concepts": [
        {"text": "Platform-as-architect problem", "context": "Structural position of digital platforms"},
        {"text": "Rules-versus-equilibria debate", "context": "Institutional economics"},
        {"text": "Rapoport's subjectivism of system-identification", "context": "Methodological framework"},
        {"text": "Three-tier research architecture", "context": "Base definitions, theoretical scaffold, operationalization"},
        {"text": "Signal-to-norm dynamics", "context": "Tier 2 theoretical mechanism"}
    ],
    "entities": [
        {"text": "Douglass North", "context": "Classical institutional theorist"},
        {"text": "W. Richard Scott", "context": "Classical institutional theorist"},
        {"text": "Meta/Facebook", "context": "Digital platform"},
        {"text": "Google", "context": "Digital platform"},
        {"text": "Anatol Rapoport", "context": "Systems scientist"},
        {"text": "Cornil and Hardisty", "context": "Researchers on A/B testing"},
        {"text": "Lambrecht and Tucker", "context": "Researchers on algorithmic exclusion"}
    ],
    "relationships": [
        {"text": "Platforms generate informational signals", "source": "Digital platforms", "target": "Informational signals"},
        {"text": "Algorithms filter signal exposure", "source": "Machine-learning algorithms", "target": "User exposure"},
        {"text": "Behavioral patterns form institutions", "source": "Behavioral clusters", "target": "Institutions"},
        {"text": "Classical definitions fail to operationalize", "source": "North/Scott definitions", "target": "Measurement crisis"}
    ],
    "processes": [
        {"text": "Algorithmic optimization excludes demographic groups from signals", "source": "Cost-efficient targeting", "target": "Gender-differentiated information environments"},
        {"text": "A/B testing manipulates user experience", "source": "Platform experiments", "target": "Behavioral outcomes"},
        {"text": "Analyst identifies stable behavioral clusters", "source": "Raw behavioral data", "target": "Institutional identification"}
    ],
    "mechanisms": [
        {"text": "Algorithmic cost optimization produces systematic exclusion", "source": "Advertising bid structures", "target": "Demographic exclusion patterns"},
        {"text": "Machine-learning filters disrupt random assignment", "source": "Platform algorithms", "target": "Experimental bias"},
        {"text": "Signal-to-norm feedback reshapes information environment", "source": "Stabilized behavioral patterns", "target": "New informational signals"}
    ],
    "contexts": [
        {"text": "Digital platform mediation of social/economic life", "context": "Contemporary institutional environment"},
        {"text": "Measurement crisis in institutional theory", "context": "Academic discipline challenge"},
        {"text": "Regulatory accountability for platform-generated behavioral clusters", "context": "Policy implications"}
    ]
}

print("\n=== EXTRACTION RESULTS ===")
for category, items in extracted_data.items():
    print(f"\n{category.upper()}: {len(items)} items")
    for item in items[:3]:  # Show first 3
        print(f"  - {item['text'][:80]}...")

# Save to JSON for wiki processing
output_file = Path("extracted_knowledge.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, indent=2)

print(f"\nSaved extracted knowledge to {output_file}")
print("Extraction demonstration complete!")
