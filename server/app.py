from flask import Flask, send_file, request, jsonify,make_response
from models import db, Student, Course, Enrollment
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migration = Migrate(app, db)

@app.before_request
def beforerequest():
    authed = False
    if request.path.startswith("/uploads") and authed == False:
        return "Prouted route. you need to be logged in", 403


@app.route("/")
def home():
    return send_file("./static/index.html")

@app.route("/uploads/<string:filename>")
def uploads(filename):
    return send_file(f"./uploads/{filename}")

@app.route('/students', methods=['GET','POST'])
def students():
    if request.method == 'GET':
        students = Student.query.all()
        students_data = [student.to_dict() for student in students]

        return students_data, 200
    
    elif request.method == 'POST':
        new_student =Student(
            name = request.json.get('name'),
            age = request.json.get('age')
        )
        db.session.add(new_student)
        db.session.commit()
        
        response = make_response(
            new_student.to_dict(),
            201
        )
        return response

@app.route('/students/<int:id>')
def students_by_id(id):
    student = Student.query.filter(Student.id == id).first()
    if student:
        response = make_response(
            student.to_dict(),
            200
        )
        return response
    else:
        response_body={
            "message": "Student doesn't exists"
        }
        response = make_response(
            response_body,
            404
        )
        return response


# GET, POST
@app.route('/courses',methods=['GET','POST'])
def courses():
    if request.method == 'GET':
        courses = [course.to_dict() for course in Course.query.all()]    
        return make_response(
            courses,
            200
        )
        
        # courses = Course.query.all()
        # courses_array =[]
        # for course in courses:
        #     course_dict = course.to_dict()
        #     courses_array.append(course_dict)
    
    elif request.method == 'POST':
        new_course =Course(
            name = request.json.get('name')
        )
        db.session.add(new_course)
        db.session.commit()
        
        response = make_response(
            new_course.to_dict(),
            201
        )
        return response
        
# GET, POST, DELETE

@app.route('/enrollments',methods=['GET','POST'])
def enrollments():
    if request.method == 'GET':
        enrollments = [enrollment.to_dict() for enrollment in Enrollment.query.all()]
        return make_response(
            enrollments,
            200
        )
    
    elif request.method == 'POST':
        new_enrollment = Enrollment(
            student_id =request.json.get('student_id'),
            course_id= request.json.get('course_id')
        )
        db.session.add(new_enrollment)
        db.session.commit()
        
        return make_response(
            new_enrollment.to_dict(),
            201
        )

@app.route('/enrollments/<int:id>', methods=['GET','DELETE'])
def enrollments_by_id(id):
    enrollment = Enrollment.query.filter(Enrollment.id == id).first()
    if request.method == 'GET':
        return make_response(
            enrollment.to_dict(),
            200
        )
    elif request.method == 'DELETE':
        db.session.delete(enrollment)
        db.session.commit()
        
        response_body={
            "deleted_successfully": True,
            "message": "Enrollment successfully deleted!"
        }
        return make_response(
            response_body,
            200
        )
        
        
    
        
        

        

if __name__ == '__main__':
    app.run(port=5555,debug=True)

# MISSING MODULE psycopg2

