from class_registry import dbhandler as db
from flask import Flask
from flask_restful import Resource, Api, reqparse

import json
import markdown
import re
import os
import sys
import time

app = Flask(__name__)

api = Api(app)

@app.before_first_request
def _run_on_start():
    for _ in range(60):
        try:
            db.create_tables()
            print('Database schema created', file=sys.stdout)
            return
        except Exception as e:
            time.sleep(1)
            continue
    print('TIMEOUT: could not connect to database after 1 minute', file=sys.stderr)

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)

class CourseList(Resource):
    def get(self):
        return {'message': 'Success' , 'data': db.get_courses()}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('crn', required = True)
        parser.add_argument('title', required = True)
        parser.add_argument('course_num', required = True)
        parser.add_argument('section_num', required = True)
        parser.add_argument('capacity', required = True)
        parser.add_argument('actual', required = True)
        parser.add_argument('course_url', required = True)
        parser.add_argument('instructor', required = True)
        parser.add_argument('dept', required = True)

        args = parser.parse_args()

        db.insert_course(args)
        
        return {'message': 'Course registered', 'data': args}, 201

class InstructorList(Resource):
    def get(self):
        return {'message': 'Success', 'data': db.get_instructors()}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required = True)
        
        args = parser.parse_args()
        db.insert_instructor(args)

        return{'message': 'Success', 'data': args}, 201

class Instructor(Resource):
    def get(self, name):
        cleaned = re.sub("[\W+]", "_", name)
        inst = db.instructor_exists(cleaned)

        if not inst:
            return {'message': 'Instructor not found', 'data': {}}, 404

        return {'message': 'Success' , 'data': inst.serialize()}, 200

class Course(Resource):
    def get(self, crn):
        course = db.course_exists(crn)

        if not course:
            return {'message': 'Course not found', 'data': {}}, 404

        return {'message': 'Course found', 'data': course.serialize()}, 200


api.add_resource(CourseList, '/courses')
api.add_resource(InstructorList, '/instructors')
api.add_resource(Instructor, '/instructors/<string:name>')
api.add_resource(Course, '/courses/<int:crn>')

