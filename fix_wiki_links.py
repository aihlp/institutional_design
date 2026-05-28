#!/usr/bin/env python3
"""
Fix common wiki link typos and inconsistencies
"""

import os
import re
from pathlib import Path

# Link fixes: old_text -> new_text
LINK_FIXES = {
    'Cluster Analysis Example': 'Behavioral Cluster Analysis Example',
    'AB Testing Illusion': 'A/B Testing Illusion',
    'The Paradox': 'The Paradox at the Heart of Institutional Theory',
    'Platform Architect': 'Platform-as-Architect Problem',
    'Rapoport-Subjectivism': "Rapoport's Subjectivism",
    'Measurement Dead End': 'The Measurement Dead End',
    'Scott-Pillars': "Scott's Three Pillars",
    'Algorithmic exclusion': 'Algorithmic Exclusion',
}

def fix_links_in_file(filepath):
    """Fix links in a single file, return number of changes made"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    for old_link, new_link in LINK_FIXES.items():
        # Match [[old_link]] patterns
        pattern = r'\[\[' + re.escape(old_link) + r'\]\]'
        replacement = f'[[{new_link}]]'
        
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)
            print(f"  Fixed {len(matches)} occurrence(s): [[{old_link}]] → [[{new_link}]]")
    
    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return changes_made

def main():
    wiki_dir = "/workspace/wiki"
    
    print("=" * 80)
    print("WIKI LINK FIXER")
    print("=" * 80)
    print()
    
    total_changes = 0
    files_changed = 0
    
    for md_file in Path(wiki_dir).rglob("*.md"):
        changes = fix_links_in_file(md_file)
        if changes > 0:
            files_changed += 1
            total_changes += changes
            rel_path = md_file.relative_to(wiki_dir)
            print(f"  → {rel_path}")
            print()
    
    print("=" * 80)
    print(f"SUMMARY: Fixed {total_changes} links in {files_changed} files")
    print("=" * 80)
    
    if total_changes == 0:
        print("No changes needed!")
    else:
        print("\n✅ Link fixes applied successfully!")
        print("\nNext steps:")
        print("1. Review changes with: git diff")
        print("2. Create missing pages for remaining broken links")
        print("3. Run audit script to verify: python3 audit_wiki_links.py")

if __name__ == "__main__":
    main()
