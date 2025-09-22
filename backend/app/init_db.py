from sqlalchemy import inspect
from .db import Base, engine, SessionLocal
from .models import Label, User, Task

# Ensure schema before we do any db magic
def ensure_schema(create_extensions: bool = False):
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Schema created successfully.")
        
        # TODO what create extensions do?
        if create_extensions:
            with engine.begin() as conn:
                conn.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
                   
        # Print out the tables that were created
        with SessionLocal() as session:
            # Use SQLAlchemy's inspect to get the table names
            inspector = inspect(session.bind)  # Use the engine from the session
            tables = inspector.get_table_names()
            print(f"Tables created: {tables}")
                
    except Exception as e:
        print(f"Error during schema creation: {e}")

def reset_schema():
    try:
        # Drop and recreate tables
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Schema reset successfully.")
    except Exception as e:
        print(f"Error during schema reset: {e}")
        
if __name__ == "__main__":
    ensure_schema()
