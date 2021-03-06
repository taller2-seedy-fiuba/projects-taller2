"""Adding sponsor table

Revision ID: 60751180e888
Revises: 923b45c6d38c
Create Date: 2021-06-09 21:09:08.790988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60751180e888'
down_revision = '923b45c6d38c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sponsor',
    sa.Column('id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_sponsor_association',
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('sponsor_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['sponsor_id'], ['sponsor.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_sponsor_association')
    op.drop_table('sponsor')
    # ### end Alembic commands ###
