# sends an SMS to a phone number via a form

from flask import Flask, render_template, request
from twilio.rest import TwilioRestClient
import twilio.twiml
import model
from model import User, Location, Supply, Comment
from pygeocoder import Geocoder
import datetime

app = Flask(__name__)
# REMOVE SID AND TOKEN BEFORE PUSHING TO GITHUB
account = "ACcd18bc05976f7bea45e9a39729140644"
token = "bf8bc3a6ab2334001787c9a02c948782"
client = TwilioRestClient(account, token)

@app.route("/", methods=["GET", "POST"])
def receive_message():
	from_number = request.values.get("From")
	if from_number:
		# 48 characters
		message = "Text message successfully received by Respondly!"

	user_msg = request.values.get("Body")

	if user_msg:
		# split string on / --> initial text message parsing
		format_msg = user_msg.split("/")
		# assign split string to appropriate fields
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

		user = User(name=name, phone_num=from_number)
		location = Location(full_address=full_address, lat=lat, lng=lng)
		supply = Supply(supply_type=supply_type, date_logged=date_logged)
		comment = Comment(extra_comment=comment)

		model.session.add(user)
		model.session.add(location)
		model.session.add(supply)
		model.session.add(comment)
		model.session.commit()

	# after user sends SMS, respond with confirmation
	resp = twilio.twiml.Response()
	resp.sms(message)

	return str(resp)

	# return render_template("parse.html", message=message)

if __name__ == "__main__":
	app.run(debug=True)