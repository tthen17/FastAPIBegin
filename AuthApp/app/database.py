from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://abdulrahmanalthenayan:postgres@localhost:5432/auth_test" #connecting to postgresdb

engine = create_engine(
    SQLALCHEMY_DATABASE_URL #connect_args only needed for sqlite
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #initiating db session