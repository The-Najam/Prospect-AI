## ***NOTE : This Testing Based On Old Schema Design***


## Test: Empty Website Content

**Input:** Empty `pages` content.

**Expected:**

* No hallucinated information.
* No unnecessary tool call.
* Empty/insufficient research result.
* Agent should not crash.

**Actual:**

* Agent completed successfully.
* Returned empty values for company data, services, ICP, opportunities, and user-owned fields.
* No hallucinated information observed.

**Result:** PASS

**Issue:** None.



## Test: Useless / Irrelevant Content

**Input:**

 When morning paints the sky with gold,
            And night releases dreams it holds,
            A quiet breeze begins to sing,
            Of all the hope that dawn can bring.

            The roads may twist, the winds may rise,
            And clouds may gather in the skies,
            Yet somewhere deep within the heart,
            A little light will never part.

            We walk through days we cannot know,
            Through fields of joy and streams of woe.
            Some days are bright, some days are gray,
            But every night gives birth to day.

            A tree may bend beneath the rain,
            Its leaves may tremble in the pain,
            But when the storm has passed away,
            It lifts its branches toward the day.

            So let us walk with gentle feet,
            And find the beauty where we meet.
            A smile, a word, a helping hand,
            Can turn a desert into land.

**Expected:**

* No hallucinated company details, services, ICP, pricing, or pain points.
* No unnecessary tool call.
* Empty or appropriately incomplete research result.
* Agent should complete without crashing.

**Actual:**

* Agent completed successfully.
* Returned empty values for company data, services, ICP, opportunities, and user-owned fields.
* No hallucinated information observed.

**Result:** PASS

**Issue:** None.


## Test: Missing Research Fields

**Input:** 
International College of Dentists: The Timelessness of Volunteering

A live presentation given by ICD Fellow, Dr. Richard Williamson during the 2019 Canadian Dental Association Convention in Saskatoon, Saskatchewan, Canada, as a joint effort between ICD and the Academy of Dentistry International, funded by ICD Section I USA and ICD Section II Canada.

The presentation focuses on volunteering and providing humanitarianism service internationally and is intended to be a useful guide for all dentists, dental staff and ICD Fellows who are interested in oral health care volunteerism worldwide.Dentistry is both an art and science and as such, dentists can have different opinions on how to treat a patient. However, there are Standards of Care that must be adhered to, and scientific evidence must be used to guide appropriate care. This is called evidence-based dentistry, and it is the integration of the best scientific evidence available with dental expertise while considering the patient’s needs and desires.
**Expected:**

* Extract only information supported by the input.
* Missing company size, services, pricing, and location should remain empty.
* ICP information should only include details supported by the content.
* No invented pain points.
* General market context should not be presented as prospect-specific facts.
* No unnecessary tool call merely because fields are missing.

**Actual:**

* Company name, description, industry, ICP location, and ICP needs were reasonably grounded in the provided content.
* Company size and services remained empty.
* Pain points remained empty.
* `ICP.Type` was returned as `B2B`, although the provided content does not explicitly establish a B2B customer type.

**Result:** FAIL

**Issue:** The agent inferred an ICP type that was not directly supported by the available evidence.

**Root Cause:** Research agent inferred `B2B` from contextual information instead of leaving the field empty when the evidence was insufficient.


## Test: Unsupported Pain Point

**Input:**
We provide professional website design and development services for small businesses.

Our services include responsive website design, e-commerce development,
website maintenance, and custom web applications.

We focus on creating modern, fast, and user-friendly websites tailored
to each client's requirements.

**Expected:**

* Services may be extracted from the provided content.
* No pain points should be generated without supporting evidence.
* No generic assumptions such as “small businesses struggle with outdated websites.”
* ICP should contain only information directly supported by the input.
* No unnecessary tool call.

**Actual:**

* Completed successfully.
* Services were extracted accurately from the provided content.
* `Pain_points=[]` — no unsupported pain points were generated.
* ICP identified as `Small businesses`, which is directly supported by the content.
* Needs were derived from the explicitly listed services.
* No hallucinated location, company size, pricing, or objections.
* No unnecessary tool call.

**Result:** PASS

**Issue:** None.

