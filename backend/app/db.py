from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session

# TODO what dis?
class Base(DeclarativeBase):
    pass

# Connection string
DATABASE_URL = "postgresql+psycopg://app:app@db:5432/app"


# pool_pre_ping: TODO ADD
# future: TODO ADD
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    connect_args={"connect_timeout": 5},
)

# autocommit: TODO ADD
# autoflush: TODO ADD
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def get_db():
    db = SessionLocal()
    try:
        # execute through errors
        yield db
    finally:
        db.close()