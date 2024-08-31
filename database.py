from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import os
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Fetch the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://user:password@localhost/dbname")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine and handle potential connection issues
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Failed to create SQLAlchemy engine: {e}")
    raise
