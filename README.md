# Prospect AI

An AI-powered prospect intelligence agent that researches prospects through their websites, analyzes their business, evaluates their qualification, and generates personalized outreach messages alongside a comprehensive prospect report.

# Problem

For freelancers, solo professionals, and small agency owners who rely on direct outreach to acquire clients, prospecting can be a time-consuming process.

Manually reviewing potential clients' websites, determining whether they qualify based on the services offered, identifying relevant opportunities, and writing personalized outreach messages requires significant time and effort. 

Repeating this process for every prospect makes consistent and scalable outreach challenging.

# Approach

Prospect AI streamlines this process through an AI-powered prospect research and qualification workflow.

Users submit a prospect's website URL, and the system processes it through the following stages:

1. **Website Extraction:** Extracts relevant information and content from the prospect's website.
2. **Content Processing:** Cleans and structures the extracted content for downstream analysis.
3. **AI Research & Analysis:** Analyzes the prospect's business, services, and relevant business context.
4. **Prospect Qualification:** Evaluates the prospect's suitability and develops an outreach strategy based on the findings.
5. **Personalized Outreach Generation:** Generates a personalized outreach message based on the developed strategy and communication channel selected by the user.
6. **Report Generation:** Produces a comprehensive, downloadable prospect report containing the research findings, qualification assessment, strategy, and generated outreach message.


# Architecture

Prospect AI follows an asynchronous, workflow-driven architecture built around FastAPI, LangGraph, and PostgreSQL. The system separates request handling from AI execution, allowing prospect research and report generation to run in the background while the frontend tracks execution progress.

## AI Prospect End-to-End Workflow
![AI Prospect End-to-End Workflow](assets/ai-prospect-workflow.png)


## Architecture Overview

- **Frontend:** Built with vanilla HTML, CSS, and JavaScript, and hosted on Vercel. It provides the user interface for submitting prospect information and retrieving generated reports.
- **Backend:** FastAPI handles API requests, validates inputs, generates unique run IDs, and manages asynchronous workflow execution.
- **AI Orchestration:** LangGraph combined with custom Python workflows coordinates the end-to-end prospect research pipeline. LLMs handle tool selection, while application logic controls workflow execution, conditional transitions, and retries.
- **Database:** PostgreSQL manages execution state and captures run metadata, including prospect URLs, execution status, timestamps, generated reports, error details, failed phases, and token usage across Gemini and Groq.
- **Deployment:** The frontend is deployed on Vercel, while the backend runs in Docker containers on an Azure Virtual Machine.
- **Observability:** LangSmith provides workflow tracing and monitoring, complemented by application-level logging for execution visibility and debugging.


## Workflow Execution

The AI pipeline follows a sequential, conditional workflow:

1. **Website Extraction:** Fetches the prospect's homepage, discovers relevant website links, selects useful pages such as About, Services, Pricing, and Contact, and extracts their content.
2. **Data Cleaning:** Removes unnecessary HTML elements, converts extracted HTML into clean text, and prepares structured content for analysis.
3. **Research Workflow:** Analyzes the prospect's business, services, industry, location, contact information, people, and business type. Conditionally invokes social bio tool or web search tool
4. **Missing Information Check:** Evaluates whether additional information is required. If necessary, the LLM can invoke the additional research tool to gather missing information.
5. **Strategy Workflow:** Evaluates prospect qualification, generates qualification reasoning, and develops an appropriate offer and outreach strategy.
6. **Outreach Workflow:** Generates a personalized outreach message based on the developed strategy and the communication channel selected by the user.
7. **Offer Refinement:** Conditionally invokes the offer refinement tool when further refinement is required.
8. **Final Report Generation:** Combines the research findings, qualification assessment, strategy, and outreach message into a comprehensive prospect report.


## Workflow-Level Retry & Fallback Handling

Prospect AI implements workflow-level retries with a maximum of three attempts per workflow. When a workflow exhausts its attempts, LangGraph follows a stage-specific fallback path to preserve successfully completed work.

| Failed Workflow | Fallback Behavior |
|---|---|
| Data Cleaning | Routes directly to the workflow's END node. |
| Research | Generates a research-only report using get_research_report. |
| Strategy | Generates a partial report using get_partial_report. |
| Outreach | Generates a partial report using get_partial_report. |

The fallback behavior depends on the stage at which execution fails:

- **Research Failure:** Produces a research-only report containing the available research findings.
- **Strategy or Outreach Failure:** Produces a partial report containing successfully completed earlier stages.
- **Data Cleaning Failure:** Terminates the workflow without proceeding to downstream stages.

