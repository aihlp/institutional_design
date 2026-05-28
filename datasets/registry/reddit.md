# Reddit Dataset Registry Entry

## Overview

Reddit provides rich behavioral traces from diverse online communities, making it valuable for studying institutional dynamics in digital platforms.

## Data Characteristics

- **Type**: Social media interactions
- **Structure**: Hierarchical (subreddits → posts → comments)
- **Temporal**: Continuous since 2005
- **Access**: Public API, pushshift archives

## Institutional Research Applications

- Community norm emergence
- Moderation policy effects
- Behavioral clustering by subreddit
- Information propagation patterns
- Governance mechanism comparisons

## Schema Summary

```
Submission:
  - id
  - subreddit
  - author
  - timestamp
  - title
  - content
  - score
  - upvote_ratio
  
Comment:
  - id
  - submission_id
  - author
  - timestamp
  - content
  - score
  - parent_id
```

## Access Notes

- API rate limits apply
- Historical data via pushshift (check current status)
- Some subreddits may have posting restrictions

## Ethics Considerations

- User privacy (pseudonymous but traceable)
- Content sensitivity (varies by subreddit)
- Researcher positionality
- Potential for re-identification

## Related Benchmarks

- Community stability measurement
- Norm detection accuracy
- Intervention effect estimation

---

*Registry entry for Institutional Design Lab*
