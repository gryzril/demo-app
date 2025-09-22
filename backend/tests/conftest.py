### Ephemeral DB for tests ###

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from backend.app.schemas import Status
from backend.app.services.task_service import create_task

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    sess = TestingSessionLocal()
    try:
        yield sess
    finally:
        sess.close()

# TODO move or update this to create state for tests
def test_create_task(db_session):
    t = create_task(db_session, user_id=1, title="x", description=None, status=Status.todo, due_date=None, label_ids=[])
    assert t.id > 0