These fallback paths allow the LangGraph pipeline to exit through its normal execution flow while preserving available results.

After workflow execution, the backend receives the pipeline result and calls update_complete_record(...) to persist the execution outcome in PostgreSQL.


## Request Lifecycle

1. The frontend submits the prospect URL and offer details to POST /get_input.
2. FastAPI validates the request, generates a unique run_id, and schedules the background task.
3. The API immediately responds with the run_id and queued status.
4. The background task creates a PostgreSQL execution record and starts the LangGraph pipeline.
5. The pipeline executes the extraction, cleaning, research, qualification, strategy, and outreach stages.
6. Execution results and status updates are captured in PostgreSQL, while LangSmith and application logging provide observability.
7. The frontend polls GET /get_report/{run_id} to retrieve execution status and results.
8. Once processing finishes, the API returns the completed report or failure information. Available partial results are retained when execution fails.


## Tech Stack

Prospect AI is built using a Python-based backend, LangGraph orchestration, multiple LLM providers, and PostgreSQL for execution-state management.

| Category | Technology | Purpose |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | User interface and API communication |
| Backend | Python, FastAPI | REST API and asynchronous request handling |
| Validation & Configuration | Pydantic, pydantic-settings | Request validation, schemas, and environment configuration |
| AI Orchestration | LangGraph, Custom Python Workflows | Workflow coordination, conditional execution, and retry handling |
| LLM Provider | Groq — openai/gpt-oss-120b | Prospect research, strategy generation, and web-search reasoning |
| LLM Provider | Google Gemini — gemini-3.5-flash-lite | Additional prospect research and outreach generation |
| LLM Fallback | Google Gemini — gemini-3.1-flash-lite | Automatic fallback when the primary Gemini model fails |
| Web Extraction | Crawl4AI | Website crawling and page fetching |
| HTML Processing | BeautifulSoup4, lxml | HTML parsing and content cleaning |
| HTTP Requests | Python Requests | Basic URL reachability checks |
| Browser Automation | Playwright, Chromium | Browser-based website extraction |
| Database | PostgreSQL | Execution-state tracking and report persistence |
| Database Driver | Psycopg | PostgreSQL connectivity |
| Database Migrations | Alembic | Database schema migrations |
| Monitoring & Tracing | LangSmith | LLM workflow tracing and observability |
| Application Logging | Python Logging | Application-level execution logs and debugging |
| API Rate Limiting | SlowAPI | Request rate limiting |
| Deployment | Docker, Azure VM | Containerized backend deployment |
| Frontend Hosting | Vercel | Frontend hosting |

### Runtime Environments

- Local Development: Python 3.13.7
- Docker Runtime: Python 3.12

### Web Extraction & Research

- Crawl4AI: Website crawling, browser-based page fetching, and content extraction.
- Playwright / Chromium: Underlying browser automation infrastructure used by Crawl4AI.
- BeautifulSoup4 / lxml: HTML parsing and content cleaning.
- Python Requests: Basic URL reachability checks.
- External Search Results: Used by the Groq-powered research workflow to gather information from public forums and credible articles.
- Gemini Additional Research: Performs supplementary prospect research when the initial analysis identifies missing information.


## Key Technology Choices

- **LangGraph:** Provides structured orchestration for sequential workflows, conditional transitions, and stage-level retry and fallback handling.
- **Multiple LLM Providers:** Groq and Google Gemini handle different AI tasks, allowing the system to use different models for research, strategy, and outreach generation.
- **Crawl4AI:** Handles website crawling and relevant page extraction instead of relying exclusively on basic HTTP requests.
- **PostgreSQL:** Provides persistent execution tracking, report storage, and workflow state management.
- **LangSmith:** Helps trace and debug multi-stage LLM execution.
- **Docker:** Provides a consistent and containerized backend deployment environment.


## Key Engineering Decisions & Trade-offs

### 1. FastAPI BackgroundTasks Instead of a Dedicated Task Queue

**Decision:** Used FastAPI's in-process `BackgroundTasks` to execute prospect research workflows asynchronously.

**Rationale:**
- Avoided the additional infrastructure required by Celery (Redis/RabbitMQ and worker processes).
- RQ's process-forking model and Windows limitations introduced unnecessary development and deployment complexity.
- PostgreSQL already provides persistent execution records.
- The 4 GB Azure VM limits practical Chromium concurrency, reducing the immediate benefit of independently scalable workers.

**Trade-off:** BackgroundTasks keeps deployment simple but does not guarantee task durability. Tasks can be lost during application or VM restarts, and worker scaling is limited. A dedicated async queue such as `arq` remains a future option if reliability or workload demands increase.

