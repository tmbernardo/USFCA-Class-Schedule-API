from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload, relationship, sessionmaker
from sqlalchemy import Table, Column, Integer, BigInteger, String, ForeignKey, Sequence

import os
import sqlalchemy as sql
import json

Base = declarative_base()
engine = sql.create_engine('mysql+mysqlconnector://root:password@db:3306/usf')

# Instructors
class Instructors(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

# Departments
class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

# Students/Users
class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

# Courses
class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    course_num = Column(Integer, nullable=False)
    section_num = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    actual = Column(Integer, nullable=False)
    course_url = Column(String(256), nullable=False)
    instructor = Column(Integer, ForeignKey('instructors.id'))
    dept = Column(Integer, ForeignKey('departments.id'))

    def serialize(self):
        return {
                'id' : self.id,
                'title' : self.title,
                'course_num' : self.course_num,
                'section_num' : self.section_num,
                'capacity' : self.capacity,
                'actual' : self.actual,
                'course_url' : self.course_url,
                'instructor' : self.instructor,
                'dept' : self.dept
                }

def start_sess():
    Session = sessionmaker(bind=engine, autocommit=False)
    return Session()

def create_tables(sess=start_sess()):
    Base.metadata.create_all(engine)
    sess.commit()
    sess.close()

def instructor_exists(instructor, sess=start_sess()):
    return sess.query(Instructors).filter(Instructors.name==instructor).scalar()

def dept_exists(dept, sess=start_sess()):
    return sess.query(Departments).filter(Departments.name==dept).scalar()

def get_courses(sess=start_sess()):
    query = sess.query(Courses).all()
    dump =  [ row.serialize() for row in query ]
    sess.close()
    return dump

def insert_course(args, sess=start_sess()):
    course = Courses(
            id = args['id'],
            title = args['title'],
            course_num = args['course_num'],
            section_num = args['section_num'],
            capacity = args['capacity'],
            actual = args['actual'],
            course_url = args['course_url'],
            )
    inst = instructor_exists(args['instructor'])
    dep = dept_exists(args['dept'])

    if not inst:
        inst = Instructors(name=args['instructor'])
        sess.add(inst)
        sess.commit()

    if not dep:
        dep = Departments(name=args['dept'])
        sess.add(dep)
        sess.commit()

    course.instructor = inst.id
    course.dept = dep.id
    sess.add(course)
    sess.commit()
    sess.close()
    return True

def insert_student(value, sess=start_sess()):
    user = Students(name=value)
    sess.add(user)
    sess.commit()
    sess.close()
    return True


