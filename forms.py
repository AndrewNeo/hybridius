from wtforms import Form, BooleanField, TextField, PasswordField, validators
import re

illegal_shortcode_names = ["admin"]
legal_shortcode_regex = "^[a-zA-Z0-9\.\_\-\~\!\$\&\'\(\)\*\,\;\=]*$"

def shortcode_validator(form, field):
	if field.data is not None:
		if (field.data in illegal_shortcode_names):
			raise validators.ValidationError("Can't use a protected name.")
		matchObject = re.match(legal_shortcode_regex, field.data)
		if not matchObject:
			raise validators.ValidationError("Can't use illegal characters.")


class AddForm(Form):
    is_random = BooleanField("Shortcode is random", default=True)
    shortcode = TextField("Custom shortcode", [
		validators.Length(max=20),
		shortcode_validator
	])
    target_url = TextField("Destination", [
    	validators.Required(),
    	validators.Length(max=1024, message="Max limit 1024 characters.")
	])


class LoginForm(Form):
    username = TextField("Username", [validators.Required()])
    password = PasswordField("Password", [validators.Required()])

    login_validator = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not self.login_validator(self.username.data, self.password.data):
            self.username.errors.append("Invalid login.")
            return False

        return True
