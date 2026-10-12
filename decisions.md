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

**Amended by D12 (2026-09-28):** Research now also receives the user's `service`. It still never sees `proof` or `low_risk`.

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


#D12
**Date:** 2026-09-28
**Context:** A test run of the Research agent on a real site (dentist / expert-witness) showed that missing facts (company size, pricing) came back empty, which is correct. But pain points, buying behavior and objections were filled with confident text that the website could not have supplied. Strategy receives these as if they were findings, which likely contributes to D6.
**Decision:**
1. **Pain points:** Research receives the user's `service` in its prompt and looks for pain points from that angle. Each pain point must trace to something Research actually saw (a gap on the site, or a `search_web()` result). If there is no signal, the list stays empty.
2. **Buying behavior and objections:** kept, but renamed in the schema to `general_buying_behavior` and `general_market_objections`. They are general market context, not facts about this prospect.
3. **User inputs:** `user_service`, `user_proof` and `user_low_risk` are set by code, never by the LLM.
**Why:** These fields can't be confirmed from a website. A human researcher would also infer them from the service being sold and from market knowledge, and real objections only appear in real conversations. Labeling them in the schema keeps that distinction from getting lost in the prose. Requiring a visible signal for pain points stops the agent from inventing problems that happen to match the user's service.
**Alternatives:**
- Prompt-only rule ("only write what the page says") — rejected: nothing enforces it, and these are the fields the model most wants to fill.
- Confirmed/inferred label on every item (D3) — rejected for now: heavier schema, and it depends on the model labeling its own guesses honestly.
- Remove the fields from Research and let Strategy infer them — rejected: moves the guessing into Strategy, which is already the known problem agent (D6).
- Evidence required for every field — rejected: buying behavior and objections can't be grounded from a company website.



#D13
Context: A test input with almost no stated facts (a generic budgeting-app description) caused Research to return a fully empty Research_result, since every field correctly followed the empty-on-missing rule. An empty result has nothing for Strategy to build on, similar to the zero-pages extraction failure named but left open in D7.
Decision: If Research returns a fully empty result, treat it as a failure and retry, using the existing per-step retry logic, at most 3 times. If it's still empty after 3 attempts, stop the pipeline rather than passing an empty result to Strategy.
Why: An empty result reaching Strategy would give it nothing to reason from, which risks Strategy inventing content to fill a report structure that expects six sections. Retrying gives the extraction or the model a few more chances in case the emptiness was one bad run rather than a genuinely thin prospect. Stopping after 3 failures avoids silently returning a fabricated-looking report.
Alternatives:

Pass the empty result forward anyway — rejected: this is the exact failure mode named in D7 and left open, now confirmed with a real case.
Stop immediately without retry — rejected: doesn't distinguish a transient failure from a genuinely thin prospect.


#D14
Context: Failure 1 — ICP.Type was a free string and was regularly inferred as B2B or B2C without the text stating an audience.
Decision: ICP.Type changed to a fixed set of four values, B2B, B2C, Both, Unknown, enforced by schema, paired with a prompt rule requiring the audience to be explicitly stated, not implied, before assigning anything other than Unknown.
Why: A prompt rule alone stopped guessing on missing-audience cases but didn't stop the model inventing new labels outside the four values (Freelance Business) for cases where an audience was stated but oddly worded. The schema enforces the closed set regardless of prompt behavior.
Status: Confirmed correct on clear B2B, clear B2C, and clearly ambiguous inputs across repeated runs. One case, business-oriented language phrased unusually ("freelance businesses"), showed inconsistent results across 6 runs (B2C, Unknown, B2B, B2B, a validation error, B2C) before further prompt tweaking; closed based on user's testing, though not independently re-verified after the final tweak.


#D15
Context: Failure 2 — contradictory sources (prospect site vs. search results) were merged silently instead of being represented as a conflict.
Decision: For all fields, the prospect's own website takes priority over external/search evidence when the two conflict. Confirmed correct on location (site: Karachi, search: Lahore, output: Karachi, consistent across runs).
Why: The company is the authority on its own factual details, and for fields that don't affect the qualification score or the outreach message, a careful conflict-representation mechanism isn't worth the added complexity. Applying one simple rule everywhere is cheaper than deciding case-by-case which fields deserve special handling.
Alternatives:

Represent conflicts explicitly, keeping both values with a note — considered for fields that matter more, but set aside as unnecessary complexity given the policy is now the site-wins default for everything.


#D16
Context: Failure 4 (Test 15) — a pain point returned by search_web() was missing from the final Research_result, in every run, regardless of whether a service was provided.
Decision: Root cause was a code bug, not a prompt or model issue. The code that assembled tool output into the model's input read item["content"], but the tool's actual output used the key page_content. Every tool result silently returned None and was dropped before it ever reached the model.
Why: The dropped-evidence question needed to be settled by checking what the model actually received, not by tuning prompts, since the cause turned out to be earlier in the pipeline entirely.
Fix: Corrected the key name in the joining logic so tool content reaches the model as intended.

#D17
Context: ICP.Needs was built from general reasoning about what a prospect "needs," without evidence that a website can reliably reveal this. The failure-3 case showed a need ("online lead generation") generated from a marketing claim rather than anything the company or a tool actually stated. Real needs, problems, pains, desired results, mostly aren't disclosed by a company about itself and would require sources this system doesn't currently use.
Decision: Remove Needs from ICP entirely, rather than relabeling it as general market context.
Why: Unlike Buying_behavior and Objections, which are openly labeled as general and never claimed as prospect-specific, a Needs field left in the schema, even relabeled, would still tempt use as if it were a real finding, and Outreach could state it to a real prospect as if it were known. Keeping it would not make the report more useful, only more likely to contain something ungrounded that damages the user's credibility. Strategy and Outreach must now build the fit argument from the user's service plus what's actually confirmed: CompanyData, Services, and evidence-backed Pain_points.

#D18
**Date:** 2026-09-30
**Context:** After the Research agent hardening pass (D12–D17), the original 15 failure cases were re-run. 9 of 15 passed. 6 failed: Tests 4, 5, 8, 10, 14, 15.
**Decision:** Research agent hardening is closed for now with known, accepted gaps, not fully resolved to zero failures. The specific gaps:
1. **Evidence quality.** Test 4 (Unsupported Pain Point) showed that a tool-sourced claim can carry a real, checkable URL as evidence while still being a generic market statement ("common small-business problems include...") rather than something specific to the prospect. The current rule checks that evidence exists and is traceable; it does not yet check that the claim itself is about this company rather than the industry in general.
2. **Undiagnosed failures.** Tests 5, 8, 10, 14, and 15 failed on re-run. Test 10 is a likely regression, since it was confirmed passing before this hardening pass. The others have not been individually diagnosed with input/output pairs the way Tests 4 and 15 (originally) were.
**Why:** The two highest-risk problems, pain points and other fields being stated as fact without grounding (D12), and tool evidence being silently dropped (D16), are confirmed fixed. The remaining failures affect precision on specific inputs, not the basic trustworthiness of what Research passes downstream. Diagnosing and fixing all 6 now would delay starting on the Strategy agent, which has a confirmed, higher-impact defect (D6) still untouched.
**Status:** Deferred, not forgotten. Revisit after Strategy agent hardening, or sooner if any of these patterns reappear in Strategy's or Outreach's output in a way that traces back to Research.


#D19
Context: Testing Strategy against real Research output showed Pain_points frequently returning empty, traced to Research's D12 evidence rule being stricter in practice than intended, not to anything in Strategy. Separately, the question of whether Strategy should filter pain points by relevance to the user's service, or preserve the full list regardless of relevance, needed a decision.
Decision: Strategy preserves Pain_points from Research unchanged, with no relevance filtering. Relevance is handled only through the Qualification Score's Pain component, not by altering the list itself.
Why: Research already applies the evidence bar; filtering again in Strategy would discard pain points that are real and verified but not relevant to today's specific service, narrowing the report to one use case and losing information that could matter for a different pitch or a later look at the same prospect.
Known issue, logged separately: Research's evidence rule (D12, tightened further during the full hardening pass) returns empty Pain_points too often in practice. Needs its own review, revisit before relying on Strategy's pain-based scoring at scale.


#D20
Date: 5-10-2026
Context: Strategy agent hardening pass. Original STR-01 through STR-19 failures all confirmed fixed. Added input validation, tool-call validation, evidence-bound generation, exact-match preservation checks on proof/low_risk/Pain_points, fail-fast exception handling, logging, and the Pain/Fit-based Qualification Score replacing the original opaque score.
Decision: Strategy agent hardening closed. Known open items carried forward, not resolved in this pass:

D4, the review-loop orchestration mismatch, is still unfixed. It belongs at the orchestrator level, not inside Strategy, and needs to be addressed when the orchestrator or Outreach is next worked on.
D19, Research's pain-points-returning-empty issue, is still open. Strategy's scoring and Problem/Desirable-outcome fields depend on Pain_points having content; while that Research-side issue is unresolved, Strategy will often score and report on an empty pain picture.
Why: All concretely identified Strategy-level failures are fixed and tested. The two remaining items are correctly out of scope for this pass, D4 belongs to the orchestrator, D19 belongs to Research, carrying them forward keeps them visible rather than letting them be mistaken as resolved now that Strategy is closed.


#D21
Context: Outreach's job is to rewrite and strengthen offer, proof, low-risk, and CTA using copywriting judgment, not reproduce them verbatim, unlike Strategy's fixed fields. This makes exact-match validation wrong here, the real risk is invented claims or deliverables not present in any input field, which isn't cheaply checkable in code, a keyword list only catches already-seen inventions and misses anything new.
Decision: No automated semantic check added for Outreach's invention risk right now. Relying on test coverage to catch this, same approach as Research's remaining known gaps, not a second LLM-based validation call.
Why: A keyword-based check gives false confidence without real protection. An LLM-based check would genuinely catch it but adds cost, latency, and a new non-determinism source, the same tradeoff already declined for Strategy.
Status: Open, revisit if testing or real use shows invented claims reaching a user, at which point an LLM-based check becomes worth the cost it was declined for here.



#D22
Context: Outreach fallback behavior across its failure points.
Decision:

API-level failures (timeout, rate limit, connection error) — retry.
Schema validation failure on structured output — already implemented.
refine_offer runs but doesn't meaningfully strengthen the offer — proceed and write the message from the original, unrefined offer rather than retrying or failing the run.
Offer from Strategy is empty or unusable — already routed through input validation, same pattern as D13.
Why: Only the API-level failure is transient and worth retrying; everything else either has a defined fallback already, or, in #3's case, has real content to work with even if weaker than ideal, so proceeding is better than discarding a usable run.

#D23
**Date:** 
**Context:** After hardening all three agents, 10 end-to-end runs on one real URL all failed. Pain points were missing or dropped between agents, and validation rules stopped runs that could still have produced a message.
**Decision:** Remove pain points and the 1-10 score. Research keeps only facts backed by a verified quote from the page. Strategy outputs `fit` (strong/moderate/weak/insufficient_evidence) and `qualification` (strong/medium/low). The report ends with a `status` field, so thin data produces `insufficient_evidence` instead of a crash.
**Why:** Pain points can only be found by guessing or through real conversations with the prospect, not from website content, so they can't be grounded in the page. The old chain depended on a field the source can't supply. `fit` carries the same information the score did, in a coarser format.
**Alternatives:**
- Keep pain points as optional and compute the 1-10 score from Fit and Pain (D12, D19) — rejected: the pain input stays unreliable, so the score would rest on it.
**Supersedes:** D2 (score format), D12, D19. `offer.problem` stays in the report, labeled as a guess ("may be struggling with...").


#D24
**Date:** 2026-10-12
**Context:** The same input run 3 times gave fit `insufficient_evidence`, `moderate`, `insufficient_evidence`, with qualification following (low, medium, low). The research was identical each time. The prompt doesn't say whether a plausible business type with no stated need counts as `moderate` or `insufficient_evidence`.
**Decision:** Fit consistency is deferred to the eval pass. Orchestrator hardening comes first.
**Why:** The pipeline now completes end to end, and fit stability is easier to fix once there's an eval set to measure it against.
**Known issue:** Fit is unstable on the same input. Fix by writing one rule for what earns each fit value, and by lowering Strategy's temperature (0 to 0.2). Then check that 5 runs return the same value 5 times.