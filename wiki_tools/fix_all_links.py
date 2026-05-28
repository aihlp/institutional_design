#!/usr/bin/env python3
import re
from pathlib import Path

wiki_path = Path('/workspace/live_wiki_audit')

# Complete mapping of all broken link variations to correct page names
mappings = {
    # Already fixed in previous pass
    'behavioral spectrum': 'Behavioral-Spectrum',
    'behavioral cluster': 'Behavioral-Cluster',
    'core concepts': 'Core-Concepts',
    'three tier architecture': 'Three-Tier-Architecture',
    'new foundation': 'Rules-to-Clusters',
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
    'ab testing illusion': 'AB-Testing-Illusion',
    'behavioral pattern': 'Behavioral-Pattern',
    'digital-platforms': 'Digital-Acceleration',
    'behavioural approach': 'Behavioural-Approach',
    'a/b testing illusion': 'AB-Testing-Illusion',
    'information field': 'Information-Field',
    'classical theory': 'Classical-Theory-Critique',
    'digital platforms': 'Digital-Acceleration',
    'classical-theory': 'Classical-Theory-Critique',
    
    # New pages created - should now resolve
    'Classical-Theory-Critique': 'Classical-Theory-Critique',
    'Institutional-Anomie': 'Institutional-Anomie',
    'classical-theory-critique': 'Classical-Theory-Critique',
    
    # Remaining edge cases
    'New-Foundation': 'Rules-to-Clusters',
    'Spectral Belonging': 'Behavioral-Spectrum',
    'Signal Genesis': 'Informational-Signal',
    'Three-Tier Architecture': 'Three-Tier-Architecture',
}

wiki_link_pattern = r'\[\[([^\]]+)\]\]'
files_modified = 0

for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    def fix_link(match):
        link_text = match.group(1).strip()
        if '|' in link_text:
            target, display = link_text.split('|', 1)
        else:
            target = link_text
            display = None
        
        target_lower = target.lower()
        if target_lower in {k.lower(): k for k in mappings.keys()}:
            # Find the actual key
            for k in mappings.keys():
                if k.lower() == target_lower:
                    new_target = mappings[k]
                    break
            if display:
                return f'[[{new_target}|{display}]]'
            else:
                return f'[[{new_target}]]'
        
        return match.group(0)
    
    content = re.sub(wiki_link_pattern, fix_link, content)
    
    if content != original:
        files_modified += 1
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {md_file.name}")

print(f"\n✅ Modified {files_modified} additional files")

# Final verification
print("\n=== FINAL VERIFICATION ===\n")
broken = []
existing_pages = set(p.stem for p in wiki_path.glob("*.md") if p.name != "README.md")

for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in re.finditer(wiki_link_pattern, content):
        link_target = match.group(1).split('|')[0].strip()
        if link_target not in existing_pages:
            broken.append({'target': link_target, 'file': md_file.stem})

if broken:
    print(f"⚠️  Still broken: {len(broken)} links")
    from collections import Counter
    by_target = Counter(b['target'] for b in broken)
    for target, count in by_target.most_common(20):
        print(f"  {target} - {count} refs")
else:
    print("🎉 ALL LINKS FIXED! Wiki is fully connected.")
