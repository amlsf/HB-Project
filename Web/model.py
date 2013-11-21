import config
# import bcrypt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

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
    supply_type = Column(String(140), nullable=True)
    date_logged = Column(DateTime, nullable=True)

# ------- Comments -------
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    extra_comment = Column(String(140), nullable=True)

# ------- Creates DB tables -------
def create_tables():
    Base.metadata.create_all(engine)

    user = User()
    session.add(user)

    location = Location()
    session.add(location)
    
    supply = Supply()
    session.add(supply)
    
    comment = Comment()
    session.add(comment)

    session.commit()

if __name__ == "__main__":
    create_tables()