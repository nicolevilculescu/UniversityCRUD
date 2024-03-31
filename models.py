from app import db
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def get_id(self):
        return self.id


class Courses(db.Model):
    courseid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(164), index=True, unique=True)
    description = db.Column(db.String(164), index=True)
    credits = db.Column(db.Integer)
    exams = db.relationship('Exams', backref='Exams', lazy=True, cascade="all,delete")


class Exams(db.Model):
    examid = db.Column(db.Integer, primary_key=True)
    exam_date = db.Column(db.Date)
    exam_length = db.Column(db.String(164))
    courseid = db.Column(db.Integer, db.ForeignKey('courses.courseid'), nullable=False)
    grades = db.relationship('Grades', backref='exam_grades', lazy=True, cascade="all,delete")


class Students(db.Model):
    studentid = db.Column(db.Integer, primary_key=True)
    lName = db.Column(db.String(164))
    fName = db.Column(db.String(164))
    specialization = db.Column(db.String(164))
    year = db.Column(db.String(164))
    grades = db.relationship('Grades', backref='student_grades', lazy=True, cascade="all,delete")


class Grades(db.Model):
    studentid = db.Column(db.Integer, db.ForeignKey('students.studentid'), primary_key=True, nullable=False)
    examid = db.Column(db.Integer, db.ForeignKey('exams.examid'), primary_key=True, nullable=False)
    grade = db.Column(db.Float)
