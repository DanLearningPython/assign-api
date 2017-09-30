from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True,
                         nullable=False)


class Client(db.Model):
    name = db.Column(db.String(40))
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)
    client_type = db.Column(db.String(20), default='public')
    _redirect_uris = db.Column(db.Text)
    default_scope = db.Column(db.Text, default='general')

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


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    scope = db.Column(db.Text)

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(250))
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    runscript_url = db.Column(db.String(250))
    runscript_port = db.Column(db.String(25))


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(250))
    year = db.Column(db.Integer())


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    use_date_control = db.Column(db.Boolean, default=False)
    group_submission = db.Column(db.Boolean, default=False)
    students_per_group_min = db.Column(db.Integer, default=0)
    students_per_group_max = db.Column(db.Integer, default=4)
    due_date = db.Column(db.DateTime, nullable=False)
    access_open_date = db.Column(db.DateTime)
    access_close_date = db.Column(db.DateTime)
    submission_open_date = db.Column(db.DateTime)
    submission_close_date = db.Column(db.DateTime)
    submission_enabled = db.Column(db.Boolean, default=False)
    access_enabled = db.Column(db.Boolean, default=False)
    submission_attempts_max = db.Column(db.Integer, default=0)
    allow_not_done = db.Column(db.Boolean, default=False)
    script_enabled = db.Column(db.Boolean, default=False)