#!/usr/bin/env python3
"""
Wiki Link Auditor - Checks for broken links, inconsistencies, and structural issues
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_all_links(wiki_dir):
    """Extract all wiki links [[...]] from markdown files"""
    links = defaultdict(list)  # link_text -> [(file, line_num), ...]
    
    for md_file in Path(wiki_dir).rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
        for line_num, line in enumerate(lines, 1):
            # Find all [[...]] patterns
            matches = re.findall(r'\[\[([^\]]+)\]\]', line)
            for match in matches:
                links[match].append((str(md_file), line_num, line.strip()))
    
    return links

def get_existing_pages(wiki_dir):
    """Get all existing page titles from H1 headers and filenames"""
    pages = {}  # title -> file_path
    
    for md_file in Path(wiki_dir).rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract H1 title
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
            pages[title] = str(md_file)
        
        # Also map filename (without .md) to path
        filename = md_file.stem.replace('-', ' ').title()
        # Special handling for some patterns
        if md_file.name == 'index.md':
            pages['index.md'] = str(md_file)
    
    return pages

def normalize_link(link_text):
    """Normalize link text for comparison"""
    # Remove extra spaces, handle common variations
    normalized = link_text.strip()
    return normalized

def check_broken_links(links, pages):
    """Check which links don't have corresponding pages"""
    broken = {}
    
    for link_text, occurrences in links.items():
        # Check if exact match exists
        if link_text not in pages:
            # Try some normalizations
            found = False
            
            # Try without "Category: " prefix
            if link_text.startswith("Category: "):
                alt_text = link_text.replace("Category: ", "")
                if alt_text in pages:
                    found = True
            
            # Try lowercase/uppercase variants
            if not found:
                for page_title in pages.keys():
                    if page_title.lower() == link_text.lower():
                        found = True
                        break
            
            # Try singular/plural variants
            if not found:
                if link_text.endswith('s'):
                    singular = link_text[:-1]
                    if singular in pages:
                        found = True
                else:
                    plural = link_text + 's'
                    if plural in pages:
                        found = True
            
            if not found:
                broken[link_text] = occurrences
    
    return broken

def find_orphaned_files(wiki_dir, links):
    """Find files that are not linked from anywhere"""
    # Get all referenced filenames
    referenced_files = set()
    for link_text in links.keys():
        # Convert link text to potential filename
        filename = link_text.lower().replace(' ', '-').replace('/', '-') + '.md'
        referenced_files.add(filename)
        # Also try with underscores
        referenced_files.add(link_text.lower().replace(' ', '_').replace('/', '_') + '.md')
    
    orphaned = []
    for md_file in Path(wiki_dir).rglob("*.md"):
        # Skip index.md and README.md as they are entry points
        if md_file.name in ['README.md']:
            continue
        
        rel_path = md_file.relative_to(wiki_dir)
        if md_file.name not in referenced_files and str(rel_path) not in referenced_files:
            # Check if file is linked with full path
            is_linked = False
            for link_text in links.keys():
                if md_file.stem in link_text.lower() or md_file.name in link_text:
                    is_linked = True
                    break
            
            if not is_linked:
                orphaned.append(str(rel_path))
    
    return orphaned

def analyze_link_consistency(links):
    """Find inconsistent link naming (singular vs plural, case variations)"""
    inconsistencies = []
    
    # Group similar links
    link_groups = defaultdict(list)
    for link_text in links.keys():
        # Normalize to lowercase for grouping
        key = link_text.lower()
        link_groups[key].append(link_text)
    
    for key, variants in link_groups.items():
        if len(variants) > 1:
            # Found variants of the same link
            inconsistencies.append((key, variants))
    
    return inconsistencies

def main():
    wiki_dir = "/workspace/wiki"
    
    print("=" * 80)
    print("WIKI LINK AUDIT REPORT")
    print("=" * 80)
    print()
    
    # Extract all links
    print("📊 Extracting links from wiki files...")
    links = extract_all_links(wiki_dir)
    print(f"   Found {len(links)} unique wiki links")
    total_occurrences = sum(len(occ) for occ in links.values())
    print(f"   Total link occurrences: {total_occurrences}")
    print()
    
    # Get existing pages
    print("📄 Cataloging existing pages...")
    pages = get_existing_pages(wiki_dir)
    print(f"   Found {len(pages)} pages with H1 titles")
    print()
    
    # Check for broken links
    print("🔍 Checking for broken links...")
    broken = check_broken_links(links, pages)
    print(f"   ❌ Found {len(broken)} broken links")
    print()
    
    if broken:
        print("   Broken links by reference count:")
        print("   " + "-" * 70)
        sorted_broken = sorted(broken.items(), key=lambda x: len(x[1]), reverse=True)
        for link_text, occurrences in sorted_broken[:30]:  # Show top 30
            print(f"   • [[{link_text}]] - referenced {len(occurrences)} times")
            if len(occurrences) <= 3:
                for file, line, context in occurrences:
                    rel_file = file.replace('/workspace/wiki/', '')
                    print(f"     - {rel_file}:{line}")
        if len(sorted_broken) > 30:
            print(f"   ... and {len(sorted_broken) - 30} more broken links")
        print()
    
    # Find orphaned files
    print("🔍 Finding orphaned files...")
    orphaned = find_orphaned_files(wiki_dir, links)
    print(f"   ⚠️  Found {len(orphaned)} potentially orphaned files")
    if orphaned:
        for file in orphaned[:20]:
            print(f"   • {file}")
        if len(orphaned) > 20:
            print(f"   ... and {len(orphaned) - 20} more")
    print()
    
    # Analyze consistency
    print("🔍 Analyzing link naming consistency...")
    inconsistencies = analyze_link_consistency(links)
    print(f"   ⚠️  Found {len(inconsistencies)} naming inconsistencies")
    if inconsistencies:
        for key, variants in inconsistencies[:20]:
            print(f"   • '{key}': {variants}")
    print()
    
    # Summary statistics
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total unique links: {len(links)}")
    print(f"Broken links: {len(broken)} ({len(broken)/len(links)*100:.1f}%)")
    print(f"Orphaned files: {len(orphaned)}")
    print(f"Naming inconsistencies: {len(inconsistencies)}")
    print()
    
    # High priority fixes
    print("=" * 80)
    print("HIGH PRIORITY FIXES (links referenced 5+ times)")
    print("=" * 80)
    high_priority = [(link, occs) for link, occs in broken.items() if len(occs) >= 5]
    high_priority.sort(key=lambda x: len(x[1]), reverse=True)
    
    if high_priority:
        for link_text, occurrences in high_priority:
            print(f"\n🔴 [[{link_text}]] - {len(occurrences)} references")
            print("   Referenced in:")
            files_set = set()
            for file, line, _ in occurrences:
                rel_file = file.replace('/workspace/wiki/', '')
                files_set.add(rel_file)
            for f in sorted(files_set)[:10]:
                print(f"   - {f}")
            if len(files_set) > 10:
                print(f"   ... and {len(files_set) - 10} more files")
    else:
        print("No high priority broken links found!")
    
    print()
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print("""
1. CRITICAL: Create missing pages for high-priority broken links
2. IMPORTANT: Fix naming inconsistencies (singular vs plural, case)
3. REVIEW: Add navigation links to orphaned files from index.md
4. CONSIDER: Update link checker in CI/CD pipeline
    """)

if __name__ == "__main__":
    main()
