from app import db


class Category(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45), nullable=False)
    events = db.relationship('Event', backref='category')

    def __repr__(self):
        return f'<Category {self.id}>'

    def __str__(self):
        return self.title
