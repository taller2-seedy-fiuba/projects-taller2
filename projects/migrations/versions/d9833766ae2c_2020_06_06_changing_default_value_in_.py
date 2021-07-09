"""2020-06-06-Changing default value in status, adding location

Revision ID: d9833766ae2c
Revises: 3d766fdd32b8
Create Date: 2021-07-07 19:03:34.062145

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from projects.model import ProjectStatus
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'd9833766ae2c'
down_revision = '3d766fdd32b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('point', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326, from_text='ST_GeogFromText', name='geography'), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('project', sa.Column('wallet_id', sa.String(), nullable=True))
    op.drop_column('project', 'location')
    op.drop_column('project','status')
    
    status_enum = postgresql.ENUM(
        'in_progres', 'ended', 'pending', 'initialized', name='project_status'
    )
    status_enum.create(op.get_bind())
    
    op.add_column(
        'project',
        sa.Column(
            'status',
            status_enum,
            nullable=False,
            default=ProjectStatus.initialized.value,
        ),
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('location', sa.VARCHAR(), nullable=True))
    op.drop_column('project', 'wallet_id')
    op.drop_table('location')
    # ### end Alembic commands ###