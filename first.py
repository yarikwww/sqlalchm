from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

student_subject_association = Table(
    'student_subject', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id'), primary_key=True),
    Column('lesson_date', DateTime, nullable=False)
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


class StudentSubject(Base):
    __tablename__ = 'student_subject_association'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    lesson_date = Column(DateTime, nullable=False)

    student = relationship('Student', back_populates='subjects')
    subject = relationship('Subject', back_populates='students')

    def __repr__(self):
        return f'<StudentSubject(student_id={self.student_id}, subject_id={self.subject_id}, lesson_date={self.lesson_date})>'



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
