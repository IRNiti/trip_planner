# Full Stack Capstone Project

## Full Stack Trip Planner

With people travelling more and more, we need tools to help us keep track of the flights and accommodation needed to make our trip the best it could be! This web app does just that! Add trips and then add flights and hotels for your trips and keep track whether they have been booked or not.

## Getting Started

### Pre-requisites and Local Development

This project uses Python3 and Flask for the backend. Authentication is handled by Auth0 through Bearer tokens and RBAC. The frontend for this application has not been implemented yet.

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, you will need to ensure you have pip installed on your maching. Finally, install dependencies by running in the project folder:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trip.psql file provided. From the project folder in terminal run:
```bash
psql trip < trip.psql
```

### Running the server

From within the project directory first ensure you are working using your created virtual environment.

Then set up the environment variables by running from the project folder

```bash
source ./setup.sh
```

Finally, to run the server, execute:

```bash
python app.py
```

### Testing

#### Unit Tests

To run the tests, in the project folder run

```
dropdb trip_test
createdb trip_test
psql trip_test < trip.psql
source ./setup.sh
python test_app.py
```

You can omit the dropdb command the first time you run the tests.

#### RBAC Tests

Two roles have been created in Auth0 to control access to this application: User and Planner. Users can only view trips, flights and accommodation. Planners have full access and can view, create, update and delete any records. Tests have been provided in order to test the different levels of access for the application in Postman. To run the tests, import udacity-trip-planner.postman_collection.json in Postman and run the collection.

## API Reference

### Getting Started

- Base URL: The application is currently hosted on Heroku and can be accessed at https://udacity-trip-planner.herokuapp.com/

- Authentication: Auth0 is handling the authentication through Bearer tokens and RBAC.

### Error Handling

Errors are returned as JSON objects in the following format

```
{
    'success': False,
    'error': 404,
    'message': 'Not found'
}
```

The following error codes can be returned by the application along with the associated error message

* 400
	* Bad request
	* No permissions in payload
	* Unable to parse authentication token
	* Unable to find the appropriate key
* 401
	* No Authorization in header
	* Authorization malformed
	* Incorrect claims. Please, check the audience and issuer
* 403
	* Forbidden
	* User does not have required permission
* 404
	* Not found
* 422
	* Could not process request
* 405
	* Method not allowed
* 500
	* Internal Server Error

### Endpoints

#### GET /trips

Returns a list of all trips in the database in json format as well as the success value (True or False). This route requires the read:trip permission to access. If the user does not have the right permissions, a 403 error will be thrown. If no authorization is provided, a 401 error will be thrown.

##### Example

curl -H "Authorization: Bearer YOUR_TOKEN" http://0.0.0.0:8080/trips

where YOUR_TOKEN contains the appropriate permissions to view trips
```
{
  "success": true,
  "trips": [
    {
      "end_date": "Sat, 08 Feb 2020 00:00:00 GMT",
      "id": 1,
      "name": "Australia",
      "start_date": "Wed, 22 Jan 2020 00:00:00 GMT"
    },
    {
      "end_date": "Sat, 28 Mar 2020 00:00:00 GMT",
      "id": 2,
      "name": "El Salvador",
      "start_date": "Sat, 21 Mar 2020 00:00:00 GMT"
    },
    {
      "end_date": "Sat, 02 May 2020 00:00:00 GMT",
      "id": 3,
      "name": "Romania",
      "start_date": "Fri, 24 Apr 2020 00:00:00 GMT"
    },
    {
      "end_date": "Mon, 01 Jun 2020 00:00:00 GMT",
      "id": 4,
      "name": "France",
      "start_date": "Fri, 22 May 2020 00:00:00 GMT"
    }
  ]
}
```

curl -H "Authorization: Bearer YOUR_TOKEN" http://0.0.0.0:8080/trips

where YOUR_TOKEN does not contain the appropriate permissions to view trips

```
{
  "error": 403,
  "message": "User does not have required permission.",
  "success": false
}
```

curl http://0.0.0.0:8080/trips
```
{
  "error": 401, 
  "message": "No Authorization in header.", 
  "success": false
}
```

#### POST /trips

Create a trip with the provided values for name, start_date and end_date. The name field is required and the route will throw a 400 error if this field is missing. If the trip is succesfully created, the trip id will be returned as well as the success value (True). This route requires the create:trip permission to access. If the user does not have the right permissions, a 403 error will be thrown. If no authorization is provided, a 401 error will be thrown.

##### Example

curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"name": "Canada", "start_date":"2020-02-14","end_date": "2020-02-16"}' http://0.0.0.0:8080/trips

here YOUR_TOKEN contains the appropriate permissions to create trips

```
{
  "success": true, 
  "trip_id": 5
}
```

curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"start_date":"2020-02-14","end_date": "2020-02-16"}' http://0.0.0.0:8080/trips

here YOUR_TOKEN contains the appropriate permissions to create trips

```
{
  "error": 400, 
  "message": "Bad request", 
  "success": false
}
```

