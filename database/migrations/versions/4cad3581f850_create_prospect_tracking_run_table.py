"""create prospect tracking run table

Revision ID: 4cad3581f850
Revises: 0349abee7762
Create Date: 2026-10-18 20:28:29.658840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cad3581f850'
down_revision: Union[str, Sequence[str], None] = '0349abee7762'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """CREATE TABLE prospect_tracking_run(
            run_id UUID PRIMARY KEY,
            prospect_url TEXT NOT NULL,
            status  VARCHAR(20) NOT NULL DEFAULT 'running',
            started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMPTZ,
            final_report JSONB,
            error_type VARCHAR(100),
            error_message TEXT,
            failed_phase VARCHAR(100),
            gemini_tokens BIGINT,
            groq_tokens BIGINT,

            CONSTRAINT ck_tracking_status
                CHECK (status IN ('running', 'completed', 'failed')),
            CONSTRAINT ck_gemini_tokens
                CHECK (gemini_tokens IS NULL OR gemini_tokens >= 0),

            CONSTRAINT ck_groq_tokens
                CHECK (groq_tokens IS NULL OR groq_tokens >= 0)
        );
        
        CREATE INDEX ix_tracking_status
            ON prospect_tracking_run (status);

        CREATE INDEX ix_tracking_started_at
            ON prospect_tracking_run (started_at);

"""
    )



def downgrade() -> None:
    op.execute("""
        DROP INDEX IF EXISTS ix_tracking_started_at;
        DROP INDEX IF EXISTS ix_tracking_status;
        DROP TABLE IF EXISTS prospect_tracking_run;
    """)


