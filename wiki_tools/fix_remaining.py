#!/usr/bin/env python3
import re
from pathlib import Path

wiki_path = Path('/workspace/live_wiki_audit')

# Additional mappings for remaining broken links
mappings = {
    'Classical-Theory-Critique': 'Classical-Theory-Critique',  # Need to create this page or map to existing
    'Institutional-Anomie': 'Institutional-Anomie',  # Need to create
    'New-Foundation': 'Rules-to-Clusters',
    'Spectral Belonging': 'Behavioral-Spectrum',
    'Signal Genesis': 'Informational-Signal',
    'Three-Tier Architecture': 'Three-Tier-Architecture',
    'classical-theory-critique': 'Classical-Theory-Critique',
}

# Check what pages actually exist
existing_pages = set()
for md_file in wiki_path.glob("*.md"):
    if md_file.name != "README.md":
        existing_pages.add(md_file.stem)

print("Existing pages:")
for p in sorted(existing_pages):
    print(f"  {p}")

# The issue: Classical-Theory-Critique and Institutional-Anomie don't exist as pages
# They are referenced but the content is in other pages
# Let's check where they're referenced from
print("\n=== Checking references to missing pages ===\n")

wiki_link_pattern = r'\[\[([^\]]+)\]\]'
for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in re.finditer(wiki_link_pattern, content):
        link_target = match.group(1).split('|')[0].strip()
        if link_target in ['Classical-Theory-Critique', 'Institutional-Anomie']:
            print(f"{md_file.stem}: [[{link_target}]]")
