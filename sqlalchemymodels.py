import sqlalchemy as sa

metadata = sa.MetaData()

students = sa.Table('students', metadata,
                    sa.Column('students_id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(255)),
                    )
#
teachers = sa.Table('teachers', metadata,
                    sa.Column('teachers_id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.String(255)),
                    )

classes = sa.Table('classes', metadata,
                   sa.Column('classes_id', sa.Integer, primary_key=True),
                   sa.Column('name', sa.String(255)),
                   sa.Column('teachers_id', None, sa.ForeignKey('teachers.teachers_id'))
                   )
#
studentclasses = sa.Table('studentclasses', metadata,
                          sa.Column('student_classes_pkey', sa.Integer, primary_key=True),
                          sa.Column('students_id', None, sa.ForeignKey('students.students_id')),
                          sa.Column('classes_id', None, sa.ForeignKey('classes.classes_id'))
                          )
