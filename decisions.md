Decision Log — AI Prospect Research & Qualification System

This log records architectural and design decisions made during the engineering design cycle for this project. Each entry captures not just what was decided, but why, so decisions can be revisited intelligently rather than re-litigated from scratch.

# Decision Log — AI Prospect Research & Qualification System

---

#D1
**Date:** 2026-09-22
**Context:** User's real workflow needs bulk prospecting (10–20 URLs), but the current pipeline (single-URL, 3-agent) is unproven in reliability and quality.
**Decision:** Build and harden single-URL synchronous processing first. Bulk/async processing (job queue, job state) is deferred until the core pipeline is reliable.
**Why:** A single URL is the atomic unit of work either way. Hardening it first means bulk later becomes a wrapper around it, not a redesign. Building bulk infra now would multiply an unproven pipeline's failures by 10–20x before the failures are even understood.
**Alternatives:**
- Bulk processed synchronously in a loop — rejected: 15–20 min wall time with no incremental feedback at 10–20 URLs, and complicates partial-failure recovery.
- Full async job-queue bulk processing now — rejected: real infra (queue, persistence, job state) shouldn't be built on top of an unhardened pipeline.

---

#D2
**Date:** 2026-09-22
**Context:** Agents need a stable contract for output structure and a way to represent fit/quality of a prospect.
**Decision:** Fixed 6-section report structure (Company Overview, Business Analysis, Opportunity Findings, Qualification Score, Recommended Offer, Outreach Package) is the functional contract between agents. Qualification Score is numeric, 1–10.
**Why:** Already defined by the user and stable enough to design against; gives each agent's structured output a clear handoff contract.
**Alternatives:** None seriously considered — structure was already fixed going in.

---

#D3
**Date:** 2026-09-22
**Context:** Research agent's output currently carries only page-level source URLs, not per-claim provenance. Hallucinated facts are a confirmed real problem (compounds across Research → Strategy → Outreach).
**Decision:** Grounding/hallucination schema design (e.g. confirmed vs. inferred split) is deferred to agent-level implementation, not decided now.
**Why:** Choosing schema granularity in the abstract, before seeing real agent output, risks designing against assumptions instead of actual LLM behavior. Better decided while implementing/prototyping the Research agent.
**Alternatives:**
- Per-claim citations (source URL/quote per fact) — more rigorous, but real schema/prompt overhead; deferred along with the rest of this decision.
- Confirmed vs. inferred split — simpler, was the leading candidate, but locking it in now was judged premature.

---

