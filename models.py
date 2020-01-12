from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#database_path = os.environ['DATABASE_URL']
database_name = "trip"
database_path = "postgresql://postgres@{}/{}".format('localhost:5432', database_name)


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