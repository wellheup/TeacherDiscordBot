from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

if not DATABASE_URL:
	raise ValueError("DATABASE_URL environment variable is not set")
if not DATABASE_URL.startswith("postgresql://"):
	raise ValueError("DATABASE_URL must start with 'postgresql://'" + DATABASE_URL)

try:
	connection = psycopg2.connect(DATABASE_URL)
	connection.close()
	print("psycopg2 driver detected and working")
except Exception as e:
	raise ImportError("Error: psycopg2 not installed or database URL incorrect") from e

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()