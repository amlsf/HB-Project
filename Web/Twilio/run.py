from flask import Flask, request, session
import twilio.twiml

SECRET_KEY = "misterfeeny"
app = Flask(__name__)
app.config.from_object(__name__)

callers = {
	"+14158675309": "Cory",
	"+14158675310": "Shawn",
	"+14158675311": "Topanga",
}

@app.route("/", methods=["GET", "POST"])
def hello_world():
	counter = session.get("counter", 0)
	counter += 1
	session["counter"] = counter

	# url?From=phone_number
	from_number = request.values.get('From', None)
	# if from this number, reply with this message
	if from_number in callers:
		name = callers[from_number]
		# message = callers[from_number] + ", thanks for the message!"
	# else, reply with this message instead
	else:
		name = "Minkus"
		# message = "Monkey, thanks for the message!"

	message = "".join([name, " has messaged ", request.values.get('To'), " ", str(counter), " times."])
	resp = twilio.twiml.Response()
	resp.sms(message)

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)