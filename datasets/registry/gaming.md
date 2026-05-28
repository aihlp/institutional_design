# Gaming Platforms Dataset Registry Entry

## Overview

Gaming platforms provide data on rule enforcement, community governance, and behavioral norms in structured interactive environments.

## Data Characteristics

- **Type**: Interactive gaming environments
- **Structure**: Matches, player profiles, chat logs, reports
- **Temporal**: Session-based with persistent histories
- **Access**: Varies by platform (API, research partnerships)

## Institutional Research Applications

- Rule enforcement mechanisms
- Player community norms
- Sanctioning systems
- Reputation dynamics
- Governance intervention effects

## Schema Summary

```
Match:
  - match_id
  - game_type
  - timestamp
  - duration
  - players[]
  - outcome
  
Player:
  - player_id
  - rank / skill_rating
  - reputation_score
  - sanction_history
  
Chat:
  - message_id
  - match_id / channel_id
  - author
  - timestamp
  - content
  - moderation_action
  
Report:
  - report_id
  - reporter
  - reported
  - reason
  - outcome
```

## Access Notes

- Platform-specific APIs
- Research partnership opportunities
- Public tournament data
- Third-party tracking sites

## Ethics Considerations

- Minor populations common
- Behavioral manipulation concerns
- Addiction-related sensitivities
- Cross-platform identification

## Related Benchmarks

- Norm violation detection
- Sanction effectiveness
- Community health metrics

---

*Registry entry for Institutional Design Lab*
