# T01 — Instagram Happy Path

## Objective
Verify that a valid strong strategy produces a grounded Instagram DM using only the supplied strategy.

## Input
```json
{
  "qualification": "strong",
  "opportunity": {
    "pain": ["The company is actively hiring software engineers."],
    "fit": "strong",
    "score": 85
  },
  "offer": {
    "problem": "Difficulty hiring qualified software engineers efficiently.",
    "desirable_outcome": "Build a stronger engineering hiring pipeline.",
    "proof": "We help companies improve their software engineering hiring process.",
    "low_risk": "Start with a small, focused engagement.",
    "value": "A more efficient way to identify and engage relevant engineering candidates."
  },
  "reason": {
    "reason": [
      "The company is actively hiring software engineers.",
      "The hiring activity indicates a relevant opportunity for engineering recruitment support."
    ]
  },
  "angle": {
    "hooks": ["Active software engineering hiring"],
    "angle": "Help make engineering hiring more efficient.",
    "cta": "Open to hearing how?"
  },
  "channel": "instagram"
}
Expected Output
Plaintext
channel = "instagram"

outreach_msg:
  message = grounded Instagram DM
  subject_line = ""
  cta = simple low-friction CTA
Actual Output
Python
channel='instagram'
outreach_msg=DM(
  message='Your team is actively hiring software engineers. Many fast-growing tech companies hit a bottleneck when their careers page doesn’t attract the right talent. I design modern, mobile-friendly, SEO-optimized careers sites that showcase tech culture and improve candidate quality. With 6+ years of experience, I can put together a quick mock of a tailored careers page for you—free demo, no commitment.'
)
Passed Checks
Correct channel: instagram

Valid Pydantic output

Complete DM generated

Uses the supplied hiring information

Failed Checks
Uses only prospect information from input

Uses only the supplied offer

Uses the supplied strategy angle

Uses the supplied CTA

Avoids unsupported sender claims

Avoids unsupported prospect claims

Avoids invented outcomes

Avoids invented offer mechanisms

Failures
Unsupported prospect claim: "Many fast-growing tech companies hit a bottleneck..."

Invented prospect problem: "their careers page doesn’t attract the right talent"

Invented offer: "I design modern, mobile-friendly, SEO-optimized careers sites"

Unsupported outcome: "improve candidate quality"

Unsupported sender claim: "With 6+ years of experience"

Invented low-risk mechanism: "free demo, no commitment"

Strategy deviation: The generated offer is substantially different from the supplied engineering-hiring offer.

CTA deviation: Supplied CTA: "Open to hearing how?" — Generated CTA is effectively replaced by the free-demo offer.

Status
FAIL

```
T02 — LinkedIn Happy Path
=========================

Objective
---------

Verify that a valid strong strategy produces a grounded LinkedIn DM using only the supplied strategy.

Input
-----

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   {    "qualification": "strong",    "opportunity": {      "pain": ["The company is actively hiring software engineers."],      "fit": "strong",      "score": 85    },    "offer": {      "problem": "Difficulty hiring qualified software engineers efficiently.",      "desirable_outcome": "Build a stronger engineering hiring pipeline.",      "proof": "We help companies improve their software engineering hiring process.",      "low_risk": "Start with a small, focused engagement.",      "value": "A more efficient way to identify and engage relevant engineering candidates."    },    "reason": {      "reason": [        "The company is actively hiring software engineers.",        "The hiring activity indicates a relevant opportunity for engineering recruitment support."      ]    },    "angle": {      "hooks": ["Active software engineering hiring"],      "angle": "Help make engineering hiring more efficient.",      "cta": "Open to hearing how?"    },    "channel": "linkedin"  }   `

Expected Output
---------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   channel = "linkedin"  outreach_msg:    message = grounded LinkedIn DM    subject_line = ""    cta = simple low-friction CTA   `