#D4
**Date:** 2026-09-22
**Context:** Outreach agent has LLM-driven access to a tool that can request Strategy be revised. This is a deliberate control-flow loop (agent decides strategy is insufficient), not failure recovery — and is architecturally distinct from the existing per-step retry (max 3, failure-triggered). Confirmed via real observed use, not hypothetical.
**Decision:** Orchestrator supports one bounded backward transition: Outreach → Strategy (re-run once, with Outreach's stated reason) → Outreach resumes with revised output. Capped at once per run, tracked independently from the retry counter. No special fallback needed if the cap is hit — a still-weak strategy surfaces naturally via a lower Qualification Score.
**Why:** Matches the one real, observed case. Boundable and simple to reason about. Avoids infinite-loop risk without building unjustified general infrastructure.
**Alternatives:**
- No orchestration support (remove the tool) — rejected: discards a mechanism with real evidence it's needed.
- General revision loop (any agent can request revision from any prior agent) — rejected: premature generality, no evidence of needing more than the one known case.

---

#D5
**Date:** 2026-09-22
**Context:** Needed to map what context each agent actually receives, to check for gaps before touching prompts/schemas.
**Decision:** Research ← raw cleaned page content. Strategy ← Research's full structured output + user-provided `service`, `proof`, `low_risk` (Research never sees these). Outreach ← Strategy's output + channel only (no raw Research output).
**Why:** Keeps Research focused purely on factual discovery; user-provided sales context is layered in only where it's needed (Strategy). Confirmed as current real implementation, not a proposal.
**Alternatives:** None proposed yet — flagged as an open concern that Outreach having no raw Research visibility means Strategy is the sole gatekeeper between facts and the outreach message, likely related to D3.

---

#D6
**Date:** 2026-09-22
**Context:** Three separate-looking issues surfaced during design review, all tracing back to Strategy agent output quality.
**Decision:** Track together, fix together, in a later polishing pass — not now:
1. Strategy agent hallucinates facts not present in Research output.
2. `request_strategy_review()` is currently implemented as a tool-internal patch that bypasses the orchestrator entirely — the bounded-once guarantee from D4 is not currently enforced in code.
3. Prompt-level grounding rules were not designed at stage 3.
**Why:** These three likely share one root cause. Fixing Strategy's grounding is likely to move all three forward at once; solving them separately risks patching symptoms instead of the shared cause.
**Alternatives:** Design the prompt grounding rule now, independently — rejected: judged better to bundle with the mechanism decision (D3) rather than decide the rule in isolation and re-decide the mechanism later.

---

#D7
**Date:** 2026-09-22
**Context:** Current extraction (crawl4ai, multi-page attempt) times out under real use. Full-site crawling is also incompatible with the <60s total pipeline latency budget regardless of reliability.
**Decision:** Targeted page discovery — rule-based link matching (about, pricing, product, services, team, case-studies, etc.), capped at 5 pages total (homepage + up to 4), per-page timeout (TBD empirically), skip failed pages and continue with successes. Minimum viable page count (failure floor) still open.
**Why:** Research needs sufficient business signal, not exhaustive coverage. A small set of high-value pages is faster, more reliable to build correctly, and likely higher-quality input than a full crawl diluted with irrelevant pages.
**Alternatives:**
- Full-site crawl — rejected: latency-incompatible and currently unreliable (timeouts).
- Homepage-only — rejected: likely insufficient signal for qualification/personalization.


*#D7 addendum*
**Decision**: Zero-pages-succeeded floor is not implemented now — deferred.
**Why**: Judged low-priority/unlikely enough for now to not block moving forward; partial success (even 1-2 of 5) already returns real content, so this only affects the rare full-failure case.
**Known gap**: If all 5 pages fail, Research proceeds with no real content, which risks fabricated output under D3/D6's known hallucination concern. No retry is currently triggered in this case.
**Revisit when**: Testing/eval (stage 9) shows this actually happening, or before wider rollout.

# D9

**Context:** Proposed a broad list of ~28 operational/business metrics to track via cost/token tracking database (D-earlier decision to add PostgreSQL for this purpose).

**Decision:** Track a focused core set only:

- Jobs processed
- Success/failure rate
- End-to-end error rate by type
- Processing latency (per run and average)
- Timeout rate
- Retry rate
- LLM API error rate
- Cost per job

**Why:** Most of the proposed list measured features that don't exist in this system (file uploads, users/accounts, queues, storage) or belonged to infra-level monitoring rather than the application. Tracking metrics for non-existent features adds schema complexity with zero signal.

The core set directly answers the questions that matter now:

- Is this reliable?
- Is this fast enough?
- Is this affordable?

**Alternatives:** Full ~28-metric list — rejected per above. Revisit individual metrics only when the feature they'd measure actually exists (e.g., bulk processing would justify queue/wait-time tracking).


# D10

**Context:** Feature — accumulate multiple saved prospect reports within one sitting and download them together as a single file.

**Decision:** Server-issued anonymous session ID (cookie-based, no login). Reports are tagged by session ID in storage, and "download all" retrieves and combines everything under that session ID. The session has an expiry/cleanup policy (TTL still to be decided).

**Why:** Enables accumulating saves across multiple prospect lookups within one sitting without requiring accounts. Chosen over a fully client-side approach (Option A) because server-side accumulation is more robust to page refreshes within the session. Chosen over a client-generated ID (Option C) because C carried the same server-side storage/cleanup burden as B with no real simplification, making B's more standard approach preferable.

**Alternatives:**

- **A (fully client-side, browser-held state, no backend involvement)** — rejected: fragile to refresh/tab-close, though simplest overall.
- **C (client-generated ID)** — rejected: same server-side burden as B, with no meaningful advantage.
