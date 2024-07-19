from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

student_subject_association = Table(
    'student_subject', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id'), primary_key=True),
    Column('lesson_date', DateTime, nullable=False, default=datetime.utcnow)
)


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    subjects = relationship('Subject', secondary=student_subject_association, back_populates='students')

    def __repr__(self):
        return f'<Student(name={self.name}, age={self.age})>'


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    students = relationship('Student', secondary=student_subject_association, back_populates='subjects')

    def __repr__(self):
        return f'<Subject(name={self.name})>'


DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(
    DATABASE_URL.format(
        host='localhost',
        database='postgres',
        user='postgres',
        password='Allo!2982',
        port=5432,
    )
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


student1 = Student(name='Олег', age=20)
student2 = Student(name='Петро', age=21)
student3 = Student(name='Максим', age=22)


subject1 = Subject(name='математика', description='Математика')
subject2 = Subject(name='англійська мова', description='Англійська мова')
subject3 = Subject(name='історія', description='Історія')


lesson_date = datetime.utcnow()
student1.subjects.append(subject1)  # Олег відвідує математику
student2.subjects.append(subject3)  # Петро відвідує історію
student3.subjects.append(subject2)  # Максим відвідує англійську мову


session.add_all([student1, student2, student3])
session.add_all([subject1, subject2, subject3])


session.commit()

students = session.query(Student).all()
subjects = session.query(Subject).all()

print("Студенти:")
for student in students:
    print(student)

print("\nПредмети:")
for subject in subjects:
    print(subject)

print("\nЗв'язки:")
for student in students:
    for subject in student.subjects:
        print(f'{student.name} відвідує {subject.name}')