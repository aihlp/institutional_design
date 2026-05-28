#!/usr/bin/env python3
import os
import re
from collections import defaultdict
from pathlib import Path

wiki_path = Path('/workspace/live_wiki_audit')
pages = {}
links_found = defaultdict(list)

# Load all pages
for md_file in wiki_path.glob("*.md"):
    if md_file.name == "README.md":
        continue
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    page_name = md_file.stem
    pages[page_name] = {'content': content, 'path': md_file}

print(f"Loaded {len(pages)} pages")

# Extract all wiki-style links
wiki_link_pattern = r'\[\[([^\]]+)\]\]'
for page_name, page_data in pages.items():
    content = page_data['content']
    for match in re.finditer(wiki_link_pattern, content):
        link_target = match.group(1).strip()
        if '|' in link_target:
            link_target = link_target.split('|')[0]
        links_found[link_target].append(page_name)

print(f"Found {len(links_found)} unique link targets")

# Find broken links
broken_links = []
for link_target, occurrences in links_found.items():
    if link_target not in pages:
        # Check case-insensitive
        found = False
        for page_name in pages.keys():
            if page_name.lower() == link_target.lower():
                found = True
                break
        if not found:
            broken_links.append({'target': link_target, 'count': len(occurrences), 'sources': list(set(occurrences))})

broken_links.sort(key=lambda x: x['count'], reverse=True)

print(f"\n=== BROKEN LINKS ({len(broken_links)}) ===\n")
for bl in broken_links[:30]:
    print(f"{bl['target']} - {bl['count']} refs from: {', '.join(bl['sources'][:5])}")

# Check for thin pages
print(f"\n=== THIN PAGES (<1000 chars) ===\n")
for page_name, page_data in pages.items():
    if len(page_data['content']) < 1000:
        print(f"{page_name}: {len(page_data['content'])} chars")

# Check Home.md structure
if 'Home' in pages:
    home_content = pages['Home']['content']
    links_in_home = re.findall(r'\[\[([^\]]+)\]\]', home_content)
    print(f"\n=== HOME.MD has {len(links_in_home)} internal links ===")
    
# Check index.md
if 'index' in pages:
    index_content = pages['index']['content']
    links_in_index = re.findall(r'\[\[([^\]]+)\]\]', index_content)
    print(f"=== INDEX.MD has {len(links_in_index)} internal links ===")
