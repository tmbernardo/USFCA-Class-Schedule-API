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
    courses = relationship("Courses", back_populates="instructor")
    
    def serialize(self):
        return {'name': self.name,
                'rating': self.rating, 
                'courses': [{
                    'name': course.title,
                    'crn': course.crn,
                    'course_num': course.course_num,
                    'section_num': course.section_num
                    } for course in self.courses]
                }

# Departments
class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    courses = relationship("Courses", back_populates="dept")
    
    def serialize(self):
        return {'name' : self.name,
                'courses': [{
                    'name': course.title,
                    'instructor': course.instructor.name,
                    'crn': course.crn,
                    'course_num': course.course_num,
                    'section_num': course.section_num
                    } for course in self.courses]
                }

# Students/Users
class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

# Courses
class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    crn = Column(Integer, unique=True, nullable=False)
    title = Column(String(64), nullable=False)
    course_num = Column(String(5), nullable=False)
    section_num = Column(String(3), nullable=False)
    capacity = Column(Integer, nullable=False)
    actual = Column(Integer, nullable=False, default=0)
    course_url = Column(String(512), nullable=False)
    dept_id = Column(Integer, ForeignKey('departments.id'))
    dept = relationship("Departments", back_populates="courses")
    inst_id = Column(Integer, ForeignKey('instructors.id'))
    instructor = relationship("Instructors", back_populates="courses")

    def serialize(self):
        return {
                'crn' : self.crn,
                'title' : self.title,
                'course_num' : self.course_num,
                'section_num' : self.section_num,
                'capacity' : self.capacity,
                'actual' : self.actual,
                'course_url' : self.course_url,
                'instructor' : self.instructor.name,
                'dept' : self.dept.name
                }

def start_sess():
    Session = sessionmaker(bind=engine, autocommit=False)
    return Session()

def create_tables(sess=start_sess()):
    Base.metadata.create_all(engine)
    sess.commit()
    sess.close()

def course_exists(crn, sess=start_sess()):
    return sess.query(Courses).filter(Courses.crn==crn).scalar()

def instructor_exists(instructor, sess=start_sess()):
    return sess.query(Instructors).filter(Instructors.name.like(instructor)).scalar()

def dept_exists(dept, sess=start_sess()):
    return sess.query(Departments).filter(Departments.name.like(dept)).scalar()

def get_courses(sess=start_sess()):
    query = sess.query(Courses).all()
    dump =  [row.serialize() for row in query]
    sess.close()
    return dump

def get_instructors(sess=start_sess()):
    query = sess.query(Instructors).all()
    dump = [row.serialize() for row in query]
    sess.close()
    return dump

def get_depts(sess=start_sess()):
    query = sess.query(Departments).all()
    dump =  [row.serialize() for row in query]
    sess.close()
    return dump

def insert_course(args, sess=start_sess()):
    if not course_exists(args['crn'], sess):
        course = Courses(
                crn = args['crn'],
                title = args['title'],
                course_num = args['course_num'],
                section_num = args['section_num'],
                capacity = args['capacity'],
                actual = args['actual'],
                course_url = args['course_url'],
                )
        
        inst = instructor_exists(args['instructor'], sess)
        dep = dept_exists(args['dept'], sess)

        if not inst:
            inst = Instructors(name=args['instructor'])
            sess.add(inst)
            sess.commit()

        if not dep:
            dep = Departments(name=args['dept'])
            sess.add(dep)
            sess.commit()

        inst.courses.append(course)
        dep.courses.append(course)
        course.instructor = inst
        course.dept = dep
        sess.add(course)
        sess.commit()
    sess.close()

def insert_instructor(args, sess=start_sess()):
    if not instructor_exists(args['name'], sess):
        inst = Instructors(name = args['name'])
        sess.add(inst)
        sess.commit()
    sess.close()

def insert_dept(args, sess=start_sess()):
    if not dept_exists(args['name'], sess):
        dept = Departments(name = args['name'])
        sess.add(dept)
        sess.commit()
    sess.close()

def insert_student(value, sess=start_sess()):
    user = Students(name=value)
    sess.add(user)
    sess.commit()
    sess.close()


def update_actual(act, crn,sess=start_sess()):
    course = course_exists(crn, sess)
    
    if course:
        course.actual = act
        sess.commit()
        sess.close()
        return True
    sess.close()
    return False

def delete_course(crn, sess=start_sess()):
    sess = start_sess()
    course = course_exists(crn, sess)

    if course:
        sess.delete(course)
        sess.commit()
        sess.close()
        return course

    sess.close()
    return course

def delete_inst(name, sess=start_sess()):
    sess = start_sess()
    inst = instructor_exists(name, sess)

    if inst:
        sess.delete(inst)
        sess.commit()
        sess.close()
        return True

    sess.close()
    return False

def delete_dept(name, sess=start_sess()):
    sess = start_sess()
    dept = dept_exists(name, sess)

    if dept:
        sess.delete(dept)
        sess.commit()
        sess.close()
        return True

    sess.close()
    return False
