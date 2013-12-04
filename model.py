import config
# import bcrypt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
# from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

# ------- Master table ------- 
class Master(Base):
    __tablename__ = "master"
    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=True)
    email = Column(String(140), nullable=True)
    phone_num = Column(String(140), nullable=True)
    full_address = Column(String(300), nullable=True)
    lat = Column(Integer, nullable=True)
    lng = Column(Integer, nullable=True)
    supply_type = Column(String(300), nullable=True)
    extra_comment = Column(String(300), nullable=True)

# ------- User info ------- 
class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=True)
    email = Column(String(140), nullable=True)
    phone_num = Column(String(140), nullable=True)

# ------- Location -------
class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    full_address = Column(String(300), nullable=True)
    lat = Column(Integer, nullable=True)
    lng = Column(Integer, nullable=True)

# ------- Supply -------
class Supply(Base):
    __tablename__ = "supply"
    id = Column(Integer, primary_key=True)
    supply_type = Column(String(300), nullable=True)
    date_logged = Column(DateTime, nullable=True)

# ------- Comments -------
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    extra_comment = Column(String(300), nullable=True)

# ------- Creates DB tables -------
def create_tables():
    Base.metadata.create_all(engine)
    session.commit()

# ------- Connects DB -------
def connect():
    engine = create_engine(config.DB_URI, echo=False) 
    session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))
    return session

if __name__ == "__main__":
    create_tables()