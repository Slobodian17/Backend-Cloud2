from app import db
from enum import Enum


class TimeZones(Enum):
    UTC_plus_1 = 1
    UTC_plus_2 = 2


class Calendar(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    type = db.Column(db.String(45))
    description = db.Column(db.Text)
    time_zone = db.Column(db.Enum(TimeZones))
    events = db.relationship('Event', backref='calendar')

    def __repr__(self):
        return f'<Calendar {self.id}>'
