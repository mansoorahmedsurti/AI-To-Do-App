"""Add Conversation and Message tables

Revision ID: 001_add_conversation_message_tables
Revises: 
Create Date: 2026-02-08 10:30:00.000000

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers
revision: str = '001_add_conversation_message_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table('conversations',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create messages table
    op.create_table('messages',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('conversation_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('tool_calls', sa.String(), nullable=True),
        sa.Column('tool_responses', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop messages table
    op.drop_table('messages')
    
    # Drop conversations table
    op.drop_table('conversations')