import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    #comment after first init since wipes the db clean
    #db_drop_and_create_all()
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        greeting = "Hello" 
        return greeting

    return app

app = create_app()

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8080, debug=True)