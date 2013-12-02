from wtforms import Form, TextField, TextAreaField, PasswordField, RadioField, validators

class RegistrationForm(Form):
	email = TextField(u"Email", [validators.Length(min=6, max=35)])
	password = PasswordField(u"New Password", [validators.Required(), validators.EqualTo("confirm", message="Passwords must match")])
	confirm = PasswordField(u"Repeat Password")

class LoginForm(Form):
	email = TextField(u"Email", [validators.Required(), validators.Email()])
	password = PasswordField(u"Password", [validators.Required()])