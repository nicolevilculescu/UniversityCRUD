from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, DecimalField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class CoursesForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    description = StringField('Course Description')
    credits = StringField('Course Credits', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ExamsForm(FlaskForm):
    exam_date = DateField('Exam Date', format='%Y-%m-%d', validators=[DataRequired()])
    exam_length = DecimalField('Exam Length', validators=[DataRequired()])
    courses = SelectField('Courses', choices=[])
    submit = SubmitField('Submit')
