from flask import Flask
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
connection_string = "mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"\
            .format(db_user=mysql_user, db_password=mysql_password, db_host=mysql_host, db_name=mysql_database)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from model import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()