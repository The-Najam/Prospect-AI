"""drop prospect tracking run table

Revision ID: 0349abee7762
Revises: 75e64dc25c49
Create Date: 2026-10-18 20:26:35.444526

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '0349abee7762'
down_revision: Union[str, Sequence[str], None] = '75e64dc25c49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op

def upgrade():
    op.drop_table(
        "prospect_tracking_run",
        schema="public"
    )

def downgrade():
    pass
