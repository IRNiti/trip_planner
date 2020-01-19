import os
from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

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

#maybe delete this
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Trip
a persistent trip entity, extends the base SQLAlchemy Model
'''
class Trip(db.Model):
  __tablename__ = 'trips'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  flights = db.relationship('Flight', cascade='all,delete-orphan', backref=db.backref('flights', lazy=True, cascade='all'))
  accomodations = db.relationship('Accommodation', cascade='all,delete-orphan', backref=db.backref('accommodations', lazy=True, cascade='all'))

  '''
  insert()
      inserts a new trip into a database
      EXAMPLE
          trip = Trip(
                    name=req_name, 
                    start_date=req_start_date, 
                    end_date=req_end_date)
          trip.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  '''
  update()
      updates a trip record in a database
      the trip id must exist in the database
      EXAMPLE
          trip = Trip.query.filter(Trip.id == id).one_or_none()
          trip.end_date = '2020-02-08T21:40:00'
          trip.update()
  '''
  def update(self):
    db.session.commit()

  '''
  delete()
      deletes a trip record in a database
      the trip id must exist in the database
      EXAMPLE
          trip = Trip.query.filter(Trip.id == id).one_or_none()
          trip.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  format()
      formats trip record to json so it can more easily be consumed by the frontend
  '''
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'start_date': self.start_date,
      'end_date': self.end_date
    }

'''
Flight
a persistent flight entity, extends the base SQLAlchemy Model
'''
class Flight(db.Model):
  __tablename__ = 'flights'

  id = Column(Integer, primary_key=True)
  origin = Column(String)
  destination = Column(String)
  time = Column(DateTime)
  booked = Column(Boolean)
  trip = Column(Integer, db.ForeignKey('trips.id', ondelete="CASCADE"))

  '''
  insert()
      inserts a new flight into a database
      the trip must correspond to a trip id in the database
      EXAMPLE
          flight = Flight(
                      origin=req_origin, 
                      destination=req_destination, 
                      time=req_time,
                      booked=req_booked,
                      trip=req_trip)
          flight.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  '''
  update()
      updates a flight record in a database
      the flight id must exist in the database
      EXAMPLE
          flight = Flight.query.filter(Flight.id == id).one_or_none()
          flight.booked = True
          flight.update()
  '''
  def update(self):
    db.session.commit()

  '''
  delete()
      deletes a flight record in a database
      the flight id must exist in the database
      EXAMPLE
          flight = Flight.query.filter(Flight.id == id).one_or_none()
          flight.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  format()
      formats flight record to json so it can more easily be consumed by the frontend
  '''
  def format(self):
    return {
      'id': self.id,
      'origin': self.origin,
      'destination': self.destination,
      'time': self.time,
      'booked': self.booked,
      'trip': self.trip
    }

'''
Accommodation
a persistent accommodation entity, extends the base SQLAlchemy Model
'''
class Accommodation(db.Model):
  __tablename__ = 'accommodations'

  id = Column(Integer, primary_key=True)
  location = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  booked = Column(Boolean)
  trip = Column(Integer, db.ForeignKey('trips.id', ondelete="CASCADE"))

  '''
  insert()
      inserts a new accommodation into a database
      the trip must correspond to a trip id in the database
      EXAMPLE
          accommodation = Accommodation(
                                      location=req_location,
                                      start_date=req_start_date,
                                      end_date=req_end_date,
                                      booked=req_booked,
                                      trip=req_trip)
          accommodation.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  '''
  update()
      updates an accommodation record in a database
      the accommodation id must exist in the database
      EXAMPLE
          accommodation = Accommodation.query.filter(Accommodation.id == id).one_or_none()
          accommodation.booked = True
          accommodation.update()
  '''
  def update(self):
    db.session.commit()


  '''
  delete()
      deletes an accommodation record in a database
      the accommodation id must exist in the database
      EXAMPLE
          accommodation = Accommodation.query.filter(Accommodation.id == id).one_or_none()
          accommodation.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()


  '''
  format()
      formats accommodation record to json so it can more easily be consumed by the frontend
  '''
  def format(self):
    return {
      'id': self.id,
      'location': self.location,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'booked': self.booked,
      'trip': self.trip
    }
