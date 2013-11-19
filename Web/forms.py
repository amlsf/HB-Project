from wtforms import Form, TextField, TextAreaField, PasswordField, RadioField, validators

class RegistrationForm(Form):
	username = TextField(u"Username", [validators.Length(min=2, max=25)])
	email = TextField(u"Email", [validators.Length(min=6, max=35)])
	password = PasswordField(u"New Password", [validators.Required(), validators.EqualTo("confirm", message="Passwords must match")])
	confirm = PasswordField("Repeat Password")

class AddLoggedIn(Form):
	address = TextField(u"Address", [validators.Required()])
	city = TextField(u"City", [validators.Required()])
	state = TextField(u"State", [validators.Required()])
	zipcode = TextField(u"Zipcode", [validators.Required()])
	supply_type = RadioField(u"Supply", [validators.Required()], choices=[("Water"),("Food"),("First Aid Kit"),("Cell Phone Charger"),("Flashlight & Batteries")])
	extra_comment = TextField(u"Comment", [validators.Optional(), validators.length(max=140)])

class AddNotLoggedIn(Form):
	name = TextField(u"Name", [validators.Required()])
	email = TextField(u"Email", [validators.Required()])
	phone_num = TextField(u"Phone Number", [validators.Required()])
	address = TextField(u"Address", [validators.Required()])
	city = TextField(u"City", [validators.Required()])
	state = TextField(u"State", [validators.Required()])
	zipcode = TextField(u"Zipcode", [validators.Required()])
	supply_type = RadioField(u"Supply", [validators.Required()], choices=[("Water"),("Food"),("First Aid Kit"),("Cell Phone Charger"),("Flashlight & Batteries")])
	extra_comment = TextField(u"Comment", [validators.Optional(), validators.length(max=140)])