### 2. PostgreSQL for Persistent Execution Tracking

**Decision:** Used PostgreSQL to store execution states, run metadata, generated reports, errors, and token usage.

**Rationale:**
- Provides persistent execution history across application restarts.
- Supports historical analysis of failures, token consumption, and workflow performance.
- Centralizes execution state and generated outputs without introducing a separate storage system.

**Trade-off:** PostgreSQL adds infrastructure overhead compared to in-memory storage or Redis. However, persistent historical data provides a foundation for evaluating and improving the system.

### 3. Multi-Provider LLM Architecture: Groq + Google Gemini

**Decision:** Distributed LLM responsibilities between Groq and Google Gemini based on observed token limits and output quality.

**Rationale:**
- **Groq:** Handles prospect research, web-search reasoning, and qualification strategy.
- **Gemini:** Handles supplementary research and personalized outreach generation.
- A Groq-only approach encountered token limitations and produced less suitable results for certain tasks.
- Splitting responsibilities allows each provider to handle the workloads where it performed better.

**Trade-off:** Multiple providers introduce additional integration, configuration, and fallback complexity. In return, the architecture offers greater flexibility in managing token limits and output quality.

### 4. Crawl4AI for Website Extraction & BeautifulSoup for Content Cleaning

**Decision:** Combined Crawl4AI for website crawling and extraction with BeautifulSoup4 and `lxml` for HTML parsing and cleaning.

**Rationale:**
- Crawl4AI provides configurable crawling and extraction capabilities for multi-page research.
- BeautifulSoup4 and `lxml` provide established HTML parsing and content-cleaning functionality.
- Separating extraction from content processing keeps responsibilities modular and allows future crawling enhancements.

**Trade-off:** Using separate libraries introduces additional dependencies and processing steps but provides clearer separation of responsibilities.

### 5. Workflow-Level Retries Instead of Retrying the Entire Pipeline

**Decision:** Implemented workflow-level retries (maximum three attempts) with stage-specific fallback paths.

**Rationale:**
- Avoids rerunning successful LLM operations and incurring unnecessary token costs.
- Isolates failures to individual workflows rather than restarting the entire LangGraph pipeline.
- Preserves successful stage outputs for subsequent processing and fallback report generation.
- Keeps retry logic localized and easier to manage.

**Trade-off:** Requires workflow-specific failure handling and fallback logic. Reports may still be incomplete when a stage exhausts its retries, but previously successful results remain available.

### 6. Per-IP API Rate Limiting Using SlowAPI

**Decision:** Implemented IP-based request rate limiting using SlowAPI.

**Rationale:**
- Restricts excessive requests and unnecessary workflow executions.
- Helps control LLM API costs and backend resource consumption.
- Provides lightweight request protection without introducing authentication or a dedicated rate-limiting service.

**Trade-off:** IP-based limits do not provide individual user quotas. Users sharing an IP may affect one another, while requests from different IPs are tracked separately. More granular usage controls may be needed as adoption increases.

### 7. Azure VM & Regional Deployment

**Decision:** Deployed the backend in Docker on an Azure Virtual Machine in the Sweden Central region.

**Rationale:**
- Leveraged an existing Azure subscription to avoid additional cloud-provider costs.
- Selected a region compatible with Groq's deployment restrictions encountered during implementation.
- Provided access to the required B2als VM size.
- Used Docker for consistent runtime environments and simplified deployment.

**Trade-off:** Regional selection was constrained by both VM availability and LLM provider compatibility. The VM's limited resources also restrict concurrent browser sessions and workflow execution.

### 8. Lightweight Frontend Using Vanilla JavaScript

**Decision:** Built the frontend using vanilla HTML, CSS, and JavaScript instead of React or Next.js.

**Rationale:**
- Avoided unnecessary framework dependencies, tooling, and build complexity.
- Enabled faster implementation of the required interface and API interactions.
- Provided sufficient structure for the application's current UI and request lifecycle.

**Trade-off:** Vanilla JavaScript offers less built-in structure as interface complexity grows. A frontend framework may become beneficial as the application expands.

# Testing & Evaluation

Prospect AI was evaluated through two testing phases: baseline functional testing and failure/edge-case testing. The evaluation focused on workflow reliability, generated report quality, execution latency, and system behavior under abnormal conditions.

## 1. Baseline Testing

Baseline testing involved submitting different prospect websites and input configurations to evaluate normal end-to-end workflow execution.

### Results:

