#!/usr/bin/env python3
"""Check wiki for broken links and inconsistencies"""
import os
import re
from pathlib import Path
from collections import defaultdict

WIKI_DIR = "/workspace/live_wiki"

def get_all_pages():
    """Get all markdown pages in wiki"""
    pages = {}
    for f in Path(WIKI_DIR).glob("*.md"):
        if f.name in ["audit_wiki.py", "check_wiki_links.py"]:
            continue
        page_name = f.stem  # filename without .md
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        pages[page_name] = {
            'path': str(f),
            'content': content,
            'size': len(content)
        }
    return pages

def extract_wiki_links(content):
    """Extract [[Wiki Link]] style links from content"""
    # Match [[Link Text]] or [[Link Text|Display Text]]
    pattern = r'\[\[([^\]|]+)(?:\|[^]]+)?\]\]'
    matches = re.findall(pattern, content)
    return [m.strip() for m in matches]

def normalize_link(link):
    """Normalize link to match filename format"""
    # Replace spaces with hyphens, remove special chars
    normalized = link.replace(' ', '-').replace("'", "").replace('"', '')
    # Remove any double hyphens
    while '--' in normalized:
        normalized = normalized.replace('--', '-')
    return normalized

def check_broken_links(pages):
    """Find all broken links"""
    broken = defaultdict(list)
    existing_pages = set(pages.keys())
    
    for page_name, page_data in pages.items():
        links = extract_wiki_links(page_data['content'])
        for link in links:
            normalized = normalize_link(link)
            if normalized not in existing_pages:
                broken[normalized].append({
                    'source': page_name,
                    'original_link': link
                })
    
    return broken

def check_inconsistencies(pages):
    """Check for naming inconsistencies and other issues"""
    issues = []
    
    # Check for mixed naming conventions
    for page_name in pages.keys():
        # Check if page has spaces but should use hyphens
        if ' ' in page_name:
            issues.append(f"Page '{page_name}' uses spaces instead of hyphens")
    
    # Check for empty or very short pages
    for page_name, page_data in pages.items():
        if page_data['size'] < 100:
            issues.append(f"Page '{page_name}' is very small ({page_data['size']} bytes)")
        
        # Check if page has no content beyond title
        lines = page_data['content'].strip().split('\n')
        if len(lines) < 3:
            issues.append(f"Page '{page_name}' has minimal content ({len(lines)} lines)")
    
    return issues

def main():
    print("=" * 60)
    print("WIKI AUDIT REPORT")
    print("=" * 60)
    print()
    
    pages = get_all_pages()
    print(f"Total pages found: {len(pages)}")
    print()
    
    # List all pages
    print("PAGES:")
    print("-" * 40)
    for name in sorted(pages.keys()):
        print(f"  - {name}")
    print()
    
    # Check broken links
    broken = check_broken_links(pages)
    print("BROKEN LINKS:")
    print("-" * 40)
    if broken:
        for link, sources in sorted(broken.items(), key=lambda x: -len(x[1])):
            print(f"  ❌ [[{link}]] - referenced in {len(sources)} page(s):")
            for src in sources[:5]:  # Show first 5
                print(f"     → {src['source']} (as '{src['original_link']}')")
            if len(sources) > 5:
                print(f"     ... and {len(sources)-5} more")
    else:
        print("  ✅ No broken links found!")
    print()
    
    # Check inconsistencies
    issues = check_inconsistencies(pages)
    print("INCONSISTENCIES & ISSUES:")
    print("-" * 40)
    if issues:
        for issue in issues:
            print(f"  ⚠️  {issue}")
    else:
        print("  ✅ No inconsistencies found!")
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Pages: {len(pages)}")
    print(f"Broken Links: {sum(len(v) for v in broken.values())}")
    print(f"Unique Broken Targets: {len(broken)}")
    print(f"Issues Found: {len(issues)}")
    
    return len(broken) == 0 and len(issues) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
