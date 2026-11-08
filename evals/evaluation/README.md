# Prospect Workflow Evaluation

## 1. Objective

This evaluation measures the end-to-end Prospect AI workflow through the
deployed frontend and FastAPI backend. It covers report quality, factual
grounding, qualification decisions, technical reliability, and usability.

The evaluation uses the 9-criterion, 18-point manual rubric in
[`../rubic.md`](../rubic.md).

## 2. Evaluation Setup

- **Evaluation type:** End-to-end workflow evaluation
- **Execution method:** Deployed frontend and FastAPI endpoints
- **Prospects attempted:** 20
- **Evaluation approach:** Automated validation and manual review
- **Automated checks:** 6 checks per prospect
- **Manual scoring:** 9 criteria, 0–2 points each, maximum 18 points
- **Detailed results:** [`../evaluation_results.csv`](../evaluation_results.csv)
- **Manual review records:** [`../reviews.csv`](../reviews.csv)

The baseline records execution latency, automated checks, manual scores,
workflow status, usability, failure category, and retry behavior.

## 3. Dataset

The recorded dataset contains 20 prospect runs. The available records cover:

- Successful and failed website extraction.
- Successful and failed workflow execution.
- Partial company information.
- Incorrect or incomplete service extraction.
- Qualification reasoning problems.
- Outreach and messaging problems.

The current repository does not contain a separate `dataset.csv`; prospect
identity is recorded by `Prospect ID` in the evaluation results.

## 4. Evaluation Procedure

For each prospect:

1. Submit the prospect through the deployed frontend.
2. Record workflow status and latency.
3. Preserve the generated report and supporting evidence.
4. Record the six automated check results.
5. Score the generated report against all nine manual criteria.
6. Record failures, category, evidence, root cause, and severity.
7. Record usability, retry behavior, and the next corrective action.

The current CSV files use `Succeed`/`succeed`, `Failed`, `N/A`, `NO RUN`,
`Major`, and `Minor`. Future records should normalize these values to the
rubric's `success`, `partial_success`, `failed`, `PASS`, `FAIL`, and
`NOT_RUN` values.

## 5. Evaluation Metrics

| Metric | Definition |
|---|---|
| Average manual score | Mean score among generated reports, out of 18 |
| Quality acceptance rate | Reports meeting the rubric threshold and having no critical factual issue |
| Automated validation pass rate | Passed automated checks / automated checks recorded |
| Factual error rate | Reports with a verified factual or grounding error / generated reports |
| Critical factual issue rate | Reports with a critical factual issue / generated reports |
| Workflow failure rate | Failed executions / attempted executions |
| Average latency | Mean recorded latency across all attempts |

Only metrics supported by the recorded CSV data are reported below.

## 6. Baseline Results Summary

| Metric | Baseline result |
|---|---:|
| Prospects attempted | 20 |
| Reports successfully generated | 15/20 (75%) |
| Workflow failures | 5/20 (25%) |
| Average manual score | 12.87/18 (71.5%), across 15 generated reports |
| Reports scoring at least 12/18 | 12/15 (80%) |
| Recorded “Meets minimum” flags | 12/20 (60%) |
| Automated validation pass rate | 98/120 (81.7%) |
| Average latency | 61.68 seconds |
| Reports with `Major` issue label | 13/20 (65%) |
| Reports with `Minor` issue label | 5/20 (25%) |

The recorded `Meets minimum` field must not be treated as the final quality
acceptance rate. The CSV uses `Major` and `Minor` issue labels instead of the
rubric's explicit critical-factual-issue decision, so acceptance must be
reclassified before publishing a definitive quality rate.

## 7. Failure Analysis

### Research and company-information failures

The main quality failures involve incorrect or incomplete company
understanding:

- Services are mixed with taglines or other page text.
- Company descriptions and about sections are incomplete or mixed.
- People are confused with testimonial subjects.
- Company names and services are captured incorrectly.
- Some services are omitted.

These failures are recorded under research, company-information, and
company-information-services categories. They affect factual accuracy,
company understanding, evidence handling, and message relevance.

### Web extraction and workflow failures

Five runs did not produce a report. Recorded causes include failed content
extraction and workflow execution failures. Some failed runs have automated
checks marked `NO RUN`, so their manual quality cannot be evaluated.

### Qualification failures

At least one generated report contains incorrect qualification scoring and
reasoning. This indicates that qualification conclusions need stronger
evidence checks before outreach generation.

### Messaging failures

The generated outreach includes unsupported observations, fabricated proof,
invented offer mechanisms, unsupported outcomes, and CTA deviations. These
failures can make otherwise valid research unusable for outreach.

## 8. Improvements and Re-evaluation

The current CSVs document the baseline failures but do not record a completed
post-change re-evaluation. The following improvements are therefore proposed,
not measured before/after results:

| Improvement | Reason | Cases to retest | Before | After |
|---|---|---:|---:|---:|
| Improve service/tagline separation | Prevent incorrect service extraction | Research cases with service failures | Baseline recorded | Not run |
| Strengthen company/about extraction | Reduce partial or incorrect company profiles | Company-info failures | Baseline recorded | Not run |
| Add stricter qualification evidence checks | Prevent unsupported qualification scores | Qualification failure cases | Baseline recorded | Not run |
| Enforce outreach grounding and CTA preservation | Prevent fabricated claims and offer drift | Outreach failure cases | Baseline recorded | Not run |
| Improve extraction fallback and error reporting | Reduce failed workflow runs | All 5 failed runs | Baseline recorded | Not run |

After each change, rerun the same input cases, preserve the original baseline,
and record the new results separately. Do not overwrite
[`evaluation_results.csv`](../evaluation_results.csv).

## 9. Limitations

- The dataset contains only 20 runs.
- Public website content may be incomplete, dynamic, or unavailable.
- Manual scores involve reviewer judgment.
- The current CSVs contain inconsistent status and severity labels.
- `reviews.csv` and `evaluation_results.csv` are not perfectly synchronized.
- No repeat-run consistency dataset is recorded.
- Results may not generalize across industries or prospect types.

## 10. Conclusion

The baseline demonstrates that the workflow can generate usable reports, but
it does not yet meet a clean acceptance standard. Fifteen of 20 runs produced
reports, while five failed during extraction or workflow execution. The
average generated-report score was 12.87/18, but the dataset contains many
major issue labels and recurring research-grounding failures.

The highest-priority work is:

1. Improve website extraction and service classification.
2. Correct company and people identification.
3. Strengthen qualification reasoning.
4. Prevent unsupported claims and offer drift in outreach.
5. Normalize evaluation records and perform a post-change re-evaluation.

A definitive acceptance rate should be reported only after critical factual
issues are recorded separately and the CSVs are aligned with the rubric.
