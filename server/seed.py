from models import db, Student, Course, Enrollment
from app import app
from sqlalchemy.sql import text as sa_text

with app.app_context():
    Student.query.delete()
    Course.query.delete()
    Enrollment.query.delete()
    # db.session.execute(sa_text('TRUNCATE TABLE enrollments RESTART IDENTITY CASCADE'))
    # db.session.execute(sa_text('TRUNCATE TABLE students RESTART IDENTITY CASCADE'))
    # db.session.execute(sa_text('TRUNCATE TABLE courses RESTART IDENTITY CASCADE'))

    db.session.add_all([
        Student(name="Frank"),
        Student(name="Faith"),
        Student(name="Roy")
    ])

    db.session.add_all([
        Course(name="DS"),
        Course(name="Cyber Sec"),
        Course(name="UI Ux")
    ])

    db.session.commit()

    students = Student.query.all()
    courses = Course.query.all()

    db.session.add_all([
        Enrollment(student=students[0], course=courses[0]),
        Enrollment(student=students[0], course=courses[1]),
        Enrollment(student=students[1], course=courses[0]),
    ])

    db.session.commit()