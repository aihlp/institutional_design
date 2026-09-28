# Behavioral Institutionalism of the Agent-to-Agent (A2A) Economy: The A2A Institutional Dynamics Standard (A2A-IDS)

**Author:** Dr. V. Dyachkov  
**Affiliation:** Computational Institutional Economics & Multi-Agent Systems Laboratory  
**Correspondence:** `itinai.com@gmail.com` · SSRN Author ID: 6742298  
**Status:** Protocol-Verified Specification & Empirical Validation  
**Conformance:** Google Agent-to-Agent (A2A) Protocol v1.0.1, Anthropic Model Context Protocol (MCP), IETF RFC 8785 (JCS), RFC 7515 (JWS)  
**Live Publication:** [https://aihlp.github.io/institutional_design/](https://aihlp.github.io/institutional_design/)  
**Download PDF (SSRN):** [https://aihlp.github.io/institutional_design/a2a_institutional_dynamics_ssrn.pdf](https://aihlp.github.io/institutional_design/a2a_institutional_dynamics_ssrn.pdf)

---

## Executive Abstract

The emerging Agent-to-Agent (A2A) protocol specification establishes syntactic interoperability across heterogeneous software agents via standardized discovery manifests (`/.well-known/agent-card.json`), JSON-RPC 2.0 message framing (`message/send`, `message/stream`), and a deterministic Task lifecycle (`SUBMITTED` → `WORKING` → `COMPLETED` / `INPUT_REQUIRED` / `FAILED` / `CANCELED`). Concurrently, the Model Context Protocol (MCP) standardizes execution filters via client-server tool, prompt, and resource binding. However, syntactic conformance to these grammars provides no guarantee of institutional stability, service-level veracity, or multi-agent equilibrium.

This paper formulates and empirically substantiates the **A2A Institutional Dynamics Standard (A2A-IDS)**. We operationalize behavioral-institutional economics through seven protocol primitives, four informational field parameters, and a computable metric of *Institutional Anomie* ($A_{\text{hub}}$) defined as the Total Variation Distance between declared AgentCard capabilities and empirical log-derived execution clusters. In an empirical testbed of 500,000 tasks across 128 heterogeneous LLM agents, we validate econometric stationarity testing (ADF/KPSS) and Markov-chain spectral gap analysis ($\tau_{\text{rel}} = \frac{1}{1 - |\lambda_2|}$), proving that sustained anomie ($A_{\text{hub}} > 0.30$) predicts cascading orchestration failures with an ROC-AUC of 0.912. We establish statistical justifications and ROC sensitivity analyses for all governance thresholds, develop tamper-evident cryptographic telemetry defenses against Goodhart's Law manipulation, and prove that the monitoring stack operates in $O(K)$ streaming time, adding less than 1.2% computational overhead.

---

## 1. Introduction

### 1.1. Relevance and Problem Statement

The Agent-to-Agent (A2A) protocol specification (Google, 2025; Linux Foundation, 2025) establishes syntactic interoperability among heterogeneous software agents through standardized discovery manifests (`/.well-known/agent-card.json`), JSON-RPC 2.0 transport methods (`message/send`, `message/stream`), and a deterministic Task lifecycle (`SUBMITTED` → `WORKING` → `COMPLETED` / `FAILED` / `INPUT_REQUIRED` / `CANCELED`). However, this syntactic layer provides no instrument for assessing the evolutionary resilience of multi-agent environments. Three structural deficiencies motivate the present study:

First, the specification treats agents as opaque execution units. A routing hub or client agent can inspect declared interface signatures but cannot audit internal neural weights, system prompts, or routing heuristics. Consequently, conformance to protocol grammar does not entail conformance to declared service-level agreements (SLAs), generating an unmeasured gap between normative declarations and executed behavior.

Second, without a telemetry-based measurement apparatus, A2A hubs accumulate latent anomalies—*capability cloaking* (inflated `AgentSkill` declarations in the AgentCard), *cyclic task delegation* (Cycle Overflow across unmonitored agent chains), and *parasitic state retention* (Task Flooding via persistent `INPUT_REQUIRED` loops)—that degrade orchestration throughput below detectable thresholds until cascading orchestration failure occurs.

Third, the Model Context Protocol (MCP; Anthropic, 2024) and emerging micropayment standards (HTTP 402 / x402) introduce additional execution surfaces whose institutional stability remains unquantified in literature on multi-agent systems (MAS), distributed AI governance, and digital institutional economics.

These deficiencies position the A2A hub not merely as a message router, but as an institutional environment whose health requires continuous, mathematically grounded diagnostics.

### 1.2. Conceptual–Categorical Apparatus

1. **Informational Signal ($S$):** Any objectively logged event in the hub carrying source identifier, carrier protocol, formal encoding type, and UTC timestamp. In the A2A stack: AgentCard publications, `message/send` JSON-RPC payloads, Task state transitions, and `x402` payment negotiation headers.
2. **Algorithmic Perception Filter ($F$):** The deterministic or stochastic configuration of a receiving agent that decodes $S$ into an internal context: system instructions, context-window limits, attached MCP tools (`tools/list`), token budget, authentication profiles (`securitySchemes`), and foundational model parameters.
3. **Stimulus ($\sigma$):** The structured token context assembled in prompt memory after $S$ passes through $F$, defined as $\sigma = F(S)$. $\sigma$ contains no anthropomorphic affective component.
4. **Reaction ($R$):** An atomic, individually logged action or inaction: a Task state transition, emission of a content part (`TextPart`, `DataPart`, `FilePart`), invocation of an external MCP tool via `tools/call`, an `x402` micropayment transaction, or connection timeout.
5. **Behavioral Pattern ($\Pi$):** A reproducible, autocorrelated sequence of reactions exhibited by an agent or cohort under recurrent signal classes ($r > 0.7$ at lag 1, verified via Ljung-Box test, $p < 0.01$).
6. **Stationarity ($\Sigma$):** The statistical property that the distribution of reactions preserves its first two moments over successive observation windows $W_t$, confirmed by Augmented Dickey–Fuller (ADF) and KPSS tests under the condition $\mathrm{TVD}(P_t, P_{t+1}) < 0.05$.
7. **Behavioral Spectrum ($K_{\text{spec}}$):** The cardinality of distinct, viable behavioral clusters ($K \ge 3$) emerging in an agent population for a given task class, operationalizing Ashby's (1956) Law of Requisite Variety.
8. **Institutional Anomie ($A_{\text{hub}}$):** The Total Variation Distance between the normative distribution $Y$ (declared in AgentCards and SLAs) and the empirical behavioral distribution $X$ (extracted from logs via unsupervised clustering):
   $$A_{\text{hub}} = \mathrm{TVD}(Y, X) = \frac{1}{2}\sum_{i=1}^{K} |y_i - x_i|$$
9. **Agent-as-Proxy:** Every agent is an algorithmic executor of a human or organizational principal. The filter encodes the principal's constraints, budget limits, and risk policies.
10. **Informational Field Parameters:** Four physically measurable quantities: signal density $D_{\text{hub}}$, propagation speed $V_{\text{prop}}$, access asymmetry $A_{\text{access}}$ (Gini coefficient over message throughput), and Shannon entropy $H_{\text{hub}}$.

### 1.3. Formal Hypotheses

- **H1 (Anomie–Fragility Linkage):** If $A_{\text{hub}} > 0.30$ is sustained over three consecutive observation windows, the empirical probability of a cascading orchestration failure within the subsequent window exceeds $0.70$, controlling for task volume.
- **H2 (Spectral Compression under Asymmetry):** An increase in access asymmetry ($\mathrm{Gini}_{\text{msg}} \to 1$) produces a statistically significant reduction in $K_{\text{spec}}$ (monoculture collapse), verified by negative rank correlation ($\rho < -0.60$, $p < 0.01$).
- **H3 (Markov Convergence Criterion):** The hub reaches a stationary institutional equilibrium if and only if the second-largest eigenvalue modulus of the $K \times K$ Markov transition matrix satisfies $|\lambda_2| < 0.85$, yielding a finite relaxation time $\tau_{\text{rel}} = \frac{1}{1 - |\lambda_2|}$.
- **H4 (Autonomization Persistence):** Once a behavioral pattern achieves an autonomization score $K_{\text{aut}} > 0.80$, removal or modification of the originating hub signal does not dissolve the pattern within two subsequent observation windows, demonstrating institutional inertia.

---

## 2. Projection of Seven Behavioral Primitives onto the A2A / MCP Architectural Stack

| Behavioral Primitive | Formal Definition | A2A / MCP Protocol Mapping | Telemetry Key |
| :--- | :--- | :--- | :--- |
| **1. Signal ($S$)** | Logged event with source, protocol carrier, type, and timestamp | `/.well-known/agent-card.json`; `message/send` JSON-RPC; Task state events; `x402` payment headers | `a2a.signal.id`, `event.timestamp_utc` |
| **2. Filter ($F$)** | Agent configuration decoding $S$ into execution memory | System prompt; context capacity; MCP tools (`tools/list`); `securitySchemes` (RFC 7515 / 8785); model weights | `mcp.tools_hash`, `agent.context_capacity` |
| **3. Stimulus ($\sigma$)** | Structured token context assembled in prompt memory | Tokenized context assembly $\sigma = F(S)$ prior to model inference | Inferred via prompt token count |
| **4. Reaction ($R$)** | Atomic logged action or inaction | Task state transition; Part payload (`DataPart`, `FilePart`); MCP `tools/call`; timeout | `task.state`, `mcp.tool_call.name`, `response.latency_ms` |
| **5. Pattern ($\Pi$)** | Autocorrelated sequence of recurrent reactions ($r > 0.7$) | Canonical task execution chains; repeated `INPUT_REQUIRED` loops; multi-hop delegation chains | `trajectory.ngram_hash`, `autocorr.rho` |
| **6. Stationarity ($\Sigma$)** | Invariance of first two moments across windows $W_t$ | ADF unit-root rejection ($p < 0.05$) and KPSS failure to reject; $\mathrm{TVD}(P_t, P_{t+1}) < 0.05$ | `stats.adf_pvalue`, `stats.tvd_delta` |
| **7. Spectrum ($K_{\text{spec}}$)** | Set of viable behavioral clusters for a task class | HDBSCAN clustering on task vectors; count of clusters with share $p_i \ge 0.05$ | `hdbscan.cluster_count`, `k_spec.cardinality` |

---

## 3. The A2A Hub as an Informational Field: Four Measurable Parameters

1. **Signal Density ($D_{\text{hub}}$):** The arrival rate of protocol events relative to agent processing bandwidth. High density triggers context saturation, forcing agents into token evasion or dropped connections.
2. **Propagation Speed ($V_{\text{prop}}$):** Time-to-First-Message (TTFM). Fast lightweight agents exploit the *fait accompli* advantage, locking in routing topologies before deeper reasoning models evaluate filters (Lieberman & Montgomery, 1988).
3. **Access Asymmetry ($A_{\text{access}}$):** Quantified via $\mathrm{Gini}_{\text{msg}}$ across outbound message volumes. Concentrated broadcast power causes severe spectral compression ($K_{\text{spec}} \to 1$).
4. **Informational Field Entropy ($H_{\text{hub}}$):** Shannon entropy of reaction-type distributions. Low entropy indicates standardized execution; high entropy signals malformed payloads and cyclic failure.

---

## 4. Four Coexisting Institutional Regimes as Hybrid Configurations

- **Regime H2H (Human-to-Human):** A2A protocol acts as structured workflow router between human nodes publishing personal AgentCards.
- **Regime H2A (Human-to-Agent):** Human principal initiates intent; agent executes with MCP tools, escalating via `INPUT_REQUIRED`.
- **Regime A2H (Agent-to-Human):** Agent hits uncertainty or financial limits and invokes human oversight via `INPUT_REQUIRED` or `AUTH_REQUIRED`.
- **Regime A2A (Agent-to-Agent):** Autonomous closed-loop interaction over `message/send` and `x402` payment rails.

---

## 5. A2A Anomie: The Measurable Gap Between Declaration and Behavior

Institutional anomie is computed as the Total Variation Distance between the normative declaration vector $Y$ and empirical cluster vector $X$:
$$A_{\text{hub}} = \mathrm{TVD}(Y, X) = \frac{1}{2} \sum_{i=1}^{K} |y_i - x_i|$$

### 5.4. Statistical Calibration & ROC Sensitivity Analysis of Diagnostic Thresholds

To statistically justify the selection of $A_{\text{hub}} = 0.10$ and $A_{\text{hub}} = 0.30$, we conducted an empirical Receiver Operating Characteristic (ROC) sensitivity analysis across 50,000 sliding observation windows evaluating binary prediction of cascading orchestration failure:

| Candidate Threshold $\theta$ | Sensitivity (TPR) | False Positive Rate (FPR) | Precision | $F_1$-Score | Youden's $J$ Index |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $\theta = 0.10$ (Nominal Warning) | 0.982 | 0.314 | 0.542 | 0.698 | 0.668 |
| $\theta = 0.20$ | 0.941 | 0.176 | 0.702 | 0.804 | 0.765 |
| **$\theta = 0.30$ (Circuit Breaker)** | **0.894** | **0.071** | **0.841** | **0.867** | **0.823** |
| $\theta = 0.40$ | 0.682 | 0.024 | 0.912 | 0.780 | 0.658 |
| $\theta = 0.50$ | 0.431 | 0.008 | 0.954 | 0.594 | 0.423 |

Youden's $J$ index peaks at $\theta = 0.30$ ($J = 0.823$), minimizing Bayes classification risk.

### 5.6. Goodhart's Law & Adversarial Robustness of Telemetry

To prevent gaming of telemetry under Goodhart's Law, A2A-IDS enforces three layers of defense:
1. **Hub-Side Independent Wire-Tap Telemetry:** Network timestamps, byte volumes, and HTTP status codes are recorded passively at the TLS reverse-proxy level; client-submitted timestamps are discarded.
2. **Tamper-Evident Merkle Nonce Chains (RFC 7515 / 8785):** Every message requires a sender-signed nonce verified against public keys registered in the AgentCard. State changes are committed to a tamper-evident Merkle hash chain requiring reciprocal signing.
3. **Distributional Entropy & Benford Auditing:** Fabricated or synthetically smoothed logs exhibit anomalous statistical uniformity ($\nabla H_{\text{hub}} \to 0$ and failure of Benford mantissa distributions), triggering immediate provenance rejection.

---

## 6. Empirical Validation and Experimental Results

We deployed an empirical testbed comprising $N = 128$ autonomous agents (Gemini 1.5, Claude 3.5, GPT-4o, Llama 3 70B) executing 500,000 tasks across four enterprise domains over a 14-day evaluation period ($N_{\text{windows}} = 336$ at $\Delta t = 1\text{ hour}$).

### 6.1. Validation of Hypothesis 1 (Anomie–Fragility Linkage)

| Institutional Regime / Anomie State | Observed Windows ($N$) | Cascading Failures | Empirical Cascade Probability | Mean Downstream Error Rate |
| :--- | :--- | :--- | :--- | :--- |
| Nominal ($A_{\text{hub}} < 0.10$) | 218 | 1 | 0.0046 | 1.2% |
| Spectral Expansion ($0.10 \le A_{\text{hub}} \le 0.30$) | 76 | 4 | 0.0526 | 6.8% |
| **Fragility Zone ($A_{\text{hub}} > 0.30$, Sustained)** | **42** | **37** | **0.8810** | **38.4%** |

In 42 episodes of sustained $A_{\text{hub}} > 0.30$, 37 resulted in cascading failure, yielding $\hat{P}(\text{Cascade} \mid A_{\text{hub}} > 0.30) = 0.881 \pm 0.049$, confirming **H1** ($p < 0.001$, ROC-AUC = 0.912).

### 6.2. Validation of Hypothesis 2 (Spectral Compression)
Spearman rank correlation between broadcast concentration $\mathrm{Gini}_{\text{msg}}$ and spectral width $K_{\text{spec}}$ was $\rho = -0.734$ ($p = 0.0004$), confirming that monopolistic broadcast reduces response diversity, validating **H2**.

### 6.3. Validation of Hypothesis 3 (Markov Convergence Criterion)

| Operating Regime | $|\lambda_2|$ Modulus | $\tau_{\text{rel}}$ (Windows) | ADF Stat ($\tau$) | KPSS Stat | Institutional Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Equilibrium (Nominal)** | **0.762** | **4.20** | -4.18 ($p = 0.0012$) | 0.182 ($p > 0.10$) | Stationary digital institution certified |
| Schema Migration Shift | 0.892 | 9.26 | -2.41 ($p = 0.1420$) | 0.541 ($p < 0.05$) | Metastable drift; active transition |
| **Cycle Overflow Attack** | **0.984** | **62.50** | -1.12 ($p = 0.7080$) | 1.240 ($p < 0.01$) | Non-stationary; infinite cycle collapse |

Nominal operation maintained $|\lambda_2| = 0.762 < 0.85$ and passed ADF/KPSS joint stationarity testing. During an induced Cycle Overflow attack, $|\lambda_2| \to 0.984$, relaxation time diverged to 62.5 hours, confirming **H3**.

### 6.4. Validation of Hypothesis 4 (Autonomization Persistence)
Under controlled signal perturbation experiments, cooperating agent cohorts retained $K_{\text{aut}} = 0.838 \pm 0.042$ of established routing edges across two consecutive windows, confirming **H4**.

---

## 7. Hub Stability: The Measurement Protocol

1. **Sliding Windows:** Discretizing telemetry into observation windows $W_t$.
2. **Inter-Window TVD Drift:** Enforcing $\mathrm{TVD}(P_t, P_{t+1}) < 0.05$.
3. **Econometric Stationarity Testing:** Augmented Dickey–Fuller (rejecting unit root) and KPSS (failing to reject stationarity).
4. **Markov Spectral Gap:** Tracking relaxation time $\tau_{\text{rel}} \approx \frac{1}{1 - |\lambda_2|}$.

---

## 8. Measurable Institutional Gaps of the A2A Hub

- **Economic Vacuum:** Resolved via integration with HTTP 402 / `x402` micropayment negotiation headers.
- **Opaque Execution & Accountability Gap:** Mitigated via zero-knowledge execution traces.
- **Human-in-the-Loop Safeguards:** `INPUT_REQUIRED` and `AUTH_REQUIRED` represent native, deliberate institutional safety return-of-control gates.

---

## 9. Hub Architecture and Computational Complexity Analysis

### 9.1. Five Functional Layers
1. **Discovery & Identity:** `/.well-known/agent-card.json`, RFC 8785 JCS, RFC 7515 JWS.
2. **Authorization & Escrow:** CAAM policies, `x402` micropayment escrow.
3. **Task Orchestration:** Extended 8-state lifecycle: `SUBMITTED → WORKING → [DELEGATED | INPUT_REQUIRED | AUTH_REQUIRED] → [COMPLETED | FAILED | CANCELED]`.
4. **Human Escalation:** Operator risk dashboards for interrupted states.
5. **Institutional Telemetry & Audit:** Continuous computation of derived metrics.

### 9.2. Five Novel Telemetry Metrics
1. `spectrum_width` ($K_{\text{spec}}$)
2. `anomie_index` ($A_{\text{hub}}$)
3. `stability_tvd` ($\mathrm{TVD}_{\Delta t}$)
4. `autonomization_score` ($K_{\text{aut}}$)
5. `filter_feedback_rate` ($\Phi_{\text{feed}}$)

### 9.3. Computational Complexity and Streaming Scalability
A2A-IDS decouples runtime monitoring from agent population size $N$:
- **State Space Reduction ($K \ll N$):** Clustering and transition matrices operate on behavioral archetypes ($K \in [3, 20]$), *not* raw agents ($N \approx 10^3 - 10^5$). Matrix operations on $K \times K$ take $<0.15\text{ ms}$ on a single core.
- **Online Power Iteration for $\lambda_2$:** The second eigenvalue is tracked incrementally in $O(K)$ time per state transition via Rayleigh quotient deflation against $\pi$:
  $$v^{(m+1)} = \frac{(P - \mathbf{1}\pi^T)v^{(m)}}{\|(P - \mathbf{1}\pi^T)v^{(m)}\|}$$
- **Benchmarked Overhead:** CPU overhead remained $<1.2\%$ and memory footprint $<65\text{ MB}$ across our 500,000-task benchmark.

---

## 10. Conclusions and Synthesis of Findings

The A2A Institutional Dynamics Standard (A2A-IDS) transforms the A2A routing hub from a syntactic message switch into an active, self-diagnosing institutional environment. By coupling field parameters, multi-regime orchestration, Total Variation Distance anomie auditing, tamper-evident telemetry defenses against Goodhart's Law, and $O(K)$ streaming complexity, operators gain an objective mathematical apparatus for preempting multi-agent cascading failures.

---

## References

1. Akerlof, G. A. (1970). The market for "lemons": Quality uncertainty and the market mechanism. *Quarterly Journal of Economics*, 84(3), 488–500.
2. Anthropic. (2024). *Model Context Protocol (MCP) Specification*. https://modelcontextprotocol.io
3. Arrow, K. J. (1985). The economics of agency. In *Principals and Agents: The Structure of Business* (pp. 37–51). Harvard Business School Press.
4. Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
5. Campello, R. J. G. B., Moulawi, D., & Sander, J. (2013). Density-based clustering based on hierarchical density estimates. *PAKDD 2013*, LNCS 7819, 160–172.
6. Chrystal, K. A., & Mizen, P. D. (2003). Goodhart's Law: Its origins, meaning and implications for monetary policy. In *Central Banking, Monetary Theory and Practice* (pp. 221–240). Edward Elgar.
7. Cowgill, B., & Tucker, C. E. (2020). Algorithmic fairness and governance. *Journal of Economic Perspectives*, 34(2), 61–78.
8. Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *JASA*, 74(366), 427–431.
9. Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. *JEP: General*, 144(1), 114–126.
10. Dietvorst, B. J., Simmons, J. P., & Massey, C. (2018). Overcoming algorithm aversion. *Management Science*, 64(3), 1155–1170.
11. Durkheim, É. (1897). *Le suicide: Étude de sociologie*. Félix Alcan.
12. Dyachkov, V. (2026a-g). Research series on Behavioral Institutionalism and Digital Institutional Design. SSRN / ResearchGate.
13. Goodhart, C. A. E. (1975). Problems of monetary management: The UK experience. In *Papers in Monetary Economics*. Reserve Bank of Australia.
14. Google. (2025). *Agent-to-Agent (A2A) Protocol Specification v1.0.1*. Linux Foundation. https://github.com/google/A2A
15. Huberman, B. A., & Hogg, T. (1988). The behavior of computational ecosystems. *The Ecology of Computation*, 77–115.
16. Kwiatkowski, D., et al. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root. *Journal of Econometrics*, 54(1–3), 159–178.
17. Levin, D. A., Peres, Y., & Wilmer, E. L. (2009). *Markov Chains and Mixing Times*. AMS.
18. Lieberman, M. B., & Montgomery, D. B. (1988). First-mover advantages. *Strategic Management Journal*, 9(S1), 41–58.
19. Lin, J. (1991). Divergence measures based on the Shannon entropy. *IEEE Transactions on Information Theory*, 37(1), 145–151.
20. Merton, R. K. (1938). Social structure and anomie. *American Sociological Review*, 3(5), 672–682.
21. Nisan, N., & Ronen, A. (1999). Algorithmic mechanism design. In *Proceedings of the 31st STOC* (pp. 129–140). ACM.
22. NIST. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. National Institute of Standards and Technology.
23. North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
24. Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press.
25. Parkes, D. C., & Wellman, M. P. (2015). Economic reasoning and artificial intelligence. *Science*, 349(6245), 267–272.
26. RFC 7515. (2015). *JSON Web Signature (JWS)*. IETF. https://datatracker.ietf.org/doc/html/rfc7515
27. RFC 8785. (2020). *JSON Canonicalization Scheme (JCS)*. IETF. https://datatracker.ietf.org/doc/html/rfc8785
28. Said, S. E., & Dickey, D. A. (1984). Testing for unit roots in autoregressive-moving average models of unknown order. *Biometrika*, 71(3), 599–607.
29. Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.
30. Weber, I., et al. (2019). Untrusted business process monitoring and execution using blockchain. *Business & Information Systems Engineering*, 61(1), 101–114.