See the GET /trips endpoint for examples of auth errors.

#### DELETE /trips/<int:trip_id>

Deletes the trip with the id passed in as an argument. If the given id does not correspond to a trip that exists in the database, a 404 error will be thrown. On the other hand, if the operation is succesful, the success value will be returned in the response as well as the id of the deleted trip. This route requires the delete:trip permission to access. If the user does not have the right permissions, a 403 error will be thrown. If no authorization is provided, a 401 error will be thrown.

##### Example

curl -X DELETE -H "Authorization: Bearer YOUR_TOKEN" http://0.0.0.0:8080/trips/6

here YOUR_TOKEN contains the appropriate permissions to delete trips

```
{
  "success": true, 
  "trip_id": 6
}
```

curl -X DELETE -H "Authorization: Bearer YOUR_TOKEN" http://0.0.0.0:8080/trips/1000

here YOUR_TOKEN contains the appropriate permissions to delete trips

```
{
  "error": 404, 
  "message": "Not found", 
  "success": false
}
```

See the GET /trips endpoint for examples of auth errors.

#### GET /flights/<int:flight_id>

Returns details for the flight with the id passed in as an argument. If the given id does not correspond to a flight that exists in the database, a 404 error will be thrown. On the other hand, if the operation is succesful, the success value will be returned in the response as well as the details for the requested flight in json format. This route requires the read:flight-details permission to access. If the user does not have the right permissions, a 403 error will be thrown. If no authorization is provided, a 401 error will be thrown.

##### Example

curl -H "Authorization: Bearer YOUR_TOKEN" http://0.0.0.0:8080/flights/1

here YOUR_TOKEN contains the appropriate permissions to view flight details

```
{
  "flight": {
    "booked": true, 
    "destination": "San Francisco", 
    "id": 1, 
    "origin": "Sydney", 
    "time": "Sat, 08 Feb 2020 21:40:00 GMT", 
    "trip": 1
  }, 
  "success": true
}
```

curl -H "Authorization: Bearer YOUR_TOKEN" http://0.0.0.0:8080/flights/1000

here YOUR_TOKEN contains the appropriate permissions to view flight details

```
{
  "error": 404, 
  "message": "Not found", 
  "success": false
}
```

See the GET /trips endpoint for examples of auth errors.

#### POST /flights

Create a flight with the provided values for origin, destination, time, trip and booked. The origin, destination and trip fields are required and the route will throw a 400 error if any of these fields are missing. What's more, the trip field must reference the id of a trip that exists in the database. Otherwise, a 400 error will be thrown. If the flight is succesfully created, the flight id will be returned as well as the success value (True). This route requires the create:flight permission to access. If the user does not have the right permissions, a 403 error will be thrown. If no authorization is provided, a 401 error will be thrown.

##### Example

curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"origin": "San Francisco","destination": "Melbourne","trip": 1,"time": "2020-01-21T22:00:00","booked": true}' http://0.0.0.0:8080/flights

here YOUR_TOKEN contains the appropriate permissions to create flights

```
{
  "flight_id": 2, 
  "success": true
}
```

curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"origin": "San Francisco",trip": 1,"time": "2020-01-21T22:00:00","booked": true}' http://0.0.0.0:8080/flights

here YOUR_TOKEN contains the appropriate permissions to create flights

```
{
  "error": 400, 
  "message": "Bad request", 
  "success": false
}
```

curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"origin": "San Francisco","destination": "Melbourne","trip": 1000,"time": "2020-01-21T22:00:00","booked": true}' http://0.0.0.0:8080/flights

here YOUR_TOKEN contains the appropriate permissions to create flights

```
{
  "error": 400, 
  "message": "Bad request", 
  "success": false
}
```

See the GET /trips endpoint for examples of auth errors.

#### PATCH /flights/<int:flight_id>

Update flight with provided id. Only the time and the booked fields can be updated. If the given id does not correspond to a flight that exists in the database, a 404 error will be thrown. On the other hand, if the operation is succesful, the success value will be returned in the response as well as the details for the updated flight in json format. This route requires the update:flight permission to access. If the user does not have the right permissions, a 403 error will be thrown. If no authorization is provided, a 401 error will be thrown.

##### Example

curl -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"booked": false}' http://0.0.0.0:8080/flights/1

here YOUR_TOKEN contains the appropriate permissions to update flights

```
{
  "flight": {
    "booked": false, 
    "destination": "San Francisco", 
    "id": 1, 
    "origin": "Sydney", 
    "time": "Sat, 08 Feb 2020 21:40:00 GMT", 
    "trip": 1
  }, 
  "success": true
}
```

curl -X PATCH -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" --data '{"booked": false}' http://0.0.0.0:8080/flights/1000

here YOUR_TOKEN contains the appropriate permissions to update flights

```
{
  "error": 404, 
  "message": "Not found", 
  "success": false
}
```

See the GET /trips endpoint for examples of auth errors.