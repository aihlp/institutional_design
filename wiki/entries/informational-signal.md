# Informational Signal

## Definition

**An informational signal is any objectively recordable change in the information environment—a timestamped event with a source and a type.**

## Role in the Framework

Informational signals are the **Tier 1 primitives** that initiate behavioral trajectories. They are:
- The "stimulus" to which agents react
- The anchor point for tracking behavioral patterns
- The identifiable cause in signal-reaction chains

## Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Objectively recordable** | Can be logged without interpretation |
| **Timestamped** | Precise temporal location |
| **Typed** | Classified by signal category |
| **Sourced** | Attributed to originating entity |
| **Identifiable** | Unique ID or fingerprint |

## Signal Taxonomy

### By Source

| Source Type | Examples |
|-------------|----------|
| **Platform-generated** | Push notifications, algorithmic feeds, UI changes, A/B test variants |
| **User-generated** | Posts, comments, messages, shares, reactions |
| **System-generated** | Error messages, status updates, maintenance notices |
| **External** | Ads from third parties, embedded content, API callbacks |

### By Type

| Type | Description | Example |
|------|-------------|---------|
| **Notification** | Direct alert to user | Push notification, email, in-app badge |
| **Content** | Informational material | Post, article, video, image |
| **Interface** | UI element or change | Button, menu, layout modification |
| **Policy** | Rule or constraint announcement | Terms update, community guideline |
| **Transactional** | Commerce-related | Price change, order confirmation, receipt |
| **Social** | Interpersonal signal | Friend request, mention, tag |

### By Intent

| Intent | Description |
|--------|-------------|
| **Explicit** | Deliberately sent to elicit response (marketing notification) |
| **Implicit** | Byproduct of system operation (feed update) |
| **Incidental** | Unintended consequence (algorithmic exclusion pattern) |

## Formal Specification

```
Signal S:
  S = {
    id: unique_identifier,
    timestamp: ISO8601_datetime,
    source: {type, entity_id},
    signal_type: taxonomy_category,
    content: {content_id, content_hash},
    targeting: {criteria, population_spec},
    delivery_channel: channel_type,
    metadata: {key: value pairs}
  }
```

## Example: E-commerce Notification

```json
{
  "id": "sig_9a8b7c6d5e4f",
  "timestamp": "2025-01-15T09:23:14.000Z",
  "source": {
    "type": "platform",
    "entity_id": "recommendation_engine_v3"
  },
  "signal_type": "notification",
  "content": {
    "content_id": "promo_flash_sale_jan15",
    "content_hash": "sha256:abc123..."
  },
  "targeting": {
    "criteria": ["active_last_7_days", "category_electronics"],
    "population_spec": "users_who_viewed_headphones"
  },
  "delivery_channel": "push_notification",
  "metadata": {
    "campaign_id": "winter_sale_2025",
    "ab_test_variant": "B",
    "priority": "high"
  }
}
```

## Relationship to Other Primitives

```
INFORMATIONAL SIGNAL
        ↓ (agent perceives and reacts)
   REACTION
        ↓ (accumulated over time)
BEHAVIORAL TRAJECTORY
        ↓ (grouped with similar trajectories)
 BEHAVIORAL CLUSTER
        ↓ (stable cluster = institution)
   INSTITUTION
```

## Measurement Requirements

To properly track informational signals:

1. **Unique identification**
   - Every signal gets persistent ID
   - Enables tracking across systems

2. **Temporal precision**
   - Millisecond timestamps recommended
   - Enables fine-grained trajectory analysis

3. **Source attribution**
   - Which system/entity generated the signal
   - Enables accountability analysis

4. **Type classification**
   - Consistent taxonomy across signals
   - Enables comparative analysis

5. **Delivery logging**
   - Which users received which signals
   - Enables exposure measurement

## Analytical Uses

### Signal Exposure Analysis
- Who saw what, when?
- Was delivery uniform or targeted?

### Signal-Response Mapping
- Which signals produce which reactions?
- What is the response distribution (spectrum)?

### Signal Clustering
- Do certain signal types produce similar behavioral patterns?
- Can we classify signals by behavioral impact?

### Institutional Genealogy
- What signals preceded cluster formation?
- Which signals maintain cluster stability?

## Contrast with Classical Concepts

| Classical Concept | Informational Signal |
|-------------------|---------------------|
| Rule (abstract constraint) | Signal (concrete event) |
| Norm (shared expectation) | Signal (observable occurrence) |
| Incentive structure (latent) | Signal (logged timestamp) |
| Assumed to exist | Recorded as data |

## Related Entries

- [[Reaction]] - Agent response to signal
- [[Behavioral Trajectory]] - Sequence of signal-reaction pairs
- [[Behavioral Spectrum]] - Distribution of reactions to signal
- [[Tier 1: Base Definitions]] - Foundational layer
- [[A/B Testing Illusion]] - Signal/filter entanglement problem
- [[Algorithmic Exclusion]] - Signals unequally distributed

## Categories

[[Core Concepts]], [[New Empirical Foundation]]
