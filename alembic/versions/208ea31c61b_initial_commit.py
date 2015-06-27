"""Initial commit.

Revision ID: 208ea31c61b
Revises: 
Create Date: 2015-05-23 13:39:37.236978

"""

# revision identifiers, used by Alembic.
revision = '208ea31c61b'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=254), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('boon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('debtor_id', sa.Integer(), nullable=True),
    sa.Column('creditor_id', sa.Integer(), nullable=True),
    sa.Column('weight', sa.String(length=20), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.Column('paid_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creditor_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['debtor_id'], ['character.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('boon')
    op.drop_table('user')
    op.drop_table('character')
    ### end Alembic commands ###