from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name):
        self.name = name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return '<User-{}>'.format(self.name)
