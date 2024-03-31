from flask import render_template, url_for, redirect, flash, session, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db
from app.models import Users, Courses, Exams, Grades
from app.forms import LoginForm, CoursesForm, ExamsForm
from app.functions import *

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    form_username = form.username.data
    form_password = form.password.data

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form_username).first()
        password = user.password

        if user is None or password != form_password:
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)
        session.permanent = True
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    form = CoursesForm()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        credits = request.form.get('credits')
        courses_l = Courses(name=name, description=description, credits=credits)
        db.session.add(courses_l)
        db.session.commit()
        return redirect(url_for('courses'))

    courses_l = get_courses()

    return render_template('courses.html', form=form, courses=courses_l)


@app.route('/course_update/<courseid>/', methods=['GET', 'POST'])
@login_required
def course_update(courseid):
    course = Courses.query.get(courseid)
    course.name = request.form.get('name')
    course.description = request.form.get('description')
    course.credits = request.form.get('credits')
    db.session.commit()
    flash(f"{course.name} has been updated.")
    return redirect(url_for('courses'))


@app.route('/course_delete/<courseid>/', methods=['GET', 'POST'])
@login_required
def course_delete(courseid):
    query = db.session.query(Courses.courseid).filter(Courses.courseid == courseid).subquery()
    db.session.query(Exams).filter(Exams.courseid.in_(query)).delete(synchronize_session=False)
    db.session.query(Courses).filter(Courses.courseid == courseid).delete(synchronize_session=False)
    db.session.commit()
    flash(f"The course has been deleted.")
    return redirect(url_for('courses'))


@app.route('/exams', methods=['GET', 'POST'])
@login_required
def exams():
    form = ExamsForm()

    courses = get_courses()

    form.courses.choices = [(course['courseid'], course['name']) for course in courses]

    if request.method == 'POST':
        exam_length = request.form.get('exam_length')
        exam_date = request.form.get('exam_date')
        courseid = request.form.get('courses')
        exams = Exams(exam_length=exam_length, exam_date=exam_date, courseid=courseid)
        db.session.add(exams)
        db.session.commit()
        return redirect(url_for('exams'))
    exams = get_exams()
    students = get_students()
    return render_template('exams.html', form=form, courses=courses, exams=exams, students=students)


@app.route('/exam_update/<examid>/', methods=['GET', 'POST'])
@login_required
def exam_update(examid):
    exam = Exams.query.get(examid)
    exam.exam_length = request.form.get('exam_length')
    exam.exam_date = request.form.get('exam_date')
    exam.courseid = request.form.get('courses')
    db.session.commit()
    flash(f"The exam has been updated.")
    return redirect(url_for('exams'))


@app.route('/exam_delete/<examid>/', methods=['GET', 'POST'])
@login_required
def exam_delete(examid):
    db.session.query(Exams).filter(Exams.examid == examid).delete()
    db.session.commit()
    flash(f"The exam has been deleted.")
    return redirect(url_for('exams'))


@app.route('/grade_update/<examid>/<studentid>/', methods=['GET', 'POST'])
@login_required
def grade_update(examid, studentid):
    grade = Grades.query.filter_by(examid=examid, studentid=studentid).first()
    if grade:
        grade.grade = request.form.get('grade')
        print(grade.grade)
        db.session.commit()
        flash(f"The grade has been updated.")
    return redirect(url_for('exams'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
