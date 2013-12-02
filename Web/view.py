from flask import Flask, Response, render_template, redirect, request, g, session, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
from forms import RegistrationForm

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

import twilio
# from twilio.rest import TwilioRestClient
import model
from model import User, Location, Supply, Comment
import json
import datetime
from pygeocoder import Geocoder

app = Flask(__name__)
app.config.from_object(config)

# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
# End login stuff

# Adding markdown capability to the app
Markdown(app)

# --------- MAIN PAGE ---------
@app.route("/")
def index():
    # location
    locations = Location.query.all()
    marker_list = []
    for location in locations:
        lat_coordinate = location.lat
        lng_coordinate = location.lng
        address = location.full_address
        single_location = [lat_coordinate, lng_coordinate, address]
        marker_list.append(single_location)
    # to JSON for Leaflet
    map_json = json.dumps(marker_list)

    return render_template("index.html", map_json=map_json)


# --------- TWILIO ---------
@app.route("/incoming/sms", methods=["GET", "POST"])
def incoming_sms():
    # print "FORM", request.form
    # print "ARGS", request.args
    
    # Get user phone number
    user_num = request.args['From']
    # Get text message
    user_msg = request.args['Body']  

    format_msg = user_msg.split("/")
    name = format_msg[0]

    address_result = format_msg[1]
    format_address = Geocoder.geocode(address_result)
    lat_lng = format_address.coordinates
    lat = lat_lng[0]
    lng = lat_lng[1]
    full_address = str(format_address)

    supply_type = format_msg[2]
    date_logged = datetime.datetime.now()

    comment = format_msg[3]

    user = User(name=name, phone_num=user_num)
    location = Location(full_address=full_address, lat=lat, lng=lng)
    supply = Supply(supply_type=supply_type, date_logged=date_logged)
    comment = Comment(extra_comment=comment)

    model.session.add(user)
    model.session.add(location)
    model.session.add(supply)
    model.session.add(comment)
    model.session.commit()

    message = "Your text message has been received by Supplycache!"
    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)


# --------- WEB FORM ---------
@app.route("/submit", methods=["POST"])
def submit():

    # ----- user -----
    name = request.form.get("name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num")

    # ----- location -----
    address = request.form.get("address")
    # ensures address is formatted correctly
    format_address = Geocoder.geocode(address)
    lat_lng = format_address.coordinates
    lat = lat_lng[0]
    lng = lat_lng[1]
    full_address = str(format_address)

    # ----- supply -----
    supply_type = request.form.get("supply_type")
    date_logged = datetime.datetime.now()

    # ----- comment -----
    comment = request.form.get("comment")

    user = User(name=name, email=email, phone_num=phone_num)
    location = Location(full_address=full_address, lat=lat, lng=lng)
    supply = Supply(supply_type=supply_type, date_logged=date_logged)
    comment = Comment(extra_comment=comment)

    model.session.add(user)
    model.session.add(location)
    model.session.add(supply)
    model.session.add(comment)
    model.session.commit()

    return redirect(url_for("index"))


# --------- ABOUT ---------
@app.route("/about")
def about():
    return render_template("about.html")


# --------- ARCHIVE ---------
@app.route("/archive")
def archive():
    return render_template("archive.html")


# --------- IF LOGGED IN ---------
@app.route("/archive/admin")
def admin():
    return render_template("admin.html")


# --------- GRAPH ---------
@app.route("/graph")
def graph():
    d = {}
    data = Supply.query.all()
    
    for value in data:
        amount = value.id
        unicode_supply = value.supply_type
        supply = unicode_supply.encode("ascii", "ignore")
        if supply not in d.keys(): 
            d[supply] = amount
        else:
            d[supply] += amount

    keys_list = d.keys()
    values_list = []
    for key in keys_list:
        values_list.append(d[key])

    return render_template("db_graph.html", keys_list=keys_list, values_list=values_list)

# @app.route("/register", methods=["GET","POST"])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == "POST" and form.validate():
#         user = User(form.username.data, form.email.data, form.password.data)
#         model.session.add(user)
#         flash("Thanks for registering")
#         return redirect(url_for("/"))
#     return render_template("register.html", form=form)

# @app.route("/login", methods=["POST"])
# def authenticate():
#     form = forms.LoginForm(request.form)
#     if not form.validate():
#         flash("Incorrect username or password") 
#         return render_template("login.html")

#     email = form.email.data
#     password = form.password.data

#     user = User.query.filter_by(email=email).first()

#     if not user or not user.authenticate(password):
#         flash("Incorrect username or password") 
#         return render_template("login.html")

#     login_user(user)
#     return redirect(request.args.get("next", url_for("index")))

if __name__ == "__main__":
    app.run(debug=True)