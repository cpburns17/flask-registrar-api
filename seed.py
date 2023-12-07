from faker import Faker
from models import Student, Course, Enrollment
from random import choice, randint
from models import db
from app import app


fake = Faker()


def create_students() -> list[Student]:
    students = []
    for _ in range(10):
        fname = fake.name().split(" ")[0]
        lname = fake.name().split(" ")[1]
        students.append(
            Student(fname=fname, lname=lname, grad_year=randint(2023, 2027))
        )
    return students


def create_courses() -> list[Course]:
    courses = []
    for _ in range(10):
        word = fake.text().split(" ")[0]
        courses.append(
            Course(title=word, instructor=fake.name(), credits=choice([1, 3]))
        )
    return courses


def create_enrollments(
    students: list[Student], courses: list[Course]
) -> list[Enrollment]:
    enrollments = []
    for _ in range(10):
        random_student: Student = choice(students)
        random_course: Course = choice(courses)
        random_term: str = choice(["F", "S"]) + str(randint(2023, 2024))
        enrollments.append(
            Enrollment(
                student_id=random_student.id,
                course_id=random_course.id,
                term=random_term,
            )
        )
    return enrollments


with app.app_context():
    Student.query.delete()
    Course.query.delete()
    Enrollment.query.delete()
    db.session.commit()
    students = create_students()
    db.session.add_all(students)
    db.session.commit()
    courses = create_courses()
    db.session.add_all(courses)
    db.session.commit()
    enrollments = create_enrollments(students, courses)
    db.session.add_all(enrollments)
    db.session.commit()
    # import ipdb; ipdb.set_trace()
    print("seeding complete!")
