CREATE TYPE status AS ENUM(
    'running',
    'success',
    'failed',
    'timeout'
);

CREATE TYPE error_type AS ENUM (
    'research',
    'strategy',
    'outreach',
    'llm_api_error',
    'output_validation_failure',
    'retry_exhausted',
    'unknown_error'
);


CREATE TABLE RUNS(
    id UUID,
    url TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ NULL,
    status status,
    error_type error_type NULL,
    retry_count INTEGER,
    total_token_used INTEGER,
    estimated_cost NUMERIC,
    latency_seconds DOUBLE PRECISION
);