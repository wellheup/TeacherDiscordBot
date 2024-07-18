from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import psycopg2

# Fetch the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://user:password@localhost/dbname")
if DATABASE_URL.startswith("postgres://"):
	DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# # Verify psycopg2 connection
# try:
# 	connection = psycopg2.connect(DATABASE_URL)
# 	connection.close()
# 	print("psycopg2 driver detected and working")
# except Exception as e:
# 	raise ImportError("Error: psycopg2 not installed or database URL incorrect") from e

# Create SQLAlchemy engine and handle potential connection issues
try:
	engine = create_engine(DATABASE_URL, pool_pre_ping=True)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	Base = declarative_base()
except Exception as e:
	print(f"Failed to create SQLAlchemy engine: {e}")
	raise