# conftest.py
#
# In-memory SQLite requires StaticPool to be shared across threads.
# Starlette 1.1 / anyio runs the ASGI app in a worker thread distinct from
# the pytest fixture thread.  Without StaticPool every thread gets its own
# private in-memory database, so tables created in the fixture thread are
# invisible to the handler thread ("no such table").
#
# This conftest wraps create_engine so that any sqlite:///:memory: engine
# created during the test session automatically uses StaticPool.

import sqlalchemy as _sa
from sqlalchemy.pool import StaticPool as _StaticPool

_real_create_engine = _sa.create_engine


def _create_engine_with_static_pool(url, **kwargs):
    if ":memory:" in str(url):
        kwargs.setdefault("poolclass", _StaticPool)
    return _real_create_engine(url, **kwargs)


_sa.create_engine = _create_engine_with_static_pool
