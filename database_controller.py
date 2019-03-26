from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.String(50), primary_key=True, unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __str__(self):
        return "[ USER : id: {0}, username: {1}, password: {2} ]".format(self.id, self.username, self.password)


class Timeseries(UserMixin, db.Model):
    id = db.Column(db.String(50), unique=True, primary_key=True)
    sensor_id = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime) # datetime.datetime()
    sensor_data = db.Column(db.Float)

    def __str__(self):
        return "[ TIMESERIES : id: {0}, sensor_id: {1}, timestamp: {2}, sensor_data: {3}]".format(self.id, self.sensor_id, self.timestamp, self.sensor_data)