**Root Cause:** N/A

## Test: Conflicting Information

**Input:**
We are a software development company based in London.

Our team operates from New York and serves clients exclusively in Canada.

We specialize in mobile app development and enterprise software solutions.

**Expected:**

* Do not choose one location arbitrarily.
* Flag the conflicting location information or leave `location` empty.
* Services should be extracted accurately.
* Do not infer additional company details.
* No hallucinated ICP, company size, pricing, or pain points.
* No unnecessary tool call.

**Actual:**

* Web Search tool was called.
* `CompanyData.location` was set to `London`.
* `ICP.location` was set to `Canada`.
* Services were extracted correctly.
* `ICP.Type='B2B'` was inferred even though it was not explicitly supported.
* No pain points, company size, pricing, or objections were hallucinated.

**Result:** FAIL

**Issue:** Conflicting location information was not handled explicitly. The agent selected `London` as the company location while using `Canada` as the ICP location without resolving or flagging the conflict. It also inferred `B2B` without direct evidence.

**Root Cause:** The research agent does not currently have a sufficiently explicit rule for handling conflicting evidence. It appears to select plausible values from different statements rather than recognizing the conflict and preserving uncertainty.


## Test: Misleading Marketing Claims

**Input:**
We are the #1 web development agency in the world.

Our award-winning team delivers the fastest websites
and guarantees 10x more leads for every client.

We provide website design, SEO, and digital marketing services.”

**Expected:**

* Extract the explicitly stated services.
* Do not treat “#1” as a verified factual claim.
* Do not treat “10x more leads” as an established company capability without supporting evidence.
* Do not invent company size, location, industry details, pricing, or pain points.
* Avoid converting marketing language into factual research findings.
* No unnecessary tool call.

**Actual:**

* No tool call was detected.
* Services were extracted correctly.
* The `about` field repeated marketing claims such as “delivering fast websites and guaranteeing increased leads.”
* `ICP.Type='B2B'` was inferred without direct evidence.
* `ICP.Needs` included “Fast, high-performing websites” and “Increased lead generation,” derived from the company's marketing claims.
* `General_Buying_behavior` was generated as an unsupported inference from the marketing language.
* No unsupported pain points were generated.
* No company size, location, or pricing was hallucinated.

**Result:** FAIL

**Issue:** Marketing claims were treated as factual or research findings. The agent also generated buying behavior from the company's marketing language without supporting evidence.

**Root Cause:** The research prompt does not sufficiently distinguish between a prospect stating a marketing claim and independently verified evidence. The model is also still inferring `ICP.Type` and general buying behavior when the source does not provide enough evidence.


## Test: Ambiguous Company Identity

**Input:**
We help businesses grow with technology.

Our team builds custom software, websites, and mobile applications.

Trusted by leading companies across multiple industries.

**Expected:**

* Do not invent or guess the company name.
* Services can be extracted.
* Do not infer a specific industry for the company.
* Do not infer company size.
* Do not infer a specific ICP beyond what the text supports.
* Do not treat “trusted by leading companies” as evidence of specific customers or company scale.
* No pain points should be generated.
* No unnecessary tool call.

**Actual:**

* Web Search tool was called.
* Company name, location, industry, and company size remained empty.
* Services were extracted correctly.
* `ICP.Type='B2B'` was inferred without direct evidence.
* `ICP.Needs` included reasonable descriptions based on the stated services.
* No pain points, objections, or unsupported company details were generated.

**Result:** FAIL

**Issue:** The agent inferred `ICP.Type='B2B'` despite the input not explicitly establishing a B2B business model.

**Root Cause:** The ICP type field still permits the model to infer a business classification from context instead of requiring direct supporting evidence.

## Test: Contradictory Service Information

**Input:**
Website content stated that the company does not provide mobile app development or SEO, while a separate services list included both.

**Expected:**

* Identify the contradiction around mobile app development and SEO.
* Do not blindly include contradicted services as confirmed services.
* Website development and maintenance should be extracted.
* Do not invent additional company information.
* No unsupported pain points or ICP details.
* No unnecessary tool call.

**Actual:**