| Metric | Observed Result |
|---|---|
| Total executions | 20 |
| Successful workflows | 15/20 (75%) |
| Failed workflows | 5/20 (25%) |
| Reports manually scored | 15 |
| Average manual score | 12.87/18 (71.5%) |
| Median manual score | 13/18 |
| Highest score | 17/18 |
| Lowest score | 9/18 |
| Reports marked usable | 13/20 (65%) |
| Average latency (all attempts) | 61.7 seconds |
| Average latency (successful runs) | 60.7 seconds |

### Failure Breakdown:

- Website extraction failures: 3/20 (15%).
- Workflow execution failures: 2/20 (10%).

These categories account for all five unsuccessful executions.

## 2. Manual Report Quality Evaluation

Successful reports were manually evaluated using a structured scoring rubric (rubric.md), with a maximum score of 18 points.

The evaluation considered:

- Research quality and relevance.
- Prospect qualification and strategy.
- Outreach personalization.
- Offer consistency.
- Input consistency.
- Workflow completion.
- Evidence quality and uncertainty handling.

The average score across 15 evaluated reports was 12.87/18 (71.5%). Additionally, 13 out of 20 total executions were marked as producing usable reports.

## 3. Failure & Edge-Case Testing

A separate failure-testing phase evaluated the system under abnormal conditions to assess input validation, error handling, workflow recovery, and frontend behavior.

### Results:

| Metric | Result |
|---|---|
| Total test cases | 14 |
| Passed | 13 |
| Partial pass | 1 |
| Unresolved failures | 0 |

### Scenarios covered:

- Input validation and malformed URLs.
- Inaccessible websites and extraction failures.
- Research and LLM timeouts.
- Invalid LLM output.
- Partial workflow failures.
- Duplicate submissions.
- Browser refresh during generation.
- Backend unavailability.
- Groq rate limits.
- Large websites and token exhaustion.
- Insufficient extracted content.

Remaining Verification — FT_012:

The insufficient-content scenario requires further verification to ensure the frontend clearly identifies reports with empty or meaningless extracted content as insufficient data, rather than presenting them as normal completed reports.

## 4. Improvements Following Testing

Testing observations led to several improvements:

- Improved URL validation and handling of invalid inputs (FT_002, FT_003).
- Defined and improved frontend behavior when users refresh during workflow execution (FT_010).
- Documented and tested backend-unavailability behavior (FT_011).
- Improved insufficient-data handling and API failure messages (FT_012–FT_014).


## 5. Evaluation Scope

The evaluation currently focuses on manually assessed report quality, workflow completion, failure handling, and execution latency.

Token consumption and per-execution LLM costs have not yet been formally evaluated as part of the baseline testing



# Known Limitations & Next Steps

## Known Limitations

Despite its current capabilities, Prospect AI has several limitations identified during development and testing.

### 1. Website Extraction Limitations

- Complex websites, particularly e-commerce websites with large product catalogs, are not extracted reliably.
- Product-heavy websites can contain large amounts of repetitive or poorly structured content, making it difficult to identify the most relevant business information.

### 2. LLM Research Reliability

- Research results can be inconsistent, particularly in the Services and Company Overview sections.
- Generated content sometimes mixes actual business information with marketing taglines, promotional language, or website copy.
- This can affect the accuracy and usefulness of downstream qualification and strategy generation.

### 3. Execution & Insufficient-Content Handling

- The workflow may continue processing websites containing irrelevant, empty, or insufficient extracted content.
- Such executions can consume additional processing time without producing useful results.
- Frontend handling of these situations needs improvement to communicate insufficient data and execution problems more clearly.

### 4. Infrastructure & Scalability Constraints

- The current Azure VM has limited computational resources, restricting concurrent browser-based extraction and workflow execution.
- Groq has regional availability restrictions that influence deployment choices.
- Groq and Gemini API usage is subject to provider-specific request and usage limits.
- The VM is not operated continuously due to infrastructure costs, affecting application availability.

### 5. Report Quality Limitations

- Report quality degrades when websites provide very limited information.
- Reports generated for certain online stores and product-focused businesses may lack sufficient research depth and useful qualification insights.
- In these cases, the system may struggle to produce relevant offers and personalized outreach.



# Future Improvements

The following areas represent the planned direction for improving Prospect AI:

### 1. Improve Website Extraction & Crawling

Develop better crawling strategies to handle complex websites, product-heavy businesses, and large websites more effectively. Improve content selection and extraction quality to prioritize relevant business information.

### 2. Improve Research Quality & Grounding

Improve research workflows to produce more consistent and evidence-based company overviews and service descriptions. Strengthen the separation between factual business information, promotional website copy, and inferred information.

### 3. Enhance Existing Research & Refinement Tools

