import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Trip, Flight, Accommodation

token = os.environ['TEST_TOKEN']

class PlannerTestCase(unittest.TestCase):
    """This class represents the planner test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_TEST_URL']
        setup_db(self.app, self.database_path)
        #db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
          

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test for GET /trips
    def test_succesful_get_trips(self):
        res = self.client().get('/trips', headers={"Authorization": "Bearer "+token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test for GET /trips
    def test_get_trips_no_auth(self):
        res = self.client().get('/trips')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # test for POST /trips
    def test_succesful_create_trip(self):
        body = {
            "name": "Australia",
            "start_date": "2020-01-22",
            "end_date": "2020-02-08"
        }
        res = self.client().post('/trips', headers={"Authorization": "Bearer "+token}, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trip_id'])

    # test for POST /trips
    def test_create_trip_no_name(self):
        body = {
            "start_date": "2020-01-22",
            "end_date": "2020-02-08"
        }
        res = self.client().post('/trips', headers={"Authorization": "Bearer "+token}, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test for POST /flights
    def test_succesful_create_flight(self):
        body = {
            "origin": "Sydney",
            "destination": "San Francisco",
            "trip": 1,
            "time": "2020-02-08T21:40:00",
            "booked": True
        }
        res = self.client().post('/flights', headers={"Authorization": "Bearer "+token}, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['flight_id'])

    # test for POST /flights
    def test_create_flight_inexistent_trip(self):
        body = {
            "origin": "Sydney",
            "destination": "San Francisco",
            "trip": 1000,
            "time": "2020-02-08T21:40:00",
            "booked": True
        }
        res = self.client().post('/flights', headers={"Authorization": "Bearer "+token}, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test for GET /flights/<int:flight_id>
    def test_succesful_get_flight_details(self):
        res = self.client().get('/flights/1', headers={"Authorization": "Bearer "+token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['flight'])

    # test for GET /flights/<int:flight_id>
    def test_get_flight_details_inexistent_flight(self):
        res = self.client().get('/flights/1000', headers={"Authorization": "Bearer "+token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # test for PATCH /flights/<int:flight_id>
    def test_succesful_update_flight(self):
        body = {
            "booked": False
        }
        res = self.client().patch('/flights/1', headers={"Authorization": "Bearer "+token}, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['flight'])

    # test for PATCH /flights/<int:flight_id>
    def test_update_inexistent_flight(self):
        body = {
            "booked": False
        }
        res = self.client().patch('/flights/1000', headers={"Authorization": "Bearer "+token}, json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # test for DELETE /trips/<int:trip_id>
    def test_succesful_delete_trip(self):
        to_delete = Trip.query.order_by(Trip.id.desc()).first()
        res = self.client().delete('/trips/'+str(to_delete.id), headers={"Authorization": "Bearer "+token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trip_id'])

    # test for DELETE /trips/<int:trip_id>
    def test_delete_inexistent_trip(self):
        res = self.client().delete('/trips/1000', headers={"Authorization": "Bearer "+token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()