* No tool call was detected.
* Website development and maintenance were extracted correctly.
* Mobile app development and SEO were excluded.
* The contradictory information was not explicitly reported or flagged.
* `ICP.Type='B2B'` was inferred without direct evidence.
* No unsupported pain points or general buying behavior were generated.

**Result:** FAIL

**Issue:** The agent handled the contradiction by excluding the explicitly denied services, but it did not preserve or flag the conflicting information. It also continued to infer `ICP.Type='B2B'` without sufficient evidence.

**Root Cause:** The research contract does not define how conflicting evidence should be represented. The model resolves the contradiction implicitly instead of surfacing uncertainty, while the ICP type remains vulnerable to contextual inference.


## Test: Temporal / Outdated Information

**Input:**
We are a digital marketing agency founded in 2018.

In 2021, we offered SEO, PPC, and social media marketing.

Since 2024, we have focused exclusively on B2B content marketing
and no longer provide PPC or social media marketing services.

Our current services include:
- B2B content strategy
- Content creation
- SEO

**Expected:**

* Distinguish historical information from current information.
* Current services should be B2B content strategy, content creation, and SEO.
* Do not treat PPC or social media marketing as current services.
* Do not infer unsupported company details.
* No unsupported pain points or buying behavior.
* No unnecessary tool call.

**Actual:**

* Web Search tool was called.
* Current services were correctly extracted as B2B content strategy, content creation, and SEO.
* Historical PPC and social media marketing services were correctly excluded.
* Company founding year and industry were extracted from the provided content.
* No unsupported pain points or buying behavior were generated.
* `ICP.Type='B2B'` was inferred without direct evidence.

**Result:** FAIL

**Issue:** The temporal information was handled correctly, but the agent still inferred `ICP.Type='B2B'` without sufficient evidence.

**Root Cause:** The ICP type field continues to allow contextual inference rather than requiring explicit evidence from the source.

## Test: Tool Returns No Useful Data

**Input:**
BrightSmile Dental Care website content contained insufficient company information, causing the Research agent to call the Web Search tool. The Web Search tool returned `None`.

**Expected:**

* Tool is called because the information gap is material.
* Tool failure/empty result does not crash the Research agent.
* Research does not invent information to compensate.
* Unsupported fields remain empty.
* Valid research output is still returned.
* The failed tool result is handled gracefully.

**Actual:**

* Web Search tool was called and returned `None`.
* Research completed successfully without crashing.
* Company name, description, industry, and services were returned from the available website content.
* No additional information was invented to compensate for the failed search.
* Unsupported fields such as location, company size, pricing, pain points, buying behavior, and objections remained empty.

**Result:** PASS

**Issue:** None related to the tested failure case.

**Root Cause:** N/A


## Test: Conflicting Tool Evidence

**Input:**
Website input:

Acme Dental Care is a dental clinic based in Karachi.
We provide general dentistry and cosmetic dentistry.

Web Search result:

Acme Dental Care operates in Lahore and specializes in orthodontics.
**Expected:**

* Conflicting information should not be silently merged as if both are true.
* The agent should preserve the conflict or avoid asserting the disputed field.
* Website-supported services can still be extracted.
* No hallucinated information should be added.
* Research should complete without crashing.

**Actual:**

* Research completed successfully without crashing.
* The agent combined information from both sources.
* `CompanyData.location` was set to `Karachi, Pakistan` despite conflicting search evidence.
* `about` and `services` combined website and search information.
* `ICP.location` was set to `Karachi, Lahore (Pakistan)`, explicitly merging the conflict.
* `Orthodontics` was added as a service based on the conflicting search result.
* No pain points or unsupported company size/pricing were generated.

**Result:** FAIL

**Issue:** Conflicting evidence was not handled explicitly. The agent merged contradictory information into the research output instead of preserving the conflict or leaving the disputed fields unresolved.

**Root Cause:** The research contract does not yet define a conflict-resolution rule for evidence from different sources. The model attempts to combine both sources rather than distinguishing or flagging conflicting claims.


## Test: Unsupported General Market Inference

**Input:**
We provide accounting software for small businesses.

Our platform includes invoicing, expense tracking, and financial reporting.
**Expected:**

