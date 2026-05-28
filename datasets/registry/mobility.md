# Mobility Data Dataset Registry Entry

## Overview

Urban mobility data provides insights into coordination mechanisms, infrastructure governance, and collective behavior in physical-digital systems.

## Data Characteristics

- **Type**: Transportation and movement
- **Structure**: Trip records, location traces, infrastructure usage
- **Temporal**: Continuous with temporal patterns
- **Access**: City open data, research partnerships, aggregated feeds

## Institutional Research Applications

- Infrastructure coordination
- Shared resource governance
- Norm emergence in new mobility
- Policy intervention effects
- Spatial behavioral clustering

## Schema Summary

```
Trip:
  - trip_id
  - start_location
  - end_location
  - start_time
  - end_time
  - mode
  - provider (if applicable)
  
Station/Zones:
  - id
  - location
  - capacity
  - utilization_timeseries
  
Policy:
  - policy_id
  - type (pricing, restriction, etc.)
  - geographic_scope
  - implementation_date
```

## Access Notes

- Highly variable by city
- Privacy restrictions common
- Aggregation requirements
- Licensing varies

## Ethics Considerations

- Location privacy critical
- Re-identification risks high
- Equity implications
- Surveillance concerns

## Related Benchmarks

- Policy effect detection
- Behavioral pattern stability
- Coordination mechanism analysis

---

*Registry entry for Institutional Design Lab*
