from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import psycopg2
try:
	connection = psycopg2.connect(os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname"))
	connection.close()
	print("psycopg2 driver detected and working")
except Exception as e:
	raise ImportError("Error: psycopg2 not installed or database URL incorrect") from e

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()