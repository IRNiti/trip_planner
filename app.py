import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, Trip, Flight, Accommodation
from auth import requires_auth, AuthError

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Homepage placeholder until frontend is in place
    @app.route('/')
    def get_greeting():
        greeting = "Welcome to the Trip Planner app" 
        return greeting

    ## ROUTES

    '''
    GET /trips
        requires the 'read:trip' permission
        returns status code 200 and json {'success': True, 'trips': trips} where trips is the list of trips
    '''
    @app.route('/trips')
    @requires_auth('read:trip')
    def get_trips(jwt):
        trips = Trip.query.all()
        formatted_trips = [trip.format() for trip in trips]

        return jsonify({
            'success': True,
            'trips': formatted_trips
            })

    '''
    GET /flights/<int:flight_id>
        where flight_id is the existing id in the database
        requires the 'read:flight-details' permission
        returns a 404 error if the flight_id is not found
        if successful, returns status code 200 and the flight details in json format
    '''
    @app.route('/flights/<int:flight_id>')
    @requires_auth('read:flight-details')
    def get_flight_details(jwt, flight_id):
        flight = Flight.query.get(flight_id)

        if(flight is None):
            abort(404)

        return jsonify({
            'success': True,
            'flight': flight.format()
            })

    '''
    POST /trips
        creates a new row in the trips table
        requirest the 'create:trip' permission
        the name field is required and route returns a 400 error if this field is missing
        if successful, returns status code 200 and the id of the created trip
    '''
    @app.route('/trips', methods=['POST'])
    @requires_auth('create:trip')
    def create_trip(jwt):
        body = request.get_json()
        name = body.get('name', None)
        start_date = body.get('start_date', None)
        end_date = body.get('end_date', None)

        if(name is None or name == ''):
            abort(400)

        try:
            new_trip = Trip(name=name, start_date=start_date, end_date=end_date)
            new_trip.insert()

            return jsonify({
                'success': True,
                'trip_id': new_trip.id
                })
        except:
            abort(422)

    '''
    POST /flights
        creates a new row in the flights table
        requires the 'create:flight' permission
        the origin, destination and trip fields are required and a 400 error will be thrown if any are missing
        the trip field has to correspond to an existing id in the trips table, otherwise a 400 error is thrown
        if successful, returns status code 200 and the id of the created flight
    '''
    @app.route('/flights', methods=['POST'])
    @requires_auth('create:flight')
    def create_flight(jwt):
        body = request.get_json()
        origin = body.get('origin', None)
        destination = body.get('destination', None)
        time = body.get('time', None)
        booked = body.get('booked', None)
        trip = body.get('trip', None)

        if(origin is None or destination is None or trip is None or origin == '' or destination == '' or trip == ''):
            abort(400)

        db_trip = Trip.query.get(trip)
        if(db_trip is None):
            abort(400)

        try:
            new_flight = Flight(origin=origin, destination=destination, time=time, booked=booked, trip=trip)
            new_flight.insert()

            return jsonify({
                'success': True,
                'flight_id': new_flight.id
                })

        except:
            abort(422)

    '''
    PATCH /flights/<int:flight_id>
        where flight_id is the existing id in the database
        updates time and booked fiels only for the given flight
        requires the 'update:flight' permission
        returns a 404 error if the flight_id is not found
        if successful, returns status code 200 and the updated flight details in json format
    '''
    @app.route('/flights/<int:flight_id>', methods=['PATCH'])
    @requires_auth('update:flight')
    def update_flight(jwt, flight_id):
        flight = Flight.query.get(flight_id)

        if(flight is None):
            abort(404)

        body = request.get_json()
        time = body.get('time', None)
        booked = body.get('booked', None)

        if(time is not None and time != ''):
            flight.time = time
        if(booked is not None and booked != ''):
            flight.booked = booked

        flight.update()

        return jsonify({
            'success': True,
            'flight': flight.format()
            })

    '''
    DELETE /trips/<int:trip_id>
        where trip_id is the existing id in the database
        deletes given trip from the database
        requires the 'delete:trip' permission
        returns a 404 error if the trip_id is not found
        if successful, returns status code 200 and the id of the deleted trip
    '''
    @app.route('/trips/<int:trip_id>', methods=['DELETE'])
    @requires_auth('delete:trip')
    def delete_trip(jwt, trip_id):
        trip = Trip.query.get(trip_id)

        if(trip is None):
            abort(404)

        try:
            trip.delete()

            return jsonify({
                'success': True,
                'trip_id': trip_id
                })
        except:
            abort(422)
        


    ## Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "Could not process request"
                        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "Not found"
                        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(403)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'
        }), 403

    '''
    error handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
            }), error.status_code



    return app

app = create_app()

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8080, debug=True)