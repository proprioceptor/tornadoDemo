from constants import DATA
from sqlalchemymodels import students, teachers, classes, studentclasses


async def create_tables(conn):
    """
    Asysc function to create intial postgresql tables
    :param conn: db connection object
    :return:
    """
    await conn.execute('DROP TABLE IF EXISTS students CASCADE')
    await conn.execute('DROP TABLE IF EXISTS classes CASCADE')
    await conn.execute('DROP TABLE IF EXISTS teachers CASCADE')
    await conn.execute('DROP TABLE IF EXISTS studentclasses')

    await conn.execute('''CREATE TABLE students (
                                        students_id serial PRIMARY KEY,
                                        name varchar(255))''')
    await conn.execute('''CREATE TABLE teachers (
                                            teachers_id serial PRIMARY KEY,
                                            name varchar(255))''')

    await conn.execute('''CREATE TABLE classes (
                            classes_id serial PRIMARY KEY,
                            name varchar(255),
                            teachers_id int references teachers(teachers_id))''')

    await conn.execute('''CREATE TABLE studentclasses (
                                student_classes_pkey serial PRIMARY KEY,
                              classes_id int REFERENCES classes (classes_id) ON DELETE CASCADE
                                , students_id int REFERENCES students (students_id) ON DELETE CASCADE
                        )''')


async def update_data(conn):
    """
    Function to populate date in the db at the application startup
    :param conn:
    :return:
    """
    for student in DATA.get('students', None):
        await conn.execute(students.insert().values(name=student))
    for teacher in DATA.get('teachers', None):
        await conn.execute(teachers.insert().values(name=teacher))

    for classdata in DATA.get('classes', None):
        for key, values in classdata.items():
            teachername = values.get('teacher', None)
            proxyteacher = await conn.execute(teachers.select().where(teachers.c.name == teachername))
            restid = await proxyteacher.fetchone()
            tid = restid.teachers_id
            proxy = await conn.execute(classes.insert().values(name=key, teachers_id=tid))
            res = await proxy.fetchone()
            classes_id = res.classes_id
            student = values.get('students', [])
            for studentname in student:
                proxystudent = await conn.execute(students.select().where(students.c.name == studentname))
                restud = await proxystudent.fetchone()
                studid = restud.students_id
                await conn.execute(studentclasses.insert().values(classes_id=classes_id, students_id=studid))
