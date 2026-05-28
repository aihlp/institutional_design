# GitHub Dataset Registry Entry

## Overview

GitHub provides data on software collaboration, governance through code review, and institutional structures in technical communities.

## Data Characteristics

- **Type**: Software development platform
- **Structure**: Repositories, issues, pull requests, discussions
- **Temporal**: Continuous since 2008
- **Access**: Public API, GH Archive, BigQuery public dataset

## Institutional Research Applications

- Code review norms
- Contribution governance
- Maintainer role emergence
- Project forking as exit mechanism
- Technical decision-making processes

## Schema Summary

```
Repository:
  - id
  - owner
  - name
  - created_at
  - visibility
  
PullRequest:
  - id
  - repository_id
  - author
  - created_at
  - merged (bool)
  - reviewers
  - comments_count
  
Issue:
  - id
  - repository_id
  - author
  - created_at
  - labels
  - state
  
Commit:
  - sha
  - repository_id
  - author
  - committer
  - timestamp
```

## Access Notes

- API rate limits (5000/hr authenticated)
- GH Archive for historical events
- BigQuery for large-scale analysis
- GraphQL API for complex queries

## Ethics Considerations

- Public but professional context
- Contributor attribution expected
- Corporate vs individual contributions
- Sensitive project information

## Related Benchmarks

- Governance model classification
- Contribution pattern stability
- Norm enforcement detection

---

*Registry entry for Institutional Design Lab*
