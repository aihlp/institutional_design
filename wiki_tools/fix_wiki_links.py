#!/usr/bin/env python3
"""
Fix broken wiki links by normalizing naming conventions
Pattern: Links use spaces, pages use hyphens
Solution: Update all [[Link Target]] to match actual page names
"""

import os
import re
from pathlib import Path

wiki_path = Path('/workspace/live_wiki_audit')

# Build mapping from normalized names to actual page names
pages = {}
for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    page_name = md_file.stem
    # Create variations that might be linked
    pages[page_name.lower().replace('-', ' ')] = page_name
    pages[page_name.lower()] = page_name
    pages[page_name.replace('-', ' ').lower()] = page_name

print(f"Indexed {len(pages)} page name variations")

# Define explicit mappings for problematic cases
mappings = {
    'behavioral spectrum': 'Behavioral-Spectrum',
    'behavioral cluster': 'Behavioral-Cluster',
    'core concepts': 'Core-Concepts',
    'three tier architecture': 'Three-Tier-Architecture',
    'new foundation': 'Rules-to-Clusters',  # Based on context
    'informational signal': 'Informational-Signal',
    'rules to clusters': 'Rules-to-Clusters',
    'algorithmic exclusion': 'Algorithmic-Exclusion',
    'behavioral trajectory': 'Behavioral-Trajectory',
    'the paradox': 'The-Paradox',
    'rapoport subjectivism': 'Rapoport-Subjectivism',
    'measurement dead end': 'Measurement-Dead-End',
    'platform architect': 'Platform-Architect',
    'cluster analysis example': 'Cluster-Analysis-Example',
    'scott pillars': 'Scott-Pillars',
    'north rules': 'North-Rules',
    'perception filter': 'Perception-Filter',
    'digital platforms as stress tests': 'Digital-Acceleration',
    'classical theory critique': 'Classical-Theory-Critique',
    'institutional-anomie': 'Institutional-Anomie',
    'ab testing illusion': 'AB-Testing-Illusion',
    'behavioral pattern': 'Behavioral-Pattern',
    'digital-platforms': 'Digital-Acceleration',
    'behavioural approach': 'Behavioural-Approach',
    'a/b testing illusion': 'AB-Testing-Illusion',
    'information field': 'Information-Field',
    'classical-theory-critique': 'Classical-Theory-Critique',
    'classical theory': 'Classical-Theory-Critique',
    'digital platforms': 'Digital-Acceleration',
    'classical-theory': 'Classical-Theory-Critique',
    'behavioral-spectrum': 'Behavioral-Spectrum',
    'behavioral-cluster': 'Behavioral-Cluster',
}

# Fix function
def fix_link(match):
    link_text = match.group(1).strip()
    # Check if it has display text
    if '|' in link_text:
        target, display = link_text.split('|', 1)
    else:
        target = link_text
        display = None
    
    # Try to find matching page
    target_lower = target.lower()
    if target_lower in mappings:
        new_target = mappings[target_lower]
        if display:
            return f'[[{new_target}|{display}]]'
        else:
            return f'[[{new_target}]]'
    
    # If no mapping found, keep original
    return match.group(0)

# Process all files
files_modified = 0
wiki_link_pattern = r'\[\[([^\]]+)\]\]'

for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = re.sub(wiki_link_pattern, fix_link, content)
    
    if content != original:
        files_modified += 1
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {md_file.name}")

print(f"\n✅ Modified {files_modified} files")

# Verify fixes
print("\n=== Verifying fixes ===\n")
broken_after = []
links_found = {}

for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    page_name = md_file.stem
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in re.finditer(wiki_link_pattern, content):
        link_target = match.group(1).split('|')[0].strip()
        if link_target not in links_found:
            links_found[link_target] = []
        links_found[link_target].append(md_file.stem)

for link_target, sources in links_found.items():
    if link_target not in [p.stem for p in wiki_path.glob("*.md") if p.name != "README.md"]:
        broken_after.append({'target': link_target, 'count': len(sources), 'sources': sources})

broken_after.sort(key=lambda x: x['count'], reverse=True)

if broken_after:
    print(f"Still broken: {len(broken_after)} links")
    for bl in broken_after[:20]:
        print(f"  {bl['target']} - {bl['count']} refs")
else:
    print("🎉 All links fixed!")
