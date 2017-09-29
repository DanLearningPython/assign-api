from flask import Flask
from sqlalchemy import Column, Integer, ForeignKey, String
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
connection_string = "mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"\
            .format(db_user=mysql_user, db_password=mysql_password, db_host=mysql_host, db_name=mysql_database)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Course(db.Model):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    course_name = Column(String(250))
    semester_id = Column(Integer, ForeignKey('semester.id'))
    runscript_url = Column(String(250))
    runscript_port = Column(String(25))


class Semester(db.Model):
    __tablename__ = "semester"
    id = Column(Integer, primary_key=True)
    season = Column(String(250))
    year = Column(Integer())


class AccessToken(db.Model):
    __tablename__ = "access_token"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer())
    token = Column(String(250))


if __name__ == '__main__':
    manager.run()