Improve existing tools and introduce additional capabilities where necessary to gather missing information, refine research findings, and support more reliable downstream analysis.

### 4. Improve Report Quality

Enhance qualification reasoning, offer relevance, and outreach personalization, particularly for businesses with limited website information or product-focused business models.

### 5. Improve Overall System Design

Refine the system architecture to improve execution reliability, resource utilization, scalability, and workflow management as the application's requirements evolve.


# Run locally

The local development setup runs PostgreSQL in Docker and runs the FastAPI
backend and static frontend directly on the host.

### Prerequisites

Install:

- Python 3.12
- Docker Desktop with Docker Compose
- Git
- A Groq API key (two keys are currently configured by the application)
- A Gemini API key
- A LangSmith API key

Playwright Chromium is installed in a later step.

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
Set-Location YOUR_REPOSITORY
```

Run all remaining commands from the repository root unless stated otherwise.

### 2. Create and activate a virtual environment

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, use a terminal policy approved by your
organization or activate the environment from Command Prompt with
`venv\Scripts\activate.bat`.

### 3. Install Python dependencies and Chromium

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirement.txt
python -m playwright install chromium
```

### 4. Create `.env`

Create a file named `.env` in the repository root. Do not commit it.

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_API_KEY_V2=your_second_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

DB_USER=postgres
DB_PASSWORD=your_local_postgres_password
DB_HOST=localhost
DB_PORT=5432

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=prospect-ai

CORS_ORIGINS=["http://127.0.0.1:5500","http://localhost:5500"]
```

`CORS_ORIGINS` must be a JSON list because it is parsed as `list[str]`.
`DB_HOST=localhost` is required when FastAPI runs on the host. The values for
the API container are overridden to `DB_HOST=postgres` by Compose.

### 5. Start PostgreSQL

From the repository root:

```powershell
docker compose up -d postgres
docker compose ps
```

Wait until the `postgres` service is healthy before continuing. The database is exposed on `localhost:5432`.

### 6. Run database migrations

With the virtual environment still activated:

```powershell
alembic upgrade head
alembic current
```

### 7. Start the FastAPI backend

Open a new terminal, return to the repository root, and activate the
environment again:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

The backend is available at
`http://127.0.0.1:8000`; API documentation is available at
`http://127.0.0.1:8000/docs`.

### 8. Serve the frontend

Open another terminal and run:

```powershell
Set-Location frontend
python -m http.server 5500 --bind 127.0.0.1
```

Open `http://127.0.0.1:5500` in a browser. The frontend is already configured
to call the local backend at `http://127.0.0.1:8000`.

### 9. Stop local services

Stop Uvicorn and the frontend server with `Ctrl+C`, then stop PostgreSQL:

```powershell
docker compose stop postgres
```

## Run the complete backend with Docker Compose

This alternative runs PostgreSQL and FastAPI in containers. It also runs
database migrations automatically before starting the API.

1. Complete steps 1 and 4 above so the repository and `.env` exist.
2. From the repository root, run:

```powershell
docker compose up --build -d
docker compose ps
docker compose logs -f api
```

The API is available at `http://127.0.0.1:8000`. Serve the frontend using
step 8, then open `http://127.0.0.1:5500`.

In this mode Compose uses the service hostname `postgres` internally; do not
change the host-side `.env` value from `localhost` for this purpose.

Stop the containerized services with:

```powershell
docker compose down
```

Add `-v` only if you intentionally want to remove the PostgreSQL data volume.


## Project structure

```text
Prospect-Ai/
├── api/                    # FastAPI application and HTTP endpoints
│   └── main.py
├── assets/                 # Static or supporting project assets
├── config/                 # Settings, logging, and error handling
├── database/               # PostgreSQL access, Redis, schema, and migrations
│   └── migrations/
├── evals/                  # Evaluation datasets and reports
├── frontend/               # Vanilla HTML, CSS, and JavaScript client
├── models/                 # Pydantic schemas and workflow state models
├── outreach/               # Outreach generation and final report logic
├── research/               # Website extraction, cleaning, and research agent
├── strategy/               # Prospect strategy agent
├── tools/                  # Search, media extraction, and supporting tools
├── tests/                  # Automated tests
├── .env                    # Local secrets and runtime configuration
├── alembic.ini             # Alembic migration configuration
├── compose.yml             # PostgreSQL, API services
├── Dockerfile              # Container image definition
├── orchestrator.py         # End-to-end workflow orchestration
├── requirement.txt         # Python dependencies
└── pytest.ini              # Pytest configuration
```

## Contact

**Najam-ul-Hasan**  
AI Engineer | LLM Systems & Workflow Development
