# Wikipedia Dataset Registry Entry

## Overview

Wikipedia provides structured data on collaborative knowledge production, governance processes, and community coordination at scale.

## Data Characteristics

- **Type**: Collaborative encyclopedia
- **Structure**: Articles, talk pages, edit histories, user contributions
- **Temporal**: Continuous since 2001
- **Access**: Public dumps, API, Quarry SQL interface

## Institutional Research Applications

- Governance policy evolution
- Dispute resolution mechanisms
- Norm enforcement patterns
- Collaborative institution building
- Administrative role emergence

## Schema Summary

```
Edit:
  - revision_id
  - page_id
  - user_id / ip
  - timestamp
  - comment
  - content_delta
  - size_change
  
Article:
  - page_id
  - title
  - namespace
  - creation_date
  
Talk:
  - page_id (talk namespace)
  - threaded discussions
  - signatures
```

## Access Notes

- Full dumps available monthly
- Real-time via RecentChanges feed
- API has rate limits
- Quarry for complex SQL queries

## Ethics Considerations

- Public data but user attribution
- Edit histories permanent
- Administrator identification possible
- Cross-wiki tracking considerations

## Related Benchmarks

- Policy change detection
- Edit war identification
- Governance intervention effects

---

*Registry entry for Institutional Design Lab*
