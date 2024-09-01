from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_mail import Message, Mail
import os
from werkzeug.security import generate_password_hash, check_password_hash

from db_schema import Users, db, Events, Ticket,Log,CancelledEvents
import random
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)  # instanstiate flask for this app through object
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SUPPRESS_SEND'] = True
# make the mail handler
mail = Mail(app)

db.init_app(app)
# instantiate database for this flask object

with app.app_context():






    db.create_all()

@app.route('/')
def home():
    events=Events.query.all()
    return render_template("home.html",events=events)

@app.route('/login')
def logIn():
    return render_template("login.html")

@app.route('/editEvent')
def editEvent():
    events=Events.query.all()
    return render_template("editEvent.html",events=events)


@app.route('/update_capacity',methods=['POST'])
def update_capacity():
    newcap=request.form.get("new_capacity")
    name=request.form.get("event_name")
    currentEvent=Events.query.filter_by(name=name).first()
    if int(newcap)<(int(currentEvent.capacity)-currentEvent.tickets):
        flash("Tickets allocated is greater than the new capacity, please enter a different capacity", "error")
        return redirect(url_for('editEvent'))
    name2="Capacity of "+ name +"changed from " +str(currentEvent.capacity)+" to" + str(newcap)
    logSubmission=Log(name2)
    db.session.add(logSubmission)
    db.session.commit()
    tempTickets=currentEvent.tickets
    currentEvent.tickets = tempTickets+int(newcap)-int(currentEvent.capacity)
    currentEvent.capacity=newcap
    db.session.commit()
    return redirect(url_for('viewEvents'))
@app.route('/emailPassReset')
def emailPassReset():
    return render_template("emailPassReset.html")

@app.route('/password_reset',methods=['POST'])
def passwordReset():
    email=request.form.get("email")
    if Users.query.filter_by(email=email).first()==None:
        flash("Email not found", "error")
        return redirect(url_for('emailPassReset'))
    sender="u5510158@dcs.warwick.ac.uk"
    mail.send_message(sender=("NOREPLY", sender),subject="Password Reset", body='Use the following link to reset your password http://127.0.0.1:5000/resetpage', recipients=[email])
    flash("Password reset link sent to "+ email)
    return redirect(url_for('emailPassReset'))



@app.route('/resetpage',methods=['POST'])
def resetPage():
    return "works"



@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/createEvent')
def createEvent():
    return render_template("createEvent.html")

@app.route('/viewEvents2')
def viewEvents2():
    events = Events.query.all()
    return render_template("viewEvents2.html",events=events)


@app.route('/viewEvents')
def viewEvents():
    events=Events.query.all()
    return render_template("viewEvent.html",events=events)

@app.route('/DeleteEvent')
def deleteEvent():
    events = Events.query.all()
    return render_template("deleteEvent.html",events=events)

@app.route('/cancelledEvents')
def cancelledEvent():
    events=CancelledEvents.query.all()
    return render_template("/cancelledEvents.html",events=events)

@app.route('/delete_event',methods=['POST'])
def delete_event():
    event1= request.form.get("event_name")
    event=Events.query.filter_by(name=event1).first()
    cancelledEvent=CancelledEvents(event.name)
    db.session.add(cancelledEvent)
    db.session.commit()
    event1 = event1 + "cancelled was scheduled for" + event.date
    sender = "u5510158@dcs.warwick.ac.uk"
    effectedTickets=Ticket.query.filter_by(name=event1)
    for record in effectedTickets:
        tempusername=record.username
        user=Users.query.filter_by(username=tempusername)
        email=user.email
        mail.send_message(sender=("NOREPLY", sender), subject="Event" + event1+ " cancelled",
                      body='The following event has been cancelled ' + event1,
                      recipients=[email])


    logSubmission = Log(event1)
    db.session.add(logSubmission)
    db.session.commit()
    db.session.delete(event)
    db.session.commit()




    return redirect(url_for("viewEvents"))





@app.route('/superUserPortal')
def superUserPortal():
    return render_template("superUserPortal.html")

@app.route('/superUserredirect',methods=['POST'])
def superUserredirect():
    return redirect(url_for('superUserPortal'))

@app.route('/Userredirect',methods=['POST'])
def Userredirect():
    return redirect(url_for('userPortal'))
@app.route('/create', methods=['POST'])
def create():
    username2 = request.form.get("username")
    password = request.form.get("password")
    secondpass=request.form.get("confirmpass")
    user=Users.query.filter_by(username=username2).first()
    if user is not None:
        flash("There already exists a user with the same username","error")
        return redirect((url_for("register")))
    if(password!=secondpass):
        flash("Passwords do not match","error")
        return redirect(url_for("register"))
    hashed_password = generate_password_hash(password)

    email = request.form.get("email")
    type=request.form.get("category")

    if type=="superuser":
        if Users.query.filter_by(type=type).first()==None:
            users = Users(username2, hashed_password, email, type)
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash("There already exists a superuser","error")
            return redirect((url_for("register")))
    users = Users(username2, hashed_password, email, type)
    db.session.add(users)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/create_event',methods=['POST'])
def addEvent():
    name=request.form.get("event_name")
    date=request.form.get("event_date")
    start_time=request.form.get("start_time")
    duration=request.form.get("duration")
    location=request.form.get("location")
    capacity=request.form.get("capacity")
    event1=Events.query.filter_by(name=name).first()
    if event1 is not None:
        flash("There already exists an event with same name", "error")
        return redirect(url_for('createEvent'))
    event2=Events.query.filter_by(date=date, start_time=start_time, location=location).first()
    if event2 is not None:
        flash("There already exists an event at the same date, time and location","error")
        return redirect(url_for('createEvent'))
    event = Events(name, date, start_time, duration, location, capacity)
    db.session.add(event)
    db.session.commit()
    name="Event" +name+"created for " +event.date
    logSubmission=Log(name)
    db.session.add(logSubmission)
    db.session.commit()
    return redirect(url_for("viewEvents"))


def generate_barcode(value):
    ean = barcode.get_barcode_class('ean13')

    barcode_img = ean(value)


    barcode_filename = f'static/barcodes/{value}.png'


    barcode_img.save(barcode_filename)


    return barcode_filename




@app.route('/verify', methods=['GET'])
def verify():
    tempusername = request.args.get("uname")
    temppassword = request.args.get("psw")
    user = Users.query.filter_by(username=tempusername).first()
    if user is None:
        flash("Username not found", "error")
        return redirect(url_for('logIn'))
    if not check_password_hash(user.password, temppassword):
        flash("Wrong password", "error")
        return redirect(url_for('logIn'))
    session['username'] = tempusername
    if user.type=="superuser":
        details="Superuser "+ tempusername+"successfully logged in"
        logSubmission=Log(details)
        db.session.add(logSubmission)
        db.session.commit()
        return redirect(url_for('superUserPortal'))
    else:
        details ="User " +tempusername + " succesfully logged in"
        logSubmission = Log(details)
        db.session.add(logSubmission)
        db.session.commit()
        return redirect(url_for('userPortal'))

@app.route('/userPortal')
def userPortal():
    return render_template('userPortal.html')


@app.route('/bookEvent')
def bookEvent():
    if 'username' not in session:
        return redirect(url_for('logIn'))
    events=Events.query.all()
    username = session['username']
    tickets=Ticket.query.filter_by(username=username).all()

    return render_template('bookEvent.html',events=events,tickets=tickets)
@app.route('/book_event',methods=['POST'])
def book_event():
    if 'username' not in session:
        return redirect(url_for('logIn'))
    username = session['username']
    name=request.form.get("event_name")
    event=Events.query.filter_by(name=name).first()
    event.tickets-=1
    db.session.commit()
    reference = str(random.randint(100000000000, 999999999999))
    filename=generate_barcode(reference)+".svg"
    ticket=Ticket(name,reference, filename,username)
    db.session.add(ticket)
    db.session.commit()
    deatils=name +" ticket allocated to " + username
    logSubmission=Log(deatils)
    db.session.add(logSubmission)
    db.session.commit()
    flash(event.name+" booked for the " +event.date)
    return redirect((url_for('bookEvent')))

@app.route('/viewBooking')
def viewBooking():
    username = session['username']
    tickets=Ticket.query.filter_by(username=username)
    return render_template("viewBooking.html",tickets=tickets)


@app.route('/cancelBooking')
def cancelBooking():
    username=session['username']
    tickets = Ticket.query.filter_by(username=username)
    user=Users.query.filter_by(username=username)

    return render_template("cancelBooking.html", tickets=tickets,user=user)

@app.route('/cancel_booking',methods=['POST'])
def cancel_Booking():
    username = request.form.get("ticket_username")
    name=request.form.get("ticket_name")
    ticket = Ticket.query.filter_by(username=username).first()
    db.session.delete(ticket)
    db.session.commit()
    event2 = Events.query.filter_by(name=name).first()
    event2.tickets+=1
    db.session.commit()
    details="The booking of "+name +" cancelled by " +username
    logSubmission=Log(details)
    db.session.add(logSubmission)
    db.session.commit()
    flash("Booking for " + event2.name +" was cancelled, was scheduled for " + event2.date)
    return redirect(url_for("cancelBooking"))

@app.route('/transactionLog')
def transactionLog():
    logs = Log.query.order_by(Log.time.desc()).all()
    return render_template("logEvents.html",Log=logs)

@app.route('/logout',methods=['POST'])
def logOut():
    user=Users.query.filter_by(username=session['username']).first()
    if(user.type=="superuser"):

        details="Superuser " +session['username']+" succesfully logged out "
    else:
        details = "User " + session['username'] + " succesfully logged out "
    log=Log(details)
    db.session.add(log)
    db.session.commit()
    session.pop('username', None)
    return redirect((url_for('logIn')))



if __name__ == "__main__":
    app.run(debug=True)