* Extract the stated services/features.
* `General_Buying_behavior` should remain empty because no buying behavior is provided.
* `General_Objections` should remain empty because no objections are provided.
* Do not generate generic assumptions such as “small businesses are price-sensitive.”
* No prospect-specific pain points should be generated.
* No unnecessary tool call.
* Research should complete successfully.

**Actual:**

* Research completed successfully.
* Services/features were extracted correctly.
* `General_Buying_behavior=''`.
* `General_Objections=''`.
* No generic buying behavior or objections were generated.
* No prospect-specific pain points were generated.
* No unnecessary tool call was detected.
* `ICP.Type='B2B (small businesses)'` was inferred, but this was outside the specific general-market-inference failure being tested.

**Result:** PASS

**Issue:** None related to the tested failure case.

**Root Cause:** N/A


## Test: Malformed Tool Output

**Input:**
Web Search was triggered for a material information gap and returned the unexpected structure:

```text
{
    "results": None
}
```

**Expected:**

* Tool is called because the information gap is material.
* Unexpected tool output does not crash the Research agent.
* The malformed result is not treated as valid research evidence.
* Unsupported fields remain empty.
* Research still returns a valid structured result when possible.
* No hallucinated information is created to compensate.

**Actual:**

* Research completed successfully without crashing.
* The malformed tool output did not cause invalid data to appear in the research result.
* Company name, description, location, industry, and company size remained empty.
* Services and ICP needs were extracted from the original website content rather than the malformed search result.
* No pain points, buying behavior, or objections were generated.

**Result:** PASS

**Issue:** None related to the tested failure case.

**Root Cause:** N/A



## Test: Mixed Evidence Quality

**Input:**
We provide accounting software for small businesses.

Our platform offers automated invoicing, expense tracking,
and financial reporting.

Thousands of businesses trust our platform to transform
their finances and eliminate all accounting problems.

Our software is the perfect solution for every small business.

**Expected:**

* Extract the explicitly stated services/features.
* Treat marketing claims as claims, not verified facts.
* Do not infer specific customer characteristics from those claims.
* Do not generate prospect-specific pain points from generic accounting problems.
* `General_Buying_behavior` and `General_Objections` should remain empty unless supported by evidence.
* No unnecessary tool call.
* Research should complete successfully.

**Actual:**

* Research completed successfully.
* Accounting software and its explicitly stated features were extracted.
* No pain points, buying behavior, or objections were generated.
* Marketing claims were copied into the `about` field without being explicitly distinguished as claims.
* `ICP.Needs` included `Eliminate accounting problems`, which is derived from a marketing claim rather than a stated customer need.
* `ICP.Type='B2B'` was inferred, but this was outside the specific mixed-evidence behavior being tested.
* No unnecessary tool call was detected.

**Result:** FAIL

**Issue:** A marketing claim was converted into an ICP need. The `about` field also preserved marketing claims as if they were ordinary company information.

**Root Cause:** The research contract does not clearly distinguish factual descriptive content from promotional/marketing claims when populating research fields such as `ICP.Needs` and `about`.


## Test: Partial Web Search Result

**Input:**
Web Search returned a partially populated result:

```python
{
    "pain_points": ["Difficulty attracting new patients"],
    "avilable_solutions": [],
    "satisfied": None,
    "resources": []
}
```

**Expected:**

* Research agent handles missing/empty fields without crashing.
* `pain_points` may be considered because the tool explicitly returned them.
* Empty `avilable_solutions` and `resources` should not cause invented values.
* `satisfied=None` should not be interpreted as `True` or `False`.
* No information should be fabricated to fill missing fields.
* Research should still return a valid structured result.

**Actual:**

* Research completed successfully without crashing.
* No hallucinated values were added for the empty tool fields.
* `satisfied=None` did not appear to be interpreted as `True` or `False`.
* The returned `Pain_points` list was empty despite the tool returning `["Difficulty attracting new patients"]`.
* The rest of the research output remained valid.

**Result:** FAIL

**Issue:** The Research agent did not preserve the pain point returned by the Web Search tool.

**Root Cause:** The tool output is not being reliably incorporated into the final research result, or the Research prompt/schema is filtering tool-provided pain points despite them being explicit tool evidence.
