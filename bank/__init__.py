from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

# Create a Flask web application instance.
app = Flask(__name__)

# Configuration of the web application
app.secret_key = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SALT'] = environ.get('SALT')

# Create an SQLAlchemy database instance using the Flask app.
db = SQLAlchemy(app)

from bank import routes