Actual Output
-------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   channel='linkedin'  outreach_msg=DM(    message='Hey [Name], I saw you’re actively hiring software engineers. Companies in that spot often hit a bottleneck turning interest into qualified candidates. I’ve spent 6+ years building conversion-focused web experiences for tech firms, and I can spin up a custom careers landing page that surfaces the right talent faster and cheaper. We can start with a free demo to see if it fits your process.\n\n'  )   `

Passed Checks
-------------

*   Correct channel: linkedin
    
*   Valid Pydantic output
    
*   Complete DM generated
    
*   References the supplied hiring activity
    

Failed Checks
-------------

*   Uses only supplied prospect information
    
*   Uses only the supplied offer
    
*   Uses the supplied strategy angle
    
*   Uses the supplied CTA
    
*   Avoids unsupported sender claims
    
*   Avoids unsupported prospect claims
    
*   Avoids unsupported outcomes
    
*   Avoids invented offer mechanisms
    

Failures
--------

1.  **Unsupported personal observation**
    
    *   "I saw you’re actively hiring software engineers."
        
    *   The strategy states the fact but does not establish that the sender personally observed it.
        
2.  **Unsupported consequence**
    
    *   "Companies in that spot often hit a bottleneck turning interest into qualified candidates."
        
3.  **Unsupported sender claim**
    
    *   "I’ve spent 6+ years building conversion-focused web experiences for tech firms."
        
4.  **Invented offer**
    
    *   "custom careers landing page"
        
5.  **Unsupported outcome**
    
    *   "surfaces the right talent faster and cheaper"
        
6.  **Invented mechanism**
    
    *   "free demo"
        
7.  **CTA deviation**
    
    *   Strategy CTA: "Open to hearing how?"
        
    *   Generated CTA asks the prospect to evaluate a demo.
        
8.  **Strategy deviation**
    
    *   The generated message shifts from engineering hiring support to careers-site/web development.
        

Status
------

**FAIL**

T03 — Facebook Happy Path
=========================

Objective
---------

Verify that a valid strong strategy produces a grounded Facebook DM using only the supplied strategy.

Input
-----

Plain 
`   {    "qualification": "strong",    "opportunity": {      "pain": ["The company is actively hiring software engineers."],      "fit": "strong",      "score": 85    },    "offer": {      "problem": "Difficulty hiring qualified software engineers efficiently.",      "desirable_outcome": "Build a stronger engineering hiring pipeline.",      "proof": "We help companies improve their software engineering hiring process.",      "low_risk": "Start with a small, focused engagement.",      "value": "A more efficient way to identify and engage relevant engineering candidates."    },    "reason": {      "reason": [        "The company is actively hiring software engineers.",        "The hiring activity indicates a relevant opportunity for engineering recruitment support."      ]    },    "angle": {      "hooks": ["Active software engineering hiring"],      "angle": "Help make engineering hiring more efficient.",      "cta": "Open to hearing how?"    },    "channel": "facebook"  }   `

Expected Output
---------------

Plain `   channel = "facebook"  subject_line = ""  message = grounded Facebook DM  cta = simple low-friction CTA   `

Actual Output
-------------

Plain 
`   channel='facebook'  outreach_msg=DM(    message='Your team is actively hiring software engineers. When hiring ramps up, generic career pages often attract unqualified applicants, slowing the pipeline. We specialize in web design for engineering careers pages – our recent work lifted engineering applicant volume by 40% for similar tech firms, giving recruiters a steadier flow of qualified candidates. I can put together a free demo of a custom landing page tailored to your roles, no commitment required. Open to a quick look?'  )   `

Passed Checks
-------------

*   Correct channel: facebook
    
*   Valid Pydantic output
    
*   Complete DM generated
    
*   Uses supplied hiring information
    
*   subject\_line appropriately absent for DM
    

Failed Checks
-------------

*   Uses only supplied prospect information
    
*   Uses only supplied offer
    
*   Uses supplied strategy angle
    
*   Uses supplied proof
    
*   Uses supplied CTA
    
*   Avoids unsupported consequences
    
*   Avoids invented sender claims
    
*   Avoids invented offer
    
*   Avoids invented outcomes
    

Failures
--------

1.  **Unsupported prospect consequence**
    
    *   "generic career pages often attract unqualified applicants, slowing the pipeline"
        
2.  **Invented offer**
    
    *   "web design for engineering careers pages"
        
3.  **Unsupported proof**
    
    *   "lifted engineering applicant volume by 40%"
        
4.  **Invented outcome**
    
    *   "giving recruiters a steadier flow of qualified candidates"
        
5.  **Invented mechanism**
    
    *   "free demo of a custom landing page"
        
6.  **CTA deviation**
    
    *   Expected: "Open to hearing how?"
        
    *   Actual: "Open to a quick look?"
        
7.  **Strategy deviation**
    
    *   The generated message changes the offer from engineering hiring efficiency to careers-page/web design.
        

Status
------

**FAIL**

# T04 — Email Happy Path

 ========================

 ## Objective

 Verify email-specific output structure and grounded message generation.

 ## Input

 Plain

 `No input provided.`

 ## Expected Output

 Plain `channel = "email" subject_line = non-empty message = email body cta = low-friction CTA`

 ## Actual Output

 Plain\
 \`channel='email' outreach\_msg=DM( message='Hi,

 I saw you’re actively hiring software engineers. Scaling that pipeline efficiently can be a challenge—especially finding qualified candidates without drowning in noise.

 We run a focused, low-risk engagement that quickly surfaces and engages relevant engineering talent. In a recent free demo, a peer company cut time-to-hire by about 30% while improving candidate quality.

 Would a short, no-commitment demo be useful to see if we can help your team?

 Best,\
 \[Your Name\]' )\`

 ## Passed Checks

 - Correct channel: email
- Valid Pydantic output
- Complete message generated
- Uses supplied hiring information

 ## Failed Checks

 - subject\_line present
- Correct email output structure
- Uses supplied proof only
- Uses supplied low-risk mechanism
- Avoids unsupported claims
- Avoids invented sender/prospect information
- Uses supplied CTA

 ## Failures

 1. **Missing email subject line**
2. **Wrong output type**
   - Returned DM instead of email structure.
3. **Unsupported observation**
   - "I saw you’re actively hiring software engineers."
4. **Unsupported consequence**
   - "without drowning in noise"
5. **Invented proof**
   - "a peer company cut time-to-hire by about 30%"
6. **Invented free demo**
7. **Unsupported outcome**
   - "improving candidate quality"
8. **CTA deviation**
   - Strategy CTA: "Open to hearing how?"
9. **Strategy deviation**
   - Generated content substantially changes the supplied offer.

 ## Status

 **FAIL**

# T05 — Weak Offer → Refine

=========================

Test Input

Plain
{ "qualification": "weak", "opportunity": { "pain": [ "The company is actively hiring software engineers." ], "fit": "weak", "score": 35 }, "offer": { "problem": "Difficulty hiring software engineers.", "desirable_outcome": "Improve engineering hiring.", "proof": "We provide hiring support.", "low_risk": "Start with a small engagement.", "value": "More efficient engineering recruitment." }, "reason": { "reason": [ "The offer has weak differentiation.", "The current opportunity fit is limited." ] }, "angle": { "hooks": [ "Active software engineering hiring" ], "angle": "Help improve engineering hiring efficiency.", "cta": "Open to hearing how?" }, "channel": "instagram" }

Expected Output

A valid Instagram Outreach_Message using the refined offer, while remaining grounded in the supplied research and strategy.

Actual Output

Plain channel='instagram' outreach_msg=DM( message='I noticed you’re actively hiring software engineers. Finding the right talent fast can be a real bottleneck. We run a ready-to-run recruitment engine that delivers vetted engineers on demand—companies using it have filled roles up to twice as fast and cut hiring costs by around 30%. It’s backed by 6+ years building hiring systems for tech firms and real case studies. I can share a free, no-commitment demo of the pipeline so you can see it in action.\n\nWhat do you think?' )

Passed Checks

Weak qualification was processed successfully.

Refinement → outreach flow completed without exception.

Final channel is instagram.

Final output was returned successfully.

Output contains a complete Instagram DM.

Failed Checks

Unsupported personal observation: "I noticed you're actively hiring" — the input states the hiring activity but does not establish that the sender personally observed it.

Unsupported consequence: "Finding the right talent fast can be a real bottleneck" is not explicitly supported.

Unsupported offer: "ready-to-run recruitment engine" was not present in the original strategy.

Unsupported mechanism/claim: "delivers vetted engineers on demand" was not supported.

Fabricated proof: "filled roles up to twice as fast" and "cut hiring costs by around 30%" were not supplied.

Fabricated sender proof: "6+ years building hiring systems for tech firms" was not supplied.

Fabricated evidence: "real case studies" was not supplied.

Fabricated low-risk mechanism: "free, no-commitment demo" was not supplied.

CTA deviation: "What do you think?" does not match the supplied CTA "Open to hearing how?".

Grounding failure: refinement produced a materially different offer containing multiple unsupported claims.

Failures

Unsupported personal observation

"I noticed you're actively hiring" — the input states the hiring activity but does not establish that the sender personally observed it.

Unsupported consequence

"Finding the right talent fast can be a real bottleneck" is not explicitly supported.

Unsupported offer

"ready-to-run recruitment engine" was not present in the original strategy.

Unsupported mechanism/claim

"delivers vetted engineers on demand" was not supported.

Fabricated proof

"filled roles up to twice as fast" and "cut hiring costs by around 30%" were not supplied.

Fabricated sender proof

"6+ years building hiring systems for tech firms" was not supplied.

Fabricated evidence

"real case studies" was not supplied.

Fabricated low-risk mechanism

"free, no-commitment demo" was not supplied.

CTA deviation

"What do you think?" does not match the supplied CTA "Open to hearing how?".

Grounding failure

*   Refinement produced a materially different offer containing multiple unsupported claims.

Status

FAIL


# T06 — Weak Offer + Email

=========================

Test Input

Plain
{ "qualification": "weak", "opportunity": { "pain": [ "The company is actively hiring software engineers." ], "fit": "weak", "score": 30 }, "offer": { "problem": "Difficulty hiring software engineers.", "desirable_outcome": "Improve engineering hiring.", "proof": "We provide hiring support.", "low_risk": "Start with a small engagement.", "value": "More efficient engineering recruitment." }, "reason": { "reason": [ "The current offer is weak.", "The opportunity has limited fit." ] }, "angle": { "hooks": [ "Active software engineering hiring" ], "angle": "Help improve engineering hiring efficiency.", "cta": "Open to hearing how?" }, "channel": "email" }

Expected Output

A valid email Outreach_Message with:

channel == "email"

Non-empty subject_line

Complete email body

Refined offer incorporated

No unsupported prospect observations

No fabricated consequences or outcomes

No fabricated sender experience or proof

No invented mechanisms such as a free demo

CTA consistent with the supplied strategy

No exception during refine → outreach flow

Actual Output

Plain
`channel='email'
outreach_msg=DM(
message='Your team is actively hiring software engineers, and scaling that pipeline can get tricky. Many companies hit bottlenecks when trying to keep quality while moving fast. We specialize in hiring support that makes recruitment more efficient, and we can start with a small engagement – even a free demo – to surface quick wins without heavy commitment.

If you’re open to hearing how we could help streamline your hiring process, just reply and we’ll take it from there.'
)`

Failures

Wrong output structure

Returned DM(message=...) instead of an email structure containing subject_line, message, and cta.

Missing subject

No subject_line was returned.

Unsupported consequence

"scaling that pipeline can get tricky" is not explicitly supported.

Unsupported generalization

"Many companies hit bottlenecks when trying to keep quality while moving fast" was not supplied.

Unsupported outcome

"surface quick wins" was not supplied.

Invented mechanism

"even a free demo" was not supplied.

CTA deviation

The supplied CTA was "Open to hearing how?", but the generated CTA is materially different.

Grounding failure

The message introduces multiple claims beyond the research/strategy.

Passed Checks

Refine → outreach flow completed.

Final channel value is "email".

A complete outreach message was returned.

No runtime exception occurred.

Status

FAIL




# T07 — Medium Offer Decision

=========================
Input:
{
  "qualification": "medium",
  "opportunity": {
    "pain": [
      "The company is actively hiring software engineers."
    ],
    "fit": "moderate",
    "score": 60
  },
  "offer": {
    "problem": "Difficulty hiring software engineers efficiently.",
    "desirable_outcome": "Improve engineering hiring efficiency.",
    "proof": "We provide hiring support.",
    "low_risk": "Start with a small engagement.",
    "value": "A more efficient engineering recruitment process."
  },
  "reason": {
    "reason": [
      "The company has a relevant hiring need.",
      "The offer has moderate alignment with the opportunity."
    ]
  },
  "angle": {
    "hooks": [
      "Active software engineering hiring"
    ],
    "angle": "Help improve engineering hiring efficiency.",
    "cta": "Open to hearing how?"
  },
  "channel": "linkedin"
}


Expected Output

A valid LinkedIn Outreach_Message where:

channel == "linkedin"

offerrefine is not called.

Original offer remains unchanged.

Complete LinkedIn DM is returned.

No subject_line is required for LinkedIn.

Message uses only supplied research and strategy.

No unsupported observations, consequences, outcomes, proof, sender claims, or mechanisms are invented.

CTA remains consistent with the supplied strategy.

No exception occurs.

Actual Output

Plain
channel='linkedin' outreach_msg=DM( message='Hi,\n\nI saw you’re actively hiring software engineers. Many tech teams find that a focused, conversion-oriented careers page can shave weeks off the hiring cycle. With 6+ years designing such pages for engineering groups, I’ve helped companies make their recruiting funnel more efficient without a full-scale overhaul.\n\nIf you’re open to it, I can put together a quick mock-up of a careers page tailored to the talent you’re targeting. It’s a low-commitment step – we can start with a free demo and see if it adds value.\n\nLet me know if that sounds useful.' )

Failures

Unsupported personal observation

"I saw you’re actively hiring" — the research states the hiring activity but does not establish firsthand observation.

Invented offer

"conversion-oriented careers page" / "mock-up of a careers page" is not in the supplied offer.

Unsupported consequence

"shave weeks off the hiring cycle" is not supported.

Unsupported generalization

"Many tech teams find..." is not supported.

Fabricated sender proof

"6+ years designing such pages" is not supplied.

Fabricated outcome

"I’ve helped companies make their recruiting funnel more efficient" is not supplied.

Unsupported mechanism

"without a full-scale overhaul" is not supplied.

Invented free demo

"start with a free demo" is not supported.

CTA deviation

"Let me know if that sounds useful" differs from the supplied "Open to hearing how?".

Grounding failure

The message substantially changes the original offer.

Passed Checks

channel == "linkedin".

Refine path was not required by the medium qualification.

A complete LinkedIn DM was returned.

No subject_line was included, which is appropriate for LinkedIn.

Execution completed without an exception.

Status

FAIL


# T08 — Minimal Research
======================
Input

{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company is actively hiring software engineers."
    ],
    "fit": "unclear",
    "score": 70
  },
  "offer": {
    "problem": "Difficulty hiring software engineers efficiently.",
    "desirable_outcome": "Improve engineering hiring efficiency.",
    "proof": "We provide hiring support.",
    "low_risk": "Start with a small engagement.",
    "value": "More efficient engineering recruitment."
  },
  "reason": {
    "reason": [
      "The company is actively hiring software engineers."
    ]
  },
  "angle": {
    "hooks": [
      "Active software engineering hiring"
    ],
    "angle": "Help improve engineering hiring efficiency.",
    "cta": "Open to hearing how?"
  },
  "channel": "instagram"
}



Expected Output
---------------

A valid Instagram Outreach\_Message where:

*   channel == "instagram"
    
*   Complete DM is returned.
    
*   Uses only the single supplied pain point and strategy.
    
*   No additional prospect facts are invented.
    
*   No unsupported consequences, observations, outcomes, proof, sender claims, or mechanisms are added.
    
*   Limited research does not cause fabricated personalization.
    
*   CTA remains consistent with the supplied strategy.
    
*   No exception occurs.
    

Actual Output
-------------
`   channel='instagram'  outreach_msg=DM(    message='Your company is actively hiring software engineers. Many tech firms see their careers pages not delivering enough qualified candidates. We’ve built custom careers-page designs that helped clients lift qualified applicants by about 30% and generate 2-3× more engineering candidates in half the time. I can put together a free demo of a page tailored to your brand—no commitment needed.'  )   `

Failures
--------

*   **Unsupported consequence/problem:** "careers pages not delivering enough qualified candidates" was not in the research.
    
*   **Invented offer:** "custom careers-page designs" was not supplied.
    
*   **Fabricated proof:** "lift qualified applicants by about 30%" was not supplied.
    
*   **Fabricated outcome:** "generate 2-3× more engineering candidates in half the time" was not supplied.
    
*   **Invented mechanism:** "free demo" was not supplied.
    
*   **Unsupported personalization:** "tailored to your brand" was not supported.
    
*   **Grounding failure:** The limited research was expanded into a much more specific scenario and offer.
    

Passed Checks
-------------

*   channel == "instagram".
    
*   Complete DM was returned.
    
*   Execution completed without an exception.
    

Status
------

**FAIL**


# T09 — Multiple Pains
====================

Input:

{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company is actively hiring software engineers.",
      "The company appears to be expanding its engineering team.",
      "The hiring activity may require more efficient candidate outreach."
    ],
    "fit": "strong",
    "score": 85
  },
  "offer": {
    "problem": "Difficulty hiring software engineers efficiently.",
    "desirable_outcome": "Improve engineering hiring efficiency.",
    "proof": "We provide hiring support.",
    "low_risk": "Start with a small engagement.",
    "value": "A more efficient engineering recruitment process."
  },
  "reason": {
    "reason": [
      "The company is actively hiring software engineers.",
      "There are multiple signals related to engineering hiring."
    ]
  },
  "angle": {
    "hooks": [
      "Active engineering hiring",
      "Engineering team expansion"
    ],
    "angle": "Help improve engineering hiring efficiency.",
    "cta": "Open to hearing how?"
  },
  "channel": "facebook"
}

Expected Output
---------------

A valid Facebook Outreach\_Message where:

*   channel == "facebook"
    
*   Complete DM is returned.
    
*   Uses one or more supplied pain points.
    
*   Does not merge the pains into unsupported claims.
    
*   No unsupported consequences or causal relationships.
    
*   No unsupported personal observations.
    
*   No fabricated sender experience, proof, outcomes, or offer mechanisms.
    
*   Stays within the supplied offer and angle.
    
*   CTA remains consistent with "Open to hearing how?".
    
*   No exception occurs.
    

Actual Output
-------------
`   channel='facebook'  outreach_msg=DM(    message='Your team’s recent push to hire more software engineers suggests you’re scaling fast. When hiring ramps up, reaching the right candidates quickly often becomes the biggest bottleneck.\n\nOur recruitment automation tool trims time-to-fill by up to 30%. We’ve helped 15+ fast-growing tech firms cut hiring cycles by 25% on average and achieve 4x higher response rates from passive candidates.\n\nIf a short, no-commitment demo sounds useful, let me know.'  )   `

Failures
--------

*   **Unsupported inference:** "suggests you’re scaling fast" is not explicitly supported.
    
*   **Unsupported consequence:** "reaching the right candidates quickly often becomes the biggest bottleneck" is not supplied.
    
*   **Invented offer:** "recruitment automation tool" was not supplied.
    
*   **Fabricated outcome:** "trims time-to-fill by up to 30%" was not supplied.
    
*   **Fabricated proof:** "helped 15+ fast-growing tech firms" was not supplied.
    
*   **Fabricated metrics:** "cut hiring cycles by 25%" and "4x higher response rates" were not supplied.
    
*   **Invented prospect characteristic:** "fast-growing" was not supplied.
    
*   **Invented mechanism:** "short, no-commitment demo" was not supplied.
    
*   **CTA deviation:** Generated CTA does not match "Open to hearing how?".
    
*   **Grounding failure:** Multiple supplied pains were used as a springboard for unsupported business conclusions and claims.
    

Passed Checks
-------------

*   channel == "facebook".
    
*   Complete Facebook DM returned.
    
*   Execution completed without an exception.
    

Status
------

**FAIL**


# T10 — Unsupported Consequence Trap
==================================

Input:
{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company is actively hiring software engineers."
    ],
    "fit": "strong",
    "score": 85
  },
  "offer": {
    "problem": "Difficulty hiring software engineers efficiently.",
    "desirable_outcome": "Improve engineering hiring efficiency.",
    "proof": "We provide hiring support.",
    "low_risk": "Start with a small engagement.",
    "value": "A more efficient engineering recruitment process."
  },
  "reason": {
    "reason": [
      "The company is actively hiring software engineers."
    ]
  },
  "angle": {
    "hooks": [
      "Active software engineering hiring"
    ],
    "angle": "Help improve engineering hiring efficiency.",
    "cta": "Open to hearing how?"
  },
  "channel": "linkedin"
}

Expected Output
---------------

A valid LinkedIn Outreach\_Message where:

*   channel == "linkedin"
    
*   References only the supported hiring activity.
    
*   Does not introduce unsupported business consequences or causal relationships.
    
*   Does not disguise unsupported claims with "may", "might", "could", or "likely".
    
*   Does not invent observations, outcomes, proof, sender claims, or mechanisms.
    
*   Offer remains consistent with the supplied strategy.
    
*   CTA remains consistent with "Open to hearing how?".
    
*   No exception occurs.
    

Actual Output
-------------
`   channel='linkedin'  outreach_msg=DM(    message='Hey,\n\nI see you’re actively hiring software engineers. Finding the right talent fast is a common bottleneck when scaling. We’ve built an AI-driven sourcing platform that you can try risk-free for two weeks – no commitment, just a live demo of a faster, cheaper hiring pipeline. In pilot projects for fast-growing tech firms, teams that needed 50+ engineers in three months cut time-to-fill by up to 40% and saved around $250K in recruiting spend.\n\nIf you’re open to a quick demo, let me know and I’ll set it up this week.'  )   `

Failures
--------

*   **Unsupported personal observation:** "I see you’re actively hiring" implies firsthand observation.
    
*   **Unsupported consequence:** "Finding the right talent fast is a common bottleneck when scaling" introduces an unsupported consequence.
    
*   **Invented offer:** "AI-driven sourcing platform" was not supplied.
    
*   **Invented mechanism:** "try risk-free for two weeks" was not supplied.
    
*   **Unsupported outcome:** "faster, cheaper hiring pipeline" was not supplied.
    
*   **Fabricated proof:** "pilot projects for fast-growing tech firms" was not supplied.
    
*   **Fabricated prospect/context claim:** "teams that needed 50+ engineers in three months" was not supplied.
    
*   **Fabricated metrics:** "cut time-to-fill by up to 40%" and "saved around $250K" were not supplied.
    
*   **Invented CTA/mechanism:** "quick demo" and "I'll set it up this week" were not supported.
    
*   **CTA deviation:** Does not preserve "Open to hearing how?".
    

Passed Checks
-------------

*   channel == "linkedin".
    
*   Complete LinkedIn DM returned.
    
*   No runtime exception occurred.
    

Status
------

**FAIL**


# T11 — Unsupported Personal Observation Trap
===========================================

Input

{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company is actively hiring software engineers."
    ],
    "fit": "strong",
    "score": 85
  },
  "offer": {
    "problem": "Difficulty hiring software engineers efficiently.",
    "desirable_outcome": "Improve engineering hiring efficiency.",
    "proof": "We provide hiring support.",
    "low_risk": "Start with a small engagement.",
    "value": "A more efficient engineering recruitment process."
  },
  "reason": {
    "reason": [
      "The company is actively hiring software engineers."
    ]
  },
  "angle": {
    "hooks": [
      "Active software engineering hiring"
    ],
    "angle": "Help improve engineering hiring efficiency.",
    "cta": "Open to hearing how?"
  },
  "channel": "instagram"
}

Expected Output
---------------

A valid Instagram Outreach\_Message where:

*   channel == "instagram"
    
*   References the supplied hiring activity **without claiming firsthand observation**.
    
*   Does not use "I noticed", "I saw", "I found", "I looked at...", or equivalent unsupported observation language.
    
*   Does not invent where/how the hiring information was observed.
    
*   No unsupported consequences, outcomes, proof, sender claims, or mechanisms.
    
*   Offer remains consistent with the supplied strategy.
    
*   CTA remains consistent with "Open to hearing how?".
    
*   No exception occurs.
    

Actual Output
-------------
`   channel='instagram'  outreach_msg=DM(    message='Hey, I saw you’re actively hiring software engineers. A lot of tech teams I work with struggle with career pages that don’t attract the right candidates fast enough. I can put together a free demo of a custom, conversion-focused hiring page—built on my 6+ years of web-design experience for tech firms—to show how a modern layout might shorten your hiring cycle.'  )   `

Failures
--------

*   **Unsupported personal observation:** "I saw you’re actively hiring software engineers."
    
*   **Fabricated sender relationship:** "tech teams I work with" was not supplied.
    
*   **Unsupported problem:** "career pages that don’t attract the right candidates fast enough" was not supplied.
    
*   **Invented offer:** "custom, conversion-focused hiring page" was not supplied.
    
*   **Invented mechanism:** "free demo" was not supplied.
    
*   **Fabricated sender proof:** "my 6+ years of web-design experience for tech firms" was not supplied.
    
*   **Unsupported outcome:** "shorten your hiring cycle" was not supported.
    
*   **CTA deviation:** The supplied CTA "Open to hearing how?" was omitted/replaced.
    
*   **Grounding failure:** The output violates the exact personal-observation trap the test is intended to detect.
    

Passed Checks
-------------

*   channel == "instagram".
    
*   Complete Instagram DM returned.
    
*   No exception occurred.
    

Status
------

**FAIL**

# T12 — Unsupported Sender-Proof Trap
===================================

Input:

{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company recently opened several customer support roles.",
      "The company is hiring across multiple support positions."
    ],
    "fit": "strong",
    "score": 88
  },
  "offer": {
    "problem": "Difficulty managing customer support hiring efficiently.",
    "desirable_outcome": "Build a more efficient customer support hiring process.",
    "proof": "We provide hiring support for growing teams.",
    "low_risk": "Start with a small engagement focused on current hiring needs.",
    "value": "A more efficient way to identify and engage relevant support candidates."
  },
  "reason": {
    "reason": [
      "Multiple customer support openings indicate an active hiring need.",
      "The number of open roles creates a relevant opportunity for hiring support."
    ]
  },
  "angle": {
    "hooks": [
      "Multiple customer support openings",
      "Active support-team hiring"
    ],
    "angle": "Help make customer support hiring more efficient while the team is actively recruiting.",
    "cta": "Open to hearing how?"
  },
  "channel": "email"
}



Expected Output
---------------

A valid email Outreach\_Message where:

*   channel == "email"
    
*   Non-empty subject\_line
    
*   Complete email body
    
*   Uses the supplied customer-support hiring context.
    
*   Uses only the supplied sender proof: "We provide hiring support for growing teams."
    
*   Does **not** invent sender experience, clients, case studies, metrics, or previous results.
    
*   Does **not** introduce unrelated services such as portal redesign.
    
*   Does **not** invent a free demo, mock-up, trial, or guarantee.
    
*   Does not introduce unsupported prospect observations or consequences.
    
*   CTA remains consistent with "Open to hearing how?".
    
*   No exception occurs.
    

Actual Output
-------------
`   channel='email'  outreach_msg=DM(    message='Hi,\n\nI saw you’ve opened several customer support roles recently. When hiring ramps up, the speed at which you can identify and engage the right candidates often dictates how quickly the team becomes productive.\n\nWe help teams like yours build a more efficient hiring pipeline – starting with a small, focused engagement on your current openings. As part of that, we can also redesign your support portal to match the new team’s workflow, something that’s delivered proven CSAT improvements for our SaaS clients.\n\nIf a free demo of a custom portal mock-up tailored to your current support flow sounds useful, just reply and I’ll send it over.\n\nThanks,\n[Your Name]'  )   `

Failures
--------

*   **Missing subject line:** Email output has no subject\_line.
    
*   **Wrong output structure:** Returned DM(message=...) rather than the expected email structure.
    
*   **Unsupported personal observation:** "I saw you’ve opened several...".
    
*   **Unsupported consequence:** "often dictates how quickly the team becomes productive".
    
*   **Unsupported sender relationship:** "teams like yours" implies an unsupported similarity/relationship.
    
*   **Invented service:** "redesign your support portal" is outside the supplied offer.
    
*   **Fabricated sender proof:** "our SaaS clients" was not supplied.
    
*   **Fabricated outcome:** "proven CSAT improvements" was not supplied.
    
*   **Invented mechanism:** "free demo" and "custom portal mock-up" were not supplied.
    
*   **Unsupported personalization:** "tailored to your current support flow" was not supported.
    
*   **CTA deviation:** Does not use the supplied "Open to hearing how?".
    
*   **Grounding failure:** Sender proof was expanded into unsupported client history and performance claims.
    

Passed Checks
-------------

*   channel == "email".
    
*   Complete message returned.
    
*   Customer-support hiring context was referenced.
    
*   No runtime exception occurred.
    

Status
------

**FAIL**

# T13 — Conflicting Information
=============================


Input:
{
  "qualification": "medium",
  "opportunity": {
    "pain": [
      "The company is expanding into enterprise sales.",
      "The company recently paused enterprise expansion and is focusing on SMB customers."
    ],
    "fit": "moderate",
    "score": 62
  },
  "offer": {
    "problem": "Difficulty maintaining a consistent sales process while priorities change.",
    "desirable_outcome": "A more consistent sales process aligned with the company's current priorities.",
    "proof": "We help teams structure and improve sales processes.",
    "low_risk": "Start with a small engagement focused on the current sales process.",
    "value": "A clearer and more consistent sales process."
  },
  "reason": {
    "reason": [
      "The research contains conflicting information about the company's current sales direction.",
      "A sales-process improvement offer may still be relevant if the company is actively adjusting its priorities."
    ]
  },
  "angle": {
    "hooks": [
      "Changing sales priorities",
      "Sales-process consistency"
    ],
    "angle": "Help create a more consistent sales process while the company's sales priorities are changing.",
    "cta": "Open to hearing how?"
  },
  "channel": "linkedin"
}


Expected Output
---------------

The message should:

*   Avoid resolving the contradiction between enterprise expansion and SMB focus as if both are simultaneously confirmed.
    
*   Avoid inventing consequences from the conflicting information.
    
*   Stay within the supplied sales-process offer, proof, low-risk mechanism, value, and CTA.
    
*   Avoid unsupported sender experience or personal observations.
    
*   Match the LinkedIn channel and output structure.
    

Actual Output
-------------
`   channel='linkedin' outreach_msg=DM(message='Hi [Name], I saw your team is juggling enterprise expansion and a renewed focus on SMBs. When priorities swing, the sales process can get fragmented, which makes scaling tricky. We’ve helped teams tighten their process without overhauling everything – a short, focused engagement that maps the current workflow and adds a few guardrails. It’s a low-risk way to get a clearer, more consistent sales engine that matches whatever priority you’re on. Open to hearing how?')   `

Failures
--------

*   **Unsupported personal observation:** "I saw your team..." — the input provided conflicting research but did not state that the sender personally observed it.
    
*   **Unsupported consequence:** "the sales process can get fragmented" — fragmentation was not stated in the research or strategy.
    
*   **Unsupported business consequence:** "which makes scaling tricky" — scaling difficulty was not supported.
    
*   **Unsupported sender proof:** "We’ve helped teams tighten their process" — the supplied proof only says "We help teams structure and improve sales processes."
    
*   **Invented mechanism:** "maps the current workflow and adds a few guardrails" — not present in the supplied low-risk mechanism.
    
*   **Modified offer/value:** "sales engine" and "matches whatever priority you're on" extend beyond the supplied offer.
    
*   **Conflict handling issue:** The message converts the contradictory research into a definitive statement that the team is "juggling enterprise expansion and a renewed focus on SMBs" rather than treating the information as uncertain/conflicting.
    
*   Fabricated metrics or numerical claims.
    
*   Fabricated customer results.
    
*   CTA deviation.
    
*   Channel violation.
    

Passed Checks
-------------

*   Channel is correctly linkedin.
    
*   Complete LinkedIn DM was returned.
    
*   No email subject was generated.
    
*   CTA "Open to hearing how?" matches the supplied strategy CTA.
    
*   No runtime exception.
    
*   The message uses the general sales-process theme from the supplied strategy.
    

Status
------

**FAIL**


# T14 — Invalid Channel
=====================


Input:
{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The company recently expanded into three new retail locations."
    ],
    "fit": "strong",
    "score": 84
  },
  "offer": {
    "problem": "Difficulty maintaining consistent inventory operations across locations.",
    "desirable_outcome": "A more consistent inventory process across the new locations.",
    "proof": "We help retail teams improve inventory processes.",
    "low_risk": "Start with a small engagement focused on current inventory operations.",
    "value": "A clearer and more consistent inventory workflow."
  },
  "reason": {
    "reason": [
      "Multiple new locations create a relevant inventory-process opportunity."
    ]
  },
  "angle": {
    "hooks": [
      "Three new retail locations",
      "Inventory consistency"
    ],
    "angle": "Improve inventory-process consistency across newly expanded locations.",
    "cta": "Open to hearing how?"
  },
  "channel": "whatsapp"
}

Expected Output
---------------
`   Input:  {    "channel": "whatsapp"  }   `

The whatsapp value should be rejected by the **upstream Strategy\_result schema**, because the current schema does not define a channel enum, but the downstream outreach\_message prompt only supports:

*   email
    
*   linkedin
    
*   instagram
    
*   facebook
    

Expected behavior: **validation/error should occur before attempting to generate an outreach message for an unsupported channel.**

Actual Output
-------------
`   The invalid-channel input raised an error.   `

Failures
--------

*   **Invalid channel caused an error.**
    
*   Error behavior is explicitly validated at the schema boundary.
    
*   Error identifies whatsapp as an unsupported channel.
    
*   Error is handled gracefully rather than propagating as an unhandled runtime exception.
    
*   No outreach message is generated for the unsupported channel.
    

Passed Checks
-------------

*   Unsupported channel did not result in a misleading Facebook/LinkedIn/Instagram/Email message.
    
*   Invalid input was rejected.
    

Status
------

**FAIL**


# T15 — Missing / Empty Critical Fields
=====================================

Input:
{
  "qualification": "strong",
  "opportunity": {
    "pain": [],
    "fit": "strong",
    "score": 82
  },
  "offer": {
    "problem": "",
    "desirable_outcome": "Improve the consistency of inventory operations.",
    "proof": "We help retail teams improve inventory processes.",
    "low_risk": "Start with a small engagement focused on current inventory operations.",
    "value": "A clearer inventory workflow."
  },
  "reason": {
    "reason": []
  },
  "angle": {
    "hooks": [],
    "angle": "",
    "cta": ""
  },
  "channel": "instagram"
}


Expected Output
---------------

The agent should **not fabricate the missing information**. Since the input contains empty critical fields (pain, offer.problem, reason, angle.hooks, angle.angle, and angle.cta), safe behavior would be to reject the input or return a clear insufficiency/validation error.

Actual Output
-------------
`   channel='instagram' outreach_msg=DM(message='Hey, I help retailers tighten inventory without a tech overhaul. A free demo of our dashboard gives real-time visibility across all sales channels, cuts stockouts and overstock, and streamlines workflow. Retailers who tried it saw inventory errors drop about 30% in three months. Want me to send a quick 2-minute walkthrough?')   `

Failures
--------

*   **Fabricated offer:** "our dashboard" was not supplied.
    
*   **Fabricated mechanism:** "real-time visibility across all sales channels" was not supplied.
    
*   **Unsupported outcomes:** "cuts stockouts and overstock" and "streamlines workflow" were not supplied.
    
*   **Fabricated proof:** "inventory errors drop about 30% in three months" was completely invented.
    
*   **Fabricated low-risk mechanism:** "free demo" was not supplied.
    
*   **Fabricated CTA/mechanism:** "2-minute walkthrough" was not supplied.
    
*   **Fabricated sender positioning:** "I help retailers..." was not supported by the input.
    
*   **Missing-data handling failure:** The model generated a highly specific offer despite critical strategy fields being empty.
    
*   Runtime exception.
    

Passed Checks
-------------

*   Channel remained instagram.
    
*   A complete DM was returned.
    
*   No runtime exception occurred.
    

Status
------

**FAIL**

# T16 — Dependency / LLM Failure
==============================

Input:

{
  "qualification": "strong",
  "opportunity": {
    "pain": [
      "The restaurant group recently expanded to five locations.",
      "Managing reservations consistently across locations is becoming an active operational concern."
    ],
    "fit": "strong",
    "score": 86
  },
  "offer": {
    "problem": "Difficulty maintaining a consistent reservation process across multiple locations.",
    "desirable_outcome": "A more consistent reservation workflow across locations.",
    "proof": "We help restaurant groups improve reservation processes.",
    "low_risk": "Start with a small engagement focused on the current reservation workflow.",
    "value": "A clearer and more consistent reservation process."
  },
  "reason": {
    "reason": [
      "The group has multiple locations with an active reservation-process need.",
      "A focused process improvement engagement is relevant to the stated operational concern."
    ]
  },
  "angle": {
    "hooks": [
      "Five-location expansion",
      "Reservation consistency"
    ],
    "angle": "Improve reservation-process consistency across the group's locations.",
    "cta": "Open to hearing how?"
  },
  "channel": "facebook"
}

Expected Output
---------------

The LLM dependency should fail and the system should return a controlled error. **No outreach message should be generated.**

Actual Output
-------------
`   channel='facebook' outreach_msg=DM(message='Hi, I saw your group recently expanded to five locations – a solid move. Keeping reservations consistent across sites can quickly become a headache. We’ve helped 12 multi-location restaurant groups tighten their reservation workflow and cut errors by about 40%, which makes daily ops smoother. I can set up a free demo of our reservation workflow tool so you can see the impact with zero commitment. Open to hearing how?')   `

Failures
--------

*   **Dependency failure was not demonstrated.** A normal successful LLM response was returned instead.
    
*   **Unsupported personal observation:** "I saw your group recently expanded..." was not stated as a firsthand observation.
    
*   **Unsupported consequence:** "can quickly become a headache" was not supported.
    
*   **Fabricated proof:** "12 multi-location restaurant groups" was invented.
    
*   **Fabricated metric:** "cut errors by about 40%" was invented.
    
*   **Unsupported outcome:** "makes daily ops smoother" was not provided.
    
*   **Invented offer/mechanism:** "reservation workflow tool" and "free demo" were not supplied.
    
*   Controlled dependency error returned.
    
*   No outreach message returned after dependency failure.
    

Passed Checks
-------------

*   Channel is facebook.
    
*   Complete Facebook DM was returned.
    
*   CTA matches the supplied strategy CTA.
    
*   No runtime exception was visible in the returned result.
    

Status
------

**FAIL**