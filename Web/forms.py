from wtforms import Form, TextField, TextAreaField, PasswordField, validators

class LoginForm(Form):
    email = TextField("Email", [validators.Required(), validators.Email()])
    password = PasswordField("Password", [validators.Required()])

class AddToMap(Form):
	first_name = TextField("First Name", [validators.Required()])
	last_name = TextField
	email = TextField
	phone_num = TextField
	address = TextField
	city = TextField
	state = TextField
	zipcode = TextField
	supply_type = TextField
	extra_comment = TextAreaField