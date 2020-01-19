import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Trip, Flight, Accommodation

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrSTNSak5GUWpoRlFUbEVNa1l5UkRjME9FTkVNVGRFT0RGRU1qYzBOakkxTURjNE5UWXdOdyJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktdHJpcC1wbGFubmVyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTFkZTFiZTdhYWM1OTBkMTI1NDEyMzUiLCJhdWQiOiJ0cmlwcyIsImlhdCI6MTU3OTM5Njc5MSwiZXhwIjoxNTc5NDgzMTkxLCJhenAiOiJ1WDJLMngyanBXM3Y0MWswVVZyVThkVTZnWkZ1ZUNycSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjY29tbW9kYXRpb24iLCJjcmVhdGU6ZmxpZ2h0IiwiY3JlYXRlOnRyaXAiLCJkZWxldGU6YWNjb21tb2RhdGlvbnMiLCJkZWxldGU6ZmxpZ2h0IiwiZGVsZXRlOnRyaXAiLCJyZWFkOmFjY29tbW9kYXRpb24iLCJyZWFkOmFjY29tbW9kYXRpb24tZGV0YWlscyIsInJlYWQ6ZmxpZ2h0IiwicmVhZDpmbGlnaHQtZGV0YWlscyIsInJlYWQ6dHJpcCIsInVwZGF0ZTphY2NvbW1vZGF0aW9uIiwidXBkYXRlOmZsaWdodCIsInVwZGF0ZTp0cmlwIl19.gLSwjxtKl_PYhTriGywmEfH5jTc69_qDSKHKkkieLHN7mUaBLEVlPEAchLANmJa6oXCQjZ3uytXQbdeMgTxZP8gdWaYx28ajv1-7qLcrnc9_P56bwdHMmpppg42QOyOQ3p8srbbxuUGVZHZUGks_Bav9Eqtz3boL9bgnfAWLsp9utjE8XsxPiFUNiKp_hINlLa7opW8msSJCB79PZtITw-rF0P4uJhSlBdllkqTxsF6VdD9jFeeNrWeB18iFsvnBFzV_HWeaORZ0RlvPWi7oPB9X3RPAECmk5hW-RuLJoib7s9jYtjqdPlecSD0F_d3lDfeTZ-YXIBVAqlJe43sc-w'

class PlannerTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trip_test"
        self.database_path = "postgresql://postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
          

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test for GET /questions
    def test_succesful_get_trips(self):
        res = self.client().get('/trips', headers={"Authorization": "Bearer "+token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_trips_no_auth(self):
        res = self.client().get('/trips')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()