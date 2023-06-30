from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set your secret key here
SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="",
    hostname="localhost:3306",
    databasename="flask"
    )
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI #"mysql://root:@localhost:3306/flask"
db = SQLAlchemy(app)
from bloging import views
