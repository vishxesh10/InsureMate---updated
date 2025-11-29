"""Add user authentication tables

Revision ID: add_user_auth_tables
Revises: e29fc116ae2b
Create Date: 2025-11-28 10:47:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = 'add_user_auth_tables'
down_revision = 'e29fc116ae2b'
branch_labels = None
depends_on = None

def upgrade():
    # Create enum type for user roles
    op.execute("CREATE TYPE userrole AS ENUM ('user', 'admin')")
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('phone', sa.String(15), nullable=False),
        sa.Column('role', sa.Enum('user', 'admin', name='userrole'), 
                 nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), 
                 nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), 
                 onupdate=sa.text('now()'), nullable=False)
    )
    
    # Add user_id column to prediction_results table
    op.add_column('prediction_results', 
                 sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_prediction_results_user_id',
        'prediction_results', 'users',
        ['user_id'], ['id'],
        ondelete='SET NULL'
    )
    
    # Create index on user_id for better query performance
    op.create_index('idx_prediction_results_user_id', 'prediction_results', ['user_id'])

def downgrade():
    # Drop foreign key constraint
    op.drop_constraint('fk_prediction_results_user_id', 'prediction_results', 
                      type_='foreignkey')
    
    # Drop index
    op.drop_index('idx_prediction_results_user_id', table_name='prediction_results')
    
    # Drop user_id column
    op.drop_column('prediction_results', 'user_id')
    
    # Drop users table
    op.drop_table('users')
    
    # Drop enum type
    op.execute("DROP TYPE userrole")
