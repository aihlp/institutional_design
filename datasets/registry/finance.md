# Financial Markets Dataset Registry Entry

## Overview

Financial market data provides insights into formal institutional structures, regulatory effects, and coordination mechanisms in highly regulated environments.

## Data Characteristics

- **Type**: Market transactions, prices, regulatory filings
- **Structure**: Time series, order books, corporate disclosures
- **Temporal**: Continuous during trading hours, periodic filings
- **Access**: Public exchanges, regulatory databases, commercial providers

## Institutional Research Applications

- Regulatory regime effects
- Market norm emergence
- Coordination under formal rules
- Information propagation
- Crisis dynamics and stability

## Schema Summary

```
Transaction:
  - transaction_id
  - asset_id
  - timestamp
  - price
  - volume
  - venue
  
OrderBook:
  - asset_id
  - timestamp
  - bids[]
  - asks[]
  
Filing:
  - filing_id
  - entity_id
  - type (10-K, 8-K, etc.)
  - date
  - content
  
Regulatory:
  - rule_id
  - jurisdiction
  - effective_date
  - scope
```

## Access Notes

- Exchange-specific formats
- Delayed vs real-time access
- Regulatory databases (SEC EDGAR, etc.)
- Commercial data licensing

## Ethics Considerations

- Market manipulation risks
- Insider information handling
- Systemic stability concerns
- unequal access implications

## Related Benchmarks

- Regulatory change detection
- Market stability metrics
- Information asymmetry measurement

---

*Registry entry for Institutional Design Lab*
