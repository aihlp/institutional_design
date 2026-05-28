#!/usr/bin/env python3
"""
Create wiki pages from extracted knowledge JSON
Demonstrates the 8-part Basic+Dynamic structure with relinking
"""
import json
from pathlib import Path
from datetime import datetime

# Load extracted knowledge
with open("extracted_knowledge.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Create wiki directory if it doesn't exist
wiki_dir = Path("wiki")
wiki_dir.mkdir(exist_ok=True)

def sanitize_filename(name):
    """Convert text to safe filename"""
    return name.lower().replace(" ", "_").replace("/", "_").replace("'", "")[:50]

def create_wiki_page(category, items):
    """Create a wiki page for a category"""
    title = category.replace("_", " ").title()
    filename = wiki_dir / f"{sanitize_filename(category)}.md"
    
    content = f"""# {title}

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Source: institutional_theory_paper*

---

"""
    
    # Add relink navigation
    all_categories = ["definitions", "facts", "concepts", "entities", "relationships", "processes", "mechanisms", "contexts"]
    content += "## Navigation\n\n"
    content += " | ".join([f"[{cat.title()}](./{sanitize_filename(cat)}.md)" for cat in all_categories]) + "\n\n---\n\n"
    
    content += f"## {len(items)} {category[:-1].title()}s Extracted\n\n"
    
    for i, item in enumerate(items, 1):
        text = item.get("text", "No text")
        context = item.get("context", "")
        source = item.get("source", "")
        target = item.get("target", "")
        
        content += f"### {i}. {text}\n\n"
        
        if context:
            content += f"**Context:** {context}\n\n"
        if source:
            content += f"**Source:** {source}\n\n"
        if target:
            content += f"**Target:** {target}\n\n"
        
        # Add relinks for dynamic parts
        if category in ["relationships", "processes", "mechanisms"]:
            content += "**Relinks:**\n"
            if source:
                content += f"- ← [[{source}]]\n"
            if target:
                content += f"- → [[{target}]]\n"
            content += "\n"
        
        content += "---\n\n"
    
    # Add backlinks section
    content += f"\n## Backlinks\n\n"
    content += f"Items in this category that are referenced by other categories.\n\n"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filename

def create_index_page():
    """Create main wiki index with overview of all categories"""
    filename = wiki_dir / "README.md"
    
    content = f"""# Knowledge Wiki - Institutional Theory

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Source Paper: Defining Institutions: Why Modern Data Demands a New Empirical Institutional Theory*

---

## Overview

This wiki organizes knowledge extracted from the institutional theory paper into **8 fundamental parts** across two dimensions:

### Basic (Static) Parts
The constituent elements of knowledge:
- **Definitions**: Explanations of terms and conceptual primitives
- **Facts**: Verifiable statements and empirical observations  
- **Concepts**: Abstract ideas and theoretical constructs
- **Entities**: Concrete objects, actors, and organizations

### Dynamic (Relational) Parts  
The connections and flows between elements:
- **Relationships**: Connections between entities/concepts (with source→target relinks)
- **Processes**: Sequences of actions and transformations (with source→target relinks)
- **Mechanisms**: Causal pathways and explanatory logics (with source→target relinks)
- **Contexts**: Situational conditions and boundary conditions

---

## Wiki Pages

| Category | Type | Items | Description |
|----------|------|-------|-------------|
"""
    
    category_descriptions = {
        "definitions": ("Basic", str(len(data["definitions"])), "Foundational term explanations"),
        "facts": ("Basic", str(len(data["facts"])), "Empirical observations"),
        "concepts": ("Basic", str(len(data["concepts"])), "Theoretical constructs"),
        "entities": ("Basic", str(len(data["entities"])), "Actors and organizations"),
        "relationships": ("Dynamic", str(len(data["relationships"])), "Connections with relinks"),
        "processes": ("Dynamic", str(len(data["processes"])), "Temporal flows with relinks"),
        "mechanisms": ("Dynamic", str(len(data["mechanisms"])), "Causal pathways with relinks"),
        "contexts": ("Basic", str(len(data["contexts"])), "Boundary conditions")
    }
    
    for cat, (type_, count, desc) in category_descriptions.items():
        content += f"| [{cat.title()}](./{sanitize_filename(cat)}.md) | {type_} | {count} | {desc} |\n"
    
    content += """
---

## Relink Structure

Dynamic parts (Relationships, Processes, Mechanisms) include bidirectional relinks:
- **Source → Target** notation shows directional connections
- Each dynamic item links to related entities and concepts
- Enables tracing causal chains and dependency networks

## Usage

1. Start with **Definitions** to understand key terms
2. Review **Facts** for empirical grounding
3. Explore **Concepts** for theoretical frameworks
4. Identify **Entities** involved in the domain
5. Trace **Relationships**, **Processes**, and **Mechanisms** to understand dynamics
6. Consider **Contexts** for boundary conditions

---

*Wiki generated automatically from knowledge extraction pipeline*
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filename

# Create all wiki pages
print("Creating wiki pages...")
for category, items in data.items():
    filename = create_wiki_page(category, items)
    print(f"  Created: {filename}")

# Create index page
index_file = create_index_page()
print(f"  Created: {index_file}")

print("\n✓ Wiki created successfully with 8 fundamental parts!")
print(f"  - 4 Basic (Static) parts: definitions, facts, concepts, entities")
print(f"  - 4 Dynamic (Relational) parts: relationships, processes, mechanisms, contexts")
print(f"  - All dynamic parts include source→target relinks")
