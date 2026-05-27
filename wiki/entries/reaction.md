# Reaction

## Definition

**A reaction is a discrete, logged action or inaction by an agent in response to an informational signal.**

## Role in the Framework

Reactions are the **Tier 1 primitives** that:
- Compose behavioral trajectories (sequences of reactions)
- Form behavioral spectra (distributions of reactions)
- Enable cluster identification (groupings of similar reaction patterns)

## Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Discrete** | Individually identifiable event |
| **Logged** | Recorded in platform data systems |
| **Observable** | No inference about mental states required |
| **Binary nature** | Can be action OR inaction (both are informative) |
| **Signal-linked** | Associated with preceding signal |

## Action vs. Inaction

Both actions and inactions are valid reactions:

### Actions (Explicit Reactions)
| Action Type | Examples |
|-------------|----------|
| **Click/Tap** | Clicking link, tapping button |
| **Navigation** | Scrolling, page transition, tab switch |
| **Input** | Typing, voice command, form submission |
| **Purchase** | Adding to cart, checkout completion |
| **Social** | Liking, sharing, commenting, following |
| **Configuration** | Changing settings, toggling options |

### Inactions (Implicit Reactions)
| Inaction Type | Examples |
|---------------|----------|
| **Non-open** | Notification delivered but not opened |
| **Scroll-past** | Content displayed but scrolled past without engagement |
| **Abandonment** | Process started but not completed |
| **Ignore** | Signal received, no observable response within time window |
| **Dismissal** | Explicit rejection (swipe away, close, hide) |

**Critical insight**: Inaction is itself a behavioral signal that carries information about agent state and preferences.

## Formal Specification

```
Reaction R:
  R = {
    id: unique_identifier,
    timestamp: ISO8601_datetime,
    agent_id: user_identifier,
    signal_id: reference_to_triggering_signal,
    reaction_type: taxonomy_category,
    reaction_value: quantitative_measure (optional),
    context: {
      device: device_info,
      location: geo_data (if available),
      session: session_id,
      state: application_state
    },
    latency_ms: time_from_signal_to_reaction (optional)
  }
```

## Example: Social Media Platform

```json
{
  "id": "react_7f8e9d0c1b2a",
  "timestamp": "2025-01-15T14:32:07.234Z",
  "agent_id": "user_482910",
  "signal_id": "sig_post_5a6b7c8d",
  "reaction_type": "scroll_past",
  "reaction_value": null,
  "context": {
    "device": "iPhone_14_Pro",
    "location": null,
    "session": "sess_abc123xyz",
    "state": "feed_browsing"
  },
  "latency_ms": 847
}
```

## Reaction Taxonomy

### By Engagement Level

| Level | Description | Examples |
|-------|-------------|----------|
| **Passive** | Minimal engagement | Impression, view (dwell < threshold) |
| **Active** | Intentional engagement | Click, tap, scroll |
| **Committed** | High-effort engagement | Purchase, signup, content creation |
| **Social** | Interpersonal engagement | Share, comment, tag, mention |

### By Valence

| Valence | Description | Examples |
|---------|-------------|----------|
| **Positive** | Affirming response | Like, upvote, purchase, subscribe |
| **Negative** | Rejecting response | Dislike, downvote, hide, unsubscribe |
| **Neutral** | Informational response | Click-through, view, navigate |
| **Ambiguous** | Unclear valence | Quick click-and-back, partial completion |

### By Temporal Pattern

| Pattern | Description | Examples |
|---------|-------------|----------|
| **Immediate** | Within seconds of signal | Push notification open |
| **Delayed** | Minutes to hours later | Email opened next day |
| **Deferred** | Days later, possibly via different channel | Ad seen on mobile, purchased on desktop |
| **Absent** | No reaction within observation window | Ignored notification |

## Relationship to Other Primitives

```
INFORMATIONAL SIGNAL
        ↓ (triggers)
   REACTION ← This entry
        ↓ (sequences of)
BEHAVIORAL TRAJECTORY
        ↓ (aggregated into)
 BEHAVIORAL SPECTRUM
        ↓ (clustered into)
 BEHAVIORAL CLUSTER
```

## Measurement Requirements

To properly track reactions:

1. **Event logging infrastructure**
   - Capture all user interactions
   - Include inaction timeouts (e.g., "no response after 24hr")

2. **Signal-reaction linkage**
   - Each reaction references triggering signal
   - Enables causal chain reconstruction

3. **Temporal precision**
   - Millisecond timestamps for latency analysis
   - Enables fine-grained pattern detection

4. **Context capture**
   - Device, location, session state
   - Enables stratified analysis

5. **Taxonomy consistency**
   - Standardized reaction categories
   - Enables cross-study comparison

## Analytical Uses

### Reaction Rate Analysis
- What percentage of signals produce reactions?
- Which signal types have highest/lowest engagement?

### Latency Distribution
- How quickly do users typically respond?
- Do latency patterns vary by signal type or user segment?

### Reaction Sequences
- What reactions tend to follow each other?
- Can we identify common reaction chains?

### Conversion Funnels
- What is the drop-off at each step?
- Where do users abandon processes?

### A/B Test Outcomes
- Do reaction distributions differ between variants?
- Is one variant producing more desirable reactions?

## Contrast with Classical Concepts

| Classical Concept | Reaction |
|-------------------|----------|
| Behavior (aggregate, inferred) | Reaction (discrete, observed) |
| Choice (requires preference inference) | Reaction (directly logged) |
| Compliance (normative judgment) | Reaction (descriptive record) |
| Utility-maximizing action | Action or inaction (no assumption) |

## Related Entries

- [[Informational Signal]] - What triggers reactions
- [[Behavioral Trajectory]] - Sequences of reactions
- [[Behavioral Spectrum]] - Distributions of reactions
- [[Tier 1: Base Definitions]] - Foundational layer
- [[From Rules to Behavioral Clusters]] - Core framework proposal

## Categories

[[Core Concepts]], [[New Empirical Foundation]]
