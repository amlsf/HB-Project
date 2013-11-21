# sends an SMS to a phone number via a form

from flask import Flask, render_template, request
from twilio.rest import TwilioRestClient

app = Flask(__name__)
# REMOVE SID AND TOKEN BEFORE PUSHING TO GITHUB
account = ""
token = ""
client = TwilioRestClient(account, token)

@app.route("/")
def form():
	return render_template("form.html")

@app.route("/", methods=["POST"])
def form_post():
	message = client.sms.messages.create(to="PHONE_NUMBER", from_="TWILIO_NUMBER", body=request.form["Message"])
	return render_template("success.html", message=message)

if __name__ == "__main__":
	app.run(debug=True)