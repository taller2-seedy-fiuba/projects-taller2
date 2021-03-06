"""20201-07-27 Changes in fav table

Revision ID: faefc4c2e606
Revises: 30c32a5e035b
Create Date: 2021-07-27 08:45:48.997104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'faefc4c2e606'
down_revision = '30c32a5e035b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sponsor_id', sa.String(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sponsor_id'], ['sponsor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('project', 'status',
               existing_type=postgresql.ENUM('in_progres', 'ended', 'pending', 'initialized', name='project_status'),
               type_=sa.Enum('initialized', 'in_progres', 'ended', 'pending', name='project_status'),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'status',
               existing_type=sa.Enum('initialized', 'in_progres', 'ended', 'pending', name='project_status'),
               type_=postgresql.ENUM('in_progres', 'ended', 'pending', 'initialized', name='project_status'),
               existing_nullable=True)
    op.drop_table('favorite')
    # ### end Alembic commands ###
