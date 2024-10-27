from app import db
from datetime import datetime


class Event(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    content = db.Column(db.Text)
    calendar_id = db.Column(db.BigInteger, db.ForeignKey('calendar.id'))
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.id'))

    def __repr__(self):
        return f'<Event {self.id}>'

    def __str__(self):
        return self.title
