from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://abdulrahmanalthenayan:postgres@localhost:5432/alembic_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    age = Column(Integer)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)
    year = Column(String, index=True)
    semester = Column(String)