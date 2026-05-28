#!/usr/bin/env python3
"""Fix broken links in README.md"""

readme_path = "/workspace/live_wiki/README.md"

# Read current content
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define link replacements (old_link -> new_link)
replacements = {
    "The Paradox at the Heart of Institutional Theory": "The-Paradox",
    "From Rules to Behavioral Clusters": "Rules-to-Clusters",
    "Three-Tier Research Architecture": "Three-Tier-Architecture",
    "Classical Institutional Theory": "Classical-Theory-Critique",
    "Digital Platforms as Empirical Stress Tests": "Digital-Acceleration",
    "New Empirical Foundation": "Core-Concepts",
    "North's Rules of the Game": "North-Rules",
    "Scott's Three Pillars": "Scott-Pillars",
    "The Measurement Dead End": "Measurement-Dead-End",
    "A/B Testing Illusion": "AB-Testing-Illusion",
    "Platform-as-Architect Problem": "Platform-Architect",
    "Rapoport's Subjectivism": "Rapoport-Subjectivism",
    "index.md": "index",
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(f"[[{old}]]", f"[[{new}]]")

# Write updated content
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed README.md links")
print("\nReplacements made:")
for old, new in replacements.items():
    print(f"  [[{old}]] → [[{new}]]")
