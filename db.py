
from flask import Flask, render_template, request, redirect,url_for
from flask import SQLAlchemy






app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///prodwork.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up a 'model' for the data you want to store
from db_schema import db, User

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
      #  dbinit()
