from flask import Flask, render_template, redirect, request, g, session, url_for, flash
# from flask.ext.login import LoginManager, login_required, login_user, current_user
# from flaskext.markdown import Markdown
# import config
# import forms
import model
from model import User, Location, Supply, Comment
import json
import datetime
from pygeocoder import Geocoder

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

app = Flask(__name__)
# app.config.from_object(config)

# Stuff to make login easier
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)
# End login stuff

# Adding markdown capability to the app
# Markdown(app)

@app.route("/")
def index():
    # ----- database to map ----- 
    locations = Location.query.all()
    location_list = []
    
    for location in locations:
        lat_coordinate = location.lat
        lng_coordinate = location.lng
        address = location.full_address
        single_location = [lat_coordinate, lng_coordinate, address]
        location_list.append(single_location)
    # to JSON for Leaflet
    map_json = json.dumps(location_list)

    return render_template("index.html", map_json=map_json)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():

    # ----- user -----
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone_num = request.form.get("phone_num")

    # ----- location -----
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")
    result = address + " " + city + " " + state + " " + zipcode
    # ensures address is formatted correctly
    new_result = Geocoder.geocode(result)
    lat_lng = new_result.coordinates
    lat = lat_lng[0]
    lng = lat_lng[1]
    full_address = str(new_result)

    # ----- supply -----
    supply_type = request.form.get("supply_type")
    supply_amount = request.form.get("supply_amount")
    date_logged = datetime.datetime.now()

    # ----- comment -----
    comment = request.form.get("comment")

    user = User(first_name=first_name, last_name=last_name, email=email, phone_num=phone_num)
    location = Location(full_address=full_address, lat=lat, lng=lng)
    supply = Supply(supply_type=supply_type, supply_amount=supply_amount, date_logged=date_logged)
    comment = Comment(extra_comment=comment)

    model.session.add(user)
    model.session.add(location)
    model.session.add(supply)
    model.session.add(comment)
    model.session.commit()

    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/archive")
def archive():
    return render_template("archive.html")

@app.route("/graph")
def graph():
    d = {}
    data = Supply.query.all()
    
    for value in data:
        amount = value.supply_amount
        unicode_supply = value.supply_type
        supply = unicode_supply.encode('ascii', 'ignore')
        if supply not in d.keys(): 
            d[supply] = amount
        else:
            d[supply] += amount

    keys_list = d.keys()
    values_list = []
    for key in keys_list:
        values_list.append(d[key])

    return render_template("db_graph.html", keys_list=keys_list, values_list=values_list)

if __name__ == "__main__":
    app.run(debug=True)