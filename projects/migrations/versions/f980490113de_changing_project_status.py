"""Changing project status

Revision ID: f980490113de
Revises: faefc4c2e606
Create Date: 2021-07-29 11:43:25.138472

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f980490113de'
down_revision = 'faefc4c2e606'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    project_status = postgresql.ENUM('CREATED', 'FUNDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELED', 'NOT_CREATED', 'PENDING', name='project_status_2')
    project_status.create(op.get_bind())
    op.add_column('project', sa.Column('project_status', sa.Enum('CREATED', 'FUNDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELED', 'NOT_CREATED', 'PENDING', name='project_status_2'), nullable=True))
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'project_status')
    # ### end Alembic commands ###
