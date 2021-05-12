"""changing column name for type

Revision ID: 24b8bab70098
Revises: 0e23f982e5bf
Create Date: 2021-05-12 18:41:56.303299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24b8bab70098'
down_revision = '0e23f982e5bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("project") as batch_op:
        batch_op.alter_column('type', new_column_name='project_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
     with op.batch_alter_table("project") as batch_op:
        batch_op.alter_column('project_type', new_column_name='type')

    # ### end Alembic commands ###
