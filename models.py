from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
#database_name = "trip"
#database_path = "postgresql://postgres@{}/{}".format('localhost:5432', database_name)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Trip(db.Model):
  __tablename__ = 'trips'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  flights = db.relationship('Flight', cascade='all,delete-orphan', backref=db.backref('flights', lazy=True, cascade='all'))
  accomodations = db.relationship('Accommodation', cascade='all,delete-orphan', backref=db.backref('accommodations', lazy=True, cascade='all'))

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'start_date': self.start_date,
      'end_date': self.end_date
    }


class Flight(db.Model):
  __tablename__ = 'flights'

  id = Column(Integer, primary_key=True)
  origin = Column(String)
  destination = Column(String)
  time = Column(DateTime)
  booked = Column(Boolean)
  trip = Column(Integer, db.ForeignKey('trips.id', ondelete="CASCADE"))

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'origin': self.origin,
      'destination': self.destination,
      'time': self.time,
      'booked': self.booked,
      'trip': self.trip
    }


class Accommodation(db.Model):
  __tablename__ = 'accommodations'

  id = Column(Integer, primary_key=True)
  location = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  booked = Column(Boolean)
  trip = Column(Integer, db.ForeignKey('trips.id', ondelete="CASCADE"))

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'location': self.location,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'booked': self.booked,
      'trip': self.trip
    }



