from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(10), nullable=False)
    limit = Column(Integer)

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    description = Column(String(256), nullable=False)
    date_time = Column(String(15), nullable=False)
    checked = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

engine = create_engine('sqlite:///database.db')
DBSession = scoped_session(sessionmaker(bind=engine))
Base.metadata.bind = engine
Base.metadata.create_all(engine)


