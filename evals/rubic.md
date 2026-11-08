# Prospect Evaluation Rubric

## 1. Purpose

This rubric evaluates the quality of each prospect report produced by the AI Prospect Research and Qualification workflow.

Evaluation consists of two separate parts:

- **Automated checks:** Verify output structure, required fields, input consistency, and workflow execution.
- **Manual checks:** Evaluate factual accuracy, company understanding, qualification quality, and practical usefulness.

Automated checks and manual scores must be recorded separately.

## 2. Manual Scoring System

Each manual criterion receives a score from **0 to 2**.

| Score | Meaning |
|---|---|
| 0 | Poor — fails the criterion or contains a significant problem. |
| 1 | Partial — meets the criterion inconsistently or requires corrections. |
| 2 | Good — meets the criterion with no significant issues identified. |

There are 9 manual criteria, giving a maximum overall score of **18 points**.

## 3. Manual Evaluation Criteria

### 3.1 Factual Accuracy

Evaluate whether claims about the prospect are supported by reliable evidence.

- **0:** Contains a material false claim or multiple unsupported factual assertions presented as facts.
- **1:** Mostly accurate but contains questionable claims or minor factual errors.
- **2:** Claims are supported by available evidence, with uncertainty clearly acknowledged.

### 3.2 Company Understanding

Evaluate whether the report correctly identifies the prospect and understands its business.

- **0:** Misidentifies the company or substantially misunderstands its business.
- **1:** Identifies the company correctly but demonstrates only partial understanding.
- **2:** Accurately describes the company's business, services, and relevant characteristics.

### 3.3 Qualification Quality

Evaluate whether the prospect's qualification outcome is justified by the available evidence.

- **0:** The qualification outcome is clearly unjustified or contradicts the evidence.
- **1:** The outcome is plausible but its justification is weak or incomplete.
- **2:** The outcome and its supporting reasoning align with the evidence and qualification criteria.

### 3.4 Evidence and Uncertainty

Evaluate whether the report distinguishes verified facts, reasonable inferences, and unknown information.

- **0:** Presents guesses as facts, invents evidence, or ignores important uncertainty.
- **1:** Provides some supporting evidence but inconsistently communicates uncertainty.
- **2:** Clearly distinguishes supported facts, reasonable inferences, and unknowns.

### 3.5 Output Usability

Evaluate whether the final report is complete, understandable, and usable by its intended audience.

- **0:** Incomplete, confusing, or unusable without substantial correction.
- **1:** Generally understandable but requires some correction or clarification.
- **2:** Clear, complete, well-organized, and usable with minimal or no correction.

### 3.6 Offer Consistency in Message

Evaluate whether the proposed outreach message is consistent with the offer, prospect research, and qualification findings.

- **0:** Misrepresents the offer, makes unsupported claims about the prospect, or proposes an irrelevant message.
- **1:** Generally relevant but includes weak personalization or some inconsistencies.
- **2:** Accurately represents the offer and uses relevant, evidence-based personalization.

### 3.7 Correct Contact Paths

Evaluate whether the recommended contact route is appropriate and supported by evidence.

Examples include an official contact page, a relevant department, or a verified professional contact.

- **0:** Contact route is incorrect, irrelevant, or fabricated.
- **1:** Route is plausible but not sufficiently verified or specific.
- **2:** Route is appropriate and supported by available evidence.

An inferred email address must not be treated as verified unless evidence supports it.

### 3.8 Qualification Reasoning Consistency

Evaluate whether the report's explanation, evidence, and final qualification outcome are logically consistent.

- **0:** The conclusion contradicts the evidence or the stated reasoning.
- **1:** Reasoning is partly consistent but contains gaps or contradictions.
- **2:** The reasoning follows logically from the available evidence and stated qualification criteria.

### 3.9 Research Relevance and Freshness

Evaluate whether the research is relevant to the prospect and sufficiently current for the claims being made.

- **0:** Research is substantially irrelevant, outdated for important claims, or about the wrong company.
- **1:** Research is mostly relevant but contains gaps or questionable freshness.
- **2:** Research is relevant to the prospect and sufficiently current for the claims being evaluated.

Do not penalize a report merely because a company has limited public information. Evaluate how appropriately the workflow handles that limitation.

## 4. Overall Score Calculation

Calculate the overall score by adding the scores for all 9 manual criteria.

**Formula:**

Overall Score = Sum of all 9 manual criterion scores

- Minimum score: 0
- Maximum score: 18

Optionally calculate the percentage:

Score Percentage = (Overall Score / 18) × 100

Example:

| Criterion | Score |
|---|---:|
| Factual Accuracy | 2 |
| Company Understanding | 2 |
| Qualification Quality | 1 |
| Evidence and Uncertainty | 1 |
| Output Usability | 2 |
| Offer Consistency | 2 |
| Correct Contact Paths | 1 |
| Qualification Reasoning Consistency | 2 |
| Research Relevance and Freshness | 1 |
| **Overall Score** | **15/18 (83%)** |

## 5. Acceptance Criteria

A report passes the overall quality evaluation only when both conditions are satisfied:

1. The overall manual score is at least **12/18 (67%)**.
2. No critical factual issue is identified.

The 12/18 threshold reflects the 9-criterion scoring format used in the
evaluation results. It is an initial project-defined threshold, not a
statistically validated industry standard. Review the first few reports to
calibrate the rubric, then freeze the threshold before evaluating the full
baseline dataset.

A report that meets the numerical threshold but contains a critical factual issue fails acceptance.

Automated validation results must be recorded separately. A report may be manually acceptable while failing a technical check, so record both outcomes rather than collapsing them into one score.

## 6. Critical Factual Issues

A critical factual issue is a verified error that could materially mislead the user or lead to a bad business decision.

Examples include:

- Incorrectly identifying the prospect or confusing it with another company.
- Fabricating a significant company attribute, service, achievement, or business need.
- Claiming the prospect has a specific problem without supporting evidence.
- Recommending outreach based on a materially false claim.
- Providing a fabricated contact route as if it were verified.

Record a critical issue only when there is sufficient evidence to support the assessment. An unverified claim is not automatically a proven falsehood, but it may still reduce the scores for factual accuracy and evidence handling.

## 7. Automated Checks

Record each automated check as `PASS`, `FAIL`, or `NOT_RUN`.

The evaluation records six automated checks:

1. **Output validation:** Output conforms to the expected schema and format.
2. **Required fields:** All mandatory fields are present.
3. **User input consistency:** The report corresponds to the submitted prospect and does not unexpectedly change the input identity.
4. **Workflow completion:** The end-to-end workflow reaches its expected completion state.
5. **Evidence/reference availability:** Required research evidence or source references are present.
6. **Execution error details:** Record relevant timeouts, API errors, tool failures, or validation errors.

A `NOT_RUN` result means the check could not be evaluated. It must not be counted as a pass.

## 8. Failure Recording

For each significant failure, record:

- **Failure:** Concise description of what went wrong.
- **Category:** Primary failure type.
- **Evidence:** Relevant output excerpt, source, or trace reference.
- **Impact:** Consequence for the prospect report or workflow.
- **Severity:** Critical, major, or minor.
- **Root cause:** Research/retrieval, model reasoning, prompt, validation, integration, or unknown.
- **Next Action:** Proposed investigation or corrective action.

Recommended failure categories:

- Research or retrieval failure
- Company identification or understanding
- Factual error or unsupported claim
- Qualification reasoning
- Sparse-data handling
- Offer or message inconsistency
- Contact-path error
- Output validation or formatting
- Workflow execution or timeout
- Other

Record the primary failure category in the per-prospect summary. Preserve additional failure records when a report has multiple distinct issues.

## 9. Per-Prospect Evaluation Record

Each evaluated run should capture:

- `prospect_id`
- `run_id`
- Automated check results
- Individual manual criterion scores
- `overall_score`
- `score_percentage` (optional)
- `meets_minimum_quality`
- `critical_factual_issue` (`N/A`, `Minor`, `Major`, or `Critical` in the current evaluation results)
- `workflow_status`
- `usable`
- `primary_failure_category`
- `latency_seconds`
- `next_action`

Use a distinct `run_id` for every execution, including repeated runs of the same prospect.

Define `workflow_status` separately from report quality. The current evaluation
files use `Succeed`/`succeed` and `Failed`; new records should normalize these
to the following values:

- `success`: Workflow completed normally.
- `partial_success`: Workflow returned incomplete results or encountered a recoverable issue.
- `failed`: Workflow did not produce the expected result.

`usable` indicates whether the report can be used for its intended purpose without substantial correction. It is distinct from `meets_minimum_quality`.

## 10. Evaluation Procedure

For each prospect:

1. Run the complete workflow through the deployed frontend.
2. Preserve the input, final output, research evidence, and relevant trace.
3. Execute automated checks and record their results.
4. Score all 9 manual criteria using this rubric.
5. Calculate the overall score and determine whether the acceptance criteria are met.
6. Record critical factual issues and other significant failures.
7. Assign a next action based on the observed failure or quality gap.

Use the same rubric and acceptance threshold for the full baseline dataset. If the rubric changes, document the change and avoid comparing scores from different rubric versions without accounting for the difference.

## 11. Interpretation and Limitations

The evaluation measures observed performance on the selected prospect dataset. Results from a small dataset do not establish performance across all companies, industries, or research conditions.

Report both counts and percentages for important outcomes, such as `3/25 reports with factual errors`, and preserve individual failure examples so aggregate metrics do not hide serious issues.

Do not change prompts or system behavior immediately after every failure. First inspect the available evidence and trace to determine whether the issue originated in research, reasoning, prompt behavior, validation, or execution.
