# Wiki Audit Report

## Executive Summary

This audit identified **critical structural issues** in the GitHub wiki that prevent proper navigation and create a fragmented user experience. The main problems are:

1. **123 broken wiki links** pointing to 44 non-existent pages
2. **10 high-priority missing pages** referenced 3+ times each
3. **11 orphaned files** not linked from anywhere
4. **Inconsistent link naming** between category titles and references

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Total markdown files | 31 |
| Total wiki links | 264 |
| Unique wiki links | 62 |
| **Broken links** | **123** |
| **Unique missing pages** | **44** |

---

## 🔴 Critical Issues: Missing High-Priority Pages

These pages are referenced in **3 or more files** and must be created:

### Category Pages (Most Critical)
1. **[[Classical Institutional Theory]]** - Referenced in **12 files**
   - Should link to `categories/classical-theory.md` (H1: "Category: Classical Institutional Theory")
   
2. **[[Core Concepts]]** - Referenced in **16 files**
   - Should link to `categories/core-concepts.md` (H1: "Category: Core Concepts")
   
3. **[[Digital Platforms as Empirical Stress Tests]]** - Referenced in **11 files**
   - Should link to `categories/digital-platforms.md` (H1: "Category: Digital Platforms as Empirical Stress Tests")
   
4. **[[New Empirical Foundation]]** - Referenced in **15 files**
   - Should link to `categories/new-foundation.md` (H1: "Category: New Empirical Foundation")

### Tier Pages (High Priority)
5. **[[Tier 1: Base Definitions]]** - Referenced in **8 files**
6. **[[Tier 2: Theoretical Scaffold]]** - Referenced in **5 files**
7. **[[Tier 3: Mathematical Operationalization]]** - Referenced in **9 files**

### Scholar Pages
8. **[[Douglass North]]** - Referenced in **3 files**
9. **[[W. Richard Scott]]** - Referenced in **3 files**
10. **[[Key Scholars and Works]]** - Referenced in **3 files**

---

## ⚠️ Structural Issues

### Orphaned Files (11 files not linked from anywhere)
These files exist but are not accessible through wiki navigation:

1. `categories/classical-theory.md`
2. `categories/digital-platforms.md`
3. `categories/new-foundation.md`
4. `concepts.md`
5. `contexts.md`
6. `definitions.md`
7. `entities.md`
8. `facts.md`
9. `mechanisms.md`
10. `processes.md`
11. `relationships.md`

### Root Cause Analysis

The primary issue is a **mismatch between link text and page titles**:

- Links use: `[[Classical Institutional Theory]]`
- Page H1 title: `# Category: Classical Institutional Theory`

Wiki software typically matches links to page titles exactly. The word "Category: " prefix breaks the link resolution.

---

## 📋 All Missing Pages by Category

### Category Pages (5)
- [[Classical Institutional Theory]]
- [[Core Concepts]]
- [[Digital Platforms as Empirical Stress Tests]]
- [[Digital platforms]] (lowercase variant)
- [[New Empirical Foundation]]

### Tier Pages (3)
- [[Tier 1: Base Definitions]]
- [[Tier 2: Theoretical Scaffold]]
- [[Tier 3: Mathematical Operationalization]]

### Scholar Pages (8)
- [[Anatol Rapoport]]
- [[Cornil and Hardisty 2025]]
- [[Douglass North]]
- [[Hodgson 2015]]
- [[Lambrecht and Tucker 2018]]
- [[North/Scott definitions]]
- [[Voigt 2018]]
- [[W. Richard Scott]]

### Application Pages (4)
- [[Behavioral Science Applications]]
- [[Product Management Applications]]
- [[Regulatory and Policy Applications]]
- [[Technology Company Accountability]]

### Concept Variations (6)
- [[Behavioral clusters]] (plural vs singular)
- [[Informational signals]] (plural vs singular)
- [[Institutional identification]]
- [[Institutions]]
- [[New informational signals]]
- [[Trajectory Clustering]]

### Other Missing Pages (18)
- [[Advertising bid structures]]
- [[Behavioral outcomes]]
- [[Cost-efficient targeting]]
- [[Demographic exclusion patterns]]
- [[Experimental bias]]
- [[Gender-differentiated information environments]]
- [[Key Scholars and Works]]
- [[Machine-learning algorithms]]
- [[Measurement crisis]]
- [[Platform algorithms]]
- [[Platform experiments]]
- [[Raw behavioral data]]
- [[Rules vs Equilibria Debate]]
- [[Stabilized behavioral patterns]]
- [[Stationarity Testing]]
- [[User exposure]]
- [[Wiki Links]]
- [[index.md]]

---

## 🔧 Recommended Fixes

### Priority 1: Fix Category Page Links

**Option A: Rename page H1 titles** (Recommended)
Remove "Category: " prefix from H1 titles in category files:
```markdown
# Category: Classical Institutional Theory
```
becomes:
```markdown
# Classical Institutional Theory
```

**Option B: Update all links**
Change all `[[Classical Institutional Theory]]` to `[[Category: Classical Institutional Theory]]`

### Priority 2: Create Missing Tier Pages

Create three new files:
- `wiki/tiers/base-definitions.md` with H1: `# Tier 1: Base Definitions`
- `wiki/tiers/theoretical-scaffold.md` with H1: `# Tier 2: Theoretical Scaffold`
- `wiki/tiers/mathematical-operationalization.md` with H1: `# Tier 3: Mathematical Operationalization`

### Priority 3: Create Scholar Pages

Create stub pages for key scholars referenced throughout the wiki.

### Priority 4: Fix Orphaned Files

Add links to orphaned files from `index.md` or relevant category pages.

### Priority 5: Standardize Naming

Choose either singular or plural forms consistently:
- Use "Behavioral Cluster" (singular) OR "Behavioral clusters" (plural)
- Use "Informational Signal" (singular) OR "Informational signals" (plural)

---

## 📁 Current File Structure

```
wiki/
├── README.md
├── index.md
├── concepts.md
├── contexts.md
├── definitions.md
├── entities.md
├── facts.md
├── mechanisms.md
├── processes.md
├── relationships.md
├── categories/
│   ├── classical-theory.md
│   ├── core-concepts.md
│   ├── digital-platforms.md
│   └── new-foundation.md
├── entries/
│   ├── ab-testing-illusion.md
│   ├── algorithmic-exclusion.md
│   ├── behavioral-cluster.md
│   ├── behavioral-spectrum.md
│   ├── behavioral-trajectory.md
│   ├── cluster-analysis-example.md
│   ├── conclusion.md
│   ├── informational-signal.md
│   ├── measurement-dead-end.md
│   ├── north-rules.md
│   ├── platform-architect.md
│   ├── rapoport-subjectivism.md
│   ├── reaction.md
│   ├── rules-to-clusters.md
│   ├── scott-pillars.md
│   ├── the-paradox.md
│   └── three-tier-architecture.md
```

---

## ✅ Verification Steps

After fixes are applied, verify:
1. No broken links remain (run link checker)
2. All files are reachable from index.md within 3 clicks
3. Consistent naming convention used throughout
4. All category pages properly linked

---

*Report generated: 2025*
