from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# instantiate data base
class Users(db.Model):
    __tablename__ = 'Users'
    # map instnaces of user class to users table within database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True)
    type = db.Column(db.String(20))



    def __init__(self, username, password, email, type):
        self.username = username
        self.password = password
        self.email = email
        self.type =type

class Events(db.Model):
    __tablename__ = 'Events'
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    date = db.Column(db.String(20))
    start_time = db.Column(db.String(30))
    duration=db.Column(db.Integer)
    capacity=db.Column(db.Integer)
    location=db.Column(db.String(20))
    tickets=db.Column(db.Integer)

    def __init__(self, name,date,time,duration,location,capacity):
        self.name = name
        self.date = date
        self.start_time = time
        self.duration = duration
        self.capacity=capacity
        self.location=location
        self.tickets=capacity

    # constructor for object

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    reference=db.Column(db.Integer, unique=True)
    barcode_filename = db.Column(db.String(255),unique=True)
    username = db.Column(db.String(30))
    # date = db.Column(db.String(20))
    # start_time = db.Column(db.String(30))
    # duration = db.Column(db.Integer)
    # capacity = db.Column(db.Integer)
    # location = db.Column(db.String(20))

    def __init__(self,name,reference,barcode_filename,username):
        self.name=name
        self.reference=reference
        self.barcode_filename=barcode_filename
        self.username=username
        # self.date=date
        # self.start_time=start_time
        # self.duration=duration
        # self.capacity=capacity
        # self.location=location

class Log(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    details=db.Column(db.String(50))
    time=db.Column(db.DateTime,default=datetime.now)
    def __init__(self,details):
        self.details=details

class CancelledEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    Date=db.Column(db.DateTime,default=datetime.now)
    def __init__(self, name):
        self.name = name









# class User(db.Model):
#     __tablename__='users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True)
#
#     def __init__(self, username):
#         self.username=username
#
# # a model of a list for the database
# # it refers to a user
