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
    return make_response(jsonify({}), 200)


@app.get("/students/<int:id>")
def get_student_by_id(id: int):
    return make_response(jsonify({}), 200)



@app.patch("/students/<int:id>")
def patch_student(id: int):
    return make_response(jsonify({}), 200)

@app.patch("/courses/<int:id>")
def patch_course(id:int):
   return make_response(jsonify({}), 200)

@app.delete("/students/<int:id>")
def delete_student(id: int):
    return make_response(jsonify({}), 200)


@app.post("/enrollments")
def enroll_student(id: int):
    return make_response(jsonify({}), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
