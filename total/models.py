
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
import pymysql
pymysql.install_as_MySQLdb()

sql_engine = create_engine('mysql://root:root@127.0.0.1:3306/lab7ap', echo=False, pool_size=20, max_overflow=40)
SessionFactory = sessionmaker(bind=sql_engine)
session = scoped_session(SessionFactory)
Base = declarative_base()
metadata = Base.metadata


class Person(Base):
    __tablename__ = "person"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False)
    firstname = Column(String(45), nullable=False)
    lastname = Column(String(45))
    phone_number = Column(String(45))
    email = Column(String(45))
    password = Column(String(100), nullable=False)
    isAdmin = Column(Enum('0', '1'), default='0')
    # fk_personcalendar = Column(BigInteger, ForeignKey('personcalendar.id'))
    # personcalendar = relationship('PersonCalendar', backref='person')


class Calendar(Base):
    __tablename__ = "calendar"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String(45))
    description = Column(Text)
    time_zone = Column(Enum("1", "2"))
    person_id = Column(BigInteger, ForeignKey('person.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    # fk_personcalendar = Column(BigInteger, ForeignKey('personcalendar.id'))
    # personcalendar = relationship('PersonCalendar', backref='calendar')
    events = relationship('Event', backref='calendar')


class PersonCalendar(Base):
    __tablename__ = "personcalendar"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    person_id = Column(BigInteger, ForeignKey('person.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    calendar_id = Column(BigInteger, ForeignKey('calendar.id', ondelete='CASCADE'), nullable=False, primary_key=True)


class Category(Base):
    __tablename__ = "category"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(45), nullable=False)
    events = relationship('Event', backref='category')


class Event(Base):
    __tablename__ = "event"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(1024), nullable=False)
    description = Column(String(2048))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    content = Column(Text)
    calendar_id = Column(BigInteger, ForeignKey('calendar.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    category_id = Column(BigInteger, ForeignKey('category.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    person_id = Column(BigInteger, ForeignKey('person.id', ondelete='CASCADE'), nullable=False, primary_key=True)

