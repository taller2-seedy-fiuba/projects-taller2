"""Adding columns and removing type table

Revision ID: 19a94fb7ddd3
Revises: b9888e52e087
Create Date: 2021-05-15 18:16:42.294734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19a94fb7ddd3'
down_revision = 'b9888e52e087'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('type')
    op.add_column('project', sa.Column('project_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'creation_date')
    op.drop_column('project', 'state')
    op.drop_column('project', 'project_type')
    op.create_table('type',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('project_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
