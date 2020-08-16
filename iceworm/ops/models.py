import sqlalchemy as sa
import sqlalchemy.ext.declarative  # noqa


Base = sa.ext.declarative.declarative_base()


class Epoch(Base):
    __tablename__ = 'epochs'

    id = sa.Column(sa.Integer, primary_key=True)

    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, onupdate=sa.func.now())
