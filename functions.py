from datetime import date

from app.db_connect import connect


def get_courses():
    rows = []
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("SELECT courseID, name, description, credits FROM courses ORDER BY name")

    for row in cursor.fetchall():
        rows.append({"courseid": row[0], "name": row[1], "description": row[2], "credits": row[3]})

    conn.close()

    return rows


def get_exams():
    rows = []
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("SELECT c.courseID, c.name, date(e.exam_date) as exam_date, e.exam_length, e.examID "
                   "FROM courses c JOIN exams e ON c.courseID = e.courseID")

    for row in cursor.fetchall():
        rows.append({"courseid": row[0], "name": row[1], "exam_date": row[2], "exam_length": row[3], "examid": row[4],
                     "current_date": date.today()})

    conn.close()

    return rows


def get_students():
    rows = []
    conn = connect()

    cursor = conn.cursor()
    cursor.execute("SELECT s.studentid, s.firstName, s.lastName, s.specialization, s.year, g.grade, g.examID "
                   "FROM Students s JOIN Grades g ON s.studentID = g.studentID")

    for row in cursor.fetchall():
        rows.append({"studentid": row[0], "fName": row[1], "lName": row[2], "specialization": row[3], "year": row[4],
                     "grade": row[5], "examid": row[6]})

    conn.close()

    return rows
