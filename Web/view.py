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

# Stuff to make login easier
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)
# End login stuff

# Adding markdown capability to the app
Markdown(app)


# --------- MAIN PAGE ---------
@app.route("/")
def index():
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
    
    resp = twilio.twiml.Response()
    message = "Your text message has been received by SupplyCache!"

    user_num = request.values.get('From')
    user_msg = request.values.get('Body')

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


# --------- IF LOGGED IN ---------
@app.route("/archive/admin")
def admin():
    return render_template("admin.html")


# --------- GRAPH ---------
# @app.route("/graph")
# def graph():
#     d = {}
#     data = Supply.query.all()
    
#     for value in data:
#         amount = value.id
#         unicode_supply = value.supply_type
#         supply = unicode_supply.encode("ascii", "ignore")
#         if supply not in d.keys(): 
#             d[supply] = amount
#         else:
#             d[supply] += amount

#     keys_list = d.keys()
#     values_list = []
#     for key in keys_list:
#         values_list.append(d[key])

#     return render_template("db_graph.html", keys_list=keys_list, values_list=values_list)

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