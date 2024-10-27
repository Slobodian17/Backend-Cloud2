from app import db

person_calendar = db.Table('person_calendar',
    db.Column('person_id', db.BigInteger, db.ForeignKey('person.id')),
    db.Column('calendar_id', db.BigInteger, db.ForeignKey('calendar.id')),
    db.Column('permission', db.Boolean, default=False)
)


class Person(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45))
    phone_number = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45), nullable=False)
    calendars = db.relationship('Calendar', secondary=person_calendar, backref='people')

    def __repr__(self):
        return f'<Person {self.id}>'

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
