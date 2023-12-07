from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
import re

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Student(db.Model, SerializerMixin):
    __tablename__ = "student_table"
    serialize_rules = ("-enrollments.student",)
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)

    enrollments = db.relationship("Enrollment", back_populates="student")
    courses = association_proxy("enrollments", "course")


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollment_table"

    serialize_rules = ("-student.enrollments", "-course.enrollments")
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_table.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course_table.id"), nullable=False)
    term = db.Column(db.String, nullable=False)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")




class Course(db.Model, SerializerMixin):
    __tablename__ = "course_table"

    serialize_rules = ("-enrollments.course",)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    instructor = db.Column(db.String)
    credits = db.Column(db.Integer, nullable=False)

    enrollments = db.relationship("Enrollment", back_populates="course")
    students = association_proxy("enrollments", "student")
