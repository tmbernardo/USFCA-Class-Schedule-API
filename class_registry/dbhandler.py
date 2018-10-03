from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload, relationship, sessionmaker
from sqlalchemy import Table, Column, Integer, BigInteger, String, ForeignKey, Sequence

import os
import sqlalchemy as sql

Base = declarative_base()
engine = sql.create_engine('mysql+mysqlconnector://root:password@db:3306/usf')

# Teachers
class Instructors(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    dept = Column(Integer, nullable=False)

# Departments
class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)

# Students/Users
class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)

# Courses
class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    course_num = Column(Integer, nullable=False)
    section_num = Column(Integer, nullable=False)
    time = Column(String(16), nullable=False)
    days = Column(String(7), nullable=False)
    instructor = Column(Integer, ForeignKey('instructors.id'))
    dept = Column(Integer, ForeignKey('departments.id'))

def start_sess():
    Session = sessionmaker(bind=engine, autocommit=False)
    return Session()

def create_tables():
    sess = start_sess()
    Base.metadata.create_all(engine)
    sess.commit()
    sess.close()

def insert_user(value):
    sess = start_sess()
    
    user = Students(name=value)
    sess.add(user)
    sess.commit()
    sess.close()
    return True
