"""
    Author: Amy Lin
    Hackbright Academy, Fall 2013

    Project: SupplyCache
    Helping communities locate resources after a disaster

    Many thanks to:
    Hackbright!
    Leaflet JS + the amazing community for the various plugins
        Marker Cluster
        Heatmap JS
    Twilio
    Rickshaw JS
    CloudMade
    ngrok
    Google Fonts
"""

from flask import Flask, render_template, redirect, request, url_for
# from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
# import forms
# from forms import RegistrationForm

import twilio.twiml
import os

import model
from model import Master, User, Location, Supply, Comment
import json
import datetime
from pygeocoder import Geocoder

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

app = Flask(__name__)
app.config.from_object(config)

# Adding markdown capability to the app
Markdown(app)


# --------- MAIN PAGE ---------
@app.route("/")
def index():
    # query DB - info for popup on map
    master_info = Master.query.all()
    master_list = []
    for info in master_info:
        name = info.name
        email = info.email
        phone = info.phone_num
        address = info.full_address
        lat = info.lat
        lng = info.lng
        supply = info.supply_type
        comment = info.extra_comment
        single_marker = [name, email, phone, address, lat, lng, supply, comment]
        master_list.append(single_marker)
    # to JSON for Leaflet
    master_json = json.dumps(master_list)

    return render_template("index.html", master_json=master_json)


# --------- TWILIO ---------
@app.route("/incoming/sms", methods=["GET"])
def incoming_sms():
    # Twilio SMS response
    resp = twilio.twiml.Response()
    message = "Your text message has been received by SupplyCache!"
    # Retrieve info from Twilio
    user_num = request.values.get('From')
    user_msg = request.values.get('Body')
    # format and parse SMS
    format_msg = user_msg.split("/")
    # user info
    name = format_msg[0]
    # street address --> geocode --> lat, lng
    address_result = format_msg[1]
    format_address = Geocoder.geocode(address_result)
    lat_lng = format_address.coordinates
    lat = lat_lng[0]
    lng = lat_lng[1]
    full_address = str(format_address)
    # supply
    supply_type = format_msg[2]
    date_logged = datetime.datetime.now()
    # comment
    comment = format_msg[3]

    master = Master(name=name, phone_num=user_num, full_address=full_address, lat=lat, lng=lng, supply_type=supply_type, extra_comment=comment)
    user = User(name=name, phone_num=user_num)
    location = Location(full_address=full_address, lat=lat, lng=lng)
    supply = Supply(supply_type=supply_type, date_logged=date_logged)
    comment = Comment(extra_comment=comment)

    model.session.add(master)
    model.session.add(user)
    model.session.add(location)
    model.session.add(supply)
    model.session.add(comment)
    model.session.commit()

    resp.sms(message)
    return str(resp)


# --------- WEB FORM ---------
@app.route("/submit", methods=["POST"])
def submit():
    # user info
    name = request.form.get("name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num")
    # street address --> geocode --> lat, lng
    address = request.form.get("address")
    format_address = Geocoder.geocode(address)
    lat_lng = format_address.coordinates
    lat = lat_lng[0]
    lng = lat_lng[1]
    full_address = str(format_address)
    # supply
    supply_type = request.form.get("supply_type")
    date_logged = datetime.datetime.now()
    # comment
    comment = request.form.get("comment")

    master = Master(name=name, email=email, phone_num=phone_num, full_address=full_address, lat=lat, lng=lng, supply_type=supply_type, extra_comment=comment)
    user = User(name=name, email=email, phone_num=phone_num)
    location = Location(full_address=full_address, lat=lat, lng=lng)
    supply = Supply(supply_type=supply_type, date_logged=date_logged)
    comment = Comment(extra_comment=comment)

    model.session.add(master)
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


# --------- ARCHIVE ---------
@app.route("/register")
def register():
    return render_template("register.html")


# --------- IF LOGGED IN ---------
@app.route("/archive/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)