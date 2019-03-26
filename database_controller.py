from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.String(50), primary_key=True, unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))

    def __str__(self):
        return "[ USER : id: %s, username: %s, password: %s ]".format(self.id, self.username, self.password)


class Timeseries(UserMixin, db.Model):
    id = db.Column(db.String(50), unique=True, primary_key=True)
    sensor_id = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime) # datetime.datetime()
    sensor_data = db.Column(db.Float)

    def __str__(self):
        return "[ TIMESERIES : id: %s, sensor_id: %s, timestamp: %s, sensor_data: %s ]".format(self.id, self.sensor_id, self.timestamp, self.sensor_data)
