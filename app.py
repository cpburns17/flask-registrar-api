from flask import make_response, jsonify, request, g
from flask import Flask
from models import db, Student, Course, Enrollment

from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def root():
    return "<h1>Registrar</h1>"


@app.get("/students")
def get_students():
    students = Student.query.all()
    student_list = []

    for s in students:
        student_list.append(s.to_dict(rules =['-enrollments']))
    
    return student_list, 200


@app.get('/students/<int:id>')
def get_student_by_id(id):
    student = db.session.get(Student, id)

    if not student:
        return {'error': 'Student not found'}
    
    return student.to_dict()

@app.post('/enrollments')
def add_enrollment():
    try:
        data = request.json
        enrollment = Enrollment(term = data.get('term'), student_id = data.get('student_id'), course_id = data.get('course_id'))
        db.session.add(enrollment)
        db.session.commit()
        return enrollment.to_dict(), 200
    except Exception:
        return {'error', 'Missing info'}, 404
    
@app.patch('/courses/<int:id>')
def update_course(id):
    try:
        data = request.json
        course = db.session.get(Course, id)

        for key in data:
            setattr(course, key, data[key])
            db.session.add(course)
            db.session.commit()
            return course.to_dict(rules = ['-enrollments']), 200
    
    except Exception:
        return {'error': 'cant update'}, 404
    
@app.patch('/student/<int:id>')
def update_student(id):
    try:
        data = request.json
        student = db.session.get(Student, id)
        if not student:
            return {'error': 'student not found'}, 404
        for key in data:
            setattr(student, key, data[key])
            db.session.add(student)
            db.session.commit()
            return student.to_dict(rules = ['-enrollments']), 202
        
    except Exception:
        return {'error': 'idk'}, 400

@app.delete('/students/<int:id>')
def remove_student(id):
    student = db.session.get(Student, id)

    if not student:
        return {'error': 'student not found'}, 404
    
    return {}, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
