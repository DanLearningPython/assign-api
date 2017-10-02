from config import *
from sqlalchemy import create_engine, Column, DateTime, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, index=True,
                         nullable=False)


class Client(Base):
    __tablename__ = 'Client'
    name = Column(String(40))
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), unique=True, index=True,
                              nullable=False)
    client_type = Column(String(20), default='public')
    _redirect_uris = Column(Text)
    default_scope = Column(Text, default='general')

    @property
    def user(self):
        return User.query.get(1)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split()
        return []


class Token(Base):
    __tablename__ = 'Token'
    id = Column(Integer, primary_key=True)
    client_id = Column(String(40), ForeignKey(Client.client_id))
    user_id = Column(Integer, ForeignKey(User.id))
    token_type = Column(String(40))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    expires = Column(DateTime)
    scope = Column(Text)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []

class Semester(Base):
    __tablename__ = 'Semester'
    id = Column(Integer, primary_key=True)
    season = Column(String(250))
    year = Column(Integer())


class Course(Base):
    __tablename__ = 'Course'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(250))
    semester_id = Column(Integer, ForeignKey(Semester.id))
    semester = relationship("Semester", backref="Course")
    assignments = relationship("Assignment", backref="Course", cascade="all", lazy="joined")
    runscript_url = Column(String(250))
    runscript_port = Column(String(25))


class Assignment(Base):
    __tablename__ = 'Assignment'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Course.id))
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    use_date_control = Column(Boolean, default=False)
    group_submission = Column(Boolean, default=False)
    students_per_group_min = Column(Integer, default=0)
    students_per_group_max = Column(Integer, default=20)
    due_date = Column(DateTime, nullable=False)
    access_open_date = Column(DateTime)
    access_close_date = Column(DateTime)
    submission_open_date = Column(DateTime)
    submission_close_date = Column(DateTime)
    submission_enabled = Column(Boolean, default=False)
    access_enabled = Column(Boolean, default=False)
    submission_attempts_max = Column(Integer, default=0)
    allow_not_done = Column(Boolean, default=False)
    script_enabled = Column(Boolean, default=False)


class Database():
    def connect(self):

        connection_string = "mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}" \
            .format(db_user=mysql_user, db_password=mysql_password, db_host=mysql_host, db_name=mysql_database)

        return connection_string

db_connect = Database()
connection_string = db_connect.connect()

engine = create_engine(connection_string)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)