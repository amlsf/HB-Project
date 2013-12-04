import model
from model import User, Location, Supply, Comment
import datetime
from pygeocoder import Geocoder
from twilio.rest import TwilioRestClient

# --------- TWILIO INTEGRATION ---------

account = "ACcd18bc05976f7bea45e9a39729140644"
token = "bf8bc3a6ab2334001787c9a02c948782"
client = TwilioRestClient(account, token)

def retrieve():
    # all text messages received in account
    messages = client.messages.list()
    # get user's phone number
    for number in messages[:1]:
        from_number = number.from_
    # get text messages in my account
    for info in messages[:1]:
        user_msg = info.body
    
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

    print "************************"
    print "From: %s" % from_number
    print "SMS: %s" % user_msg
    print "Split message: %s" % format_msg
    print "Name: %s" % name
    print "Address: %s" % full_address
    print "Latitude: %s" % lat
    print "Longitude: %s" % lng
    print "Supply: %s" % supply_type
    print "Date: %s" % date_logged
    print "Comment: %s" % comment

    user = User(name=name, phone_num=from_number)
    location = Location(full_address=full_address, lat=lat, lng=lng)
    supply = Supply(supply_type=supply_type, date_logged=date_logged)
    comment = Comment(extra_comment=comment)

    model.session.add(user)
    model.session.add(location)
    model.session.add(supply)
    model.session.add(comment)
    model.session.commit()