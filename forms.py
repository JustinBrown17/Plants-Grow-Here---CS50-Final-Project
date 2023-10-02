# WTForms files
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField
from wtforms.validators import InputRequired, ValidationError, Email, Length, EqualTo, DataRequired, Optional
from flask_ckeditor import CKEditorField
import phonenumbers
import string

#TODO: add credentials to password fields


#!__________________________________ Variables __________________________________#
# create reuseable variables
name_min = 5
name_max = 30
username_min = 5
username_max = 14
password_min = 8
password_max = 16


NAME_LENGTH = Length(min = name_min, max = name_max,
                      message=f"Name must be between {name_min}-{name_max} characters long")
EMAIL_LENGTH = Length(min = 6, max = 40)
USERNAME_LENGTH = Length(min = username_min, max = username_max,
                          message=f"Username must be between {username_min}-{username_max} characters long")
PASSWORD_LENGTH = Length(min = password_min, max = password_max,
                          message=f"Password must be between {password_min}-{password_max} characters long")

# Error messages for phone validation
PH_MESSAGE1 = "Can only contain numbers: 0-9 and special characters such as: \"-\" or \"+\""
PH_MESSAGE2 = "Can only contain up to 16 characters"
PH_MESSAGE3 = "Invalid phone number, please enter a valid number."


#!__________________________________ Form Classes __________________________________#

# Create a Post Class
class PostForm(FlaskForm):
    title   = StringField("Title", validators = [InputRequired(message="Title is required")] )
    content = CKEditorField("Content", validators = [DataRequired(message="Body is required")])  # <--  , validators = [DataRequired(message="Body is required")] (NOTE: validator was not working)
    file    = FileField("File")
    submit  = SubmitField("Post")


# Create an Account Class (where user can edit their data) (NONE REQUIRED TO REUSE, REGISTER/ACCOUNT)
class AccountForm(FlaskForm):
    name         = StringField("Full Name",
                    validators = [NAME_LENGTH, Optional(strip_whitespace=True)])
    phone        = StringField("Phone",
                    validators = [Optional(strip_whitespace=True)])
    job          = StringField("Job Title",
                    validators = [Optional()])
    email        = StringField("Email",
                    validators = [EMAIL_LENGTH, Email(), Optional(strip_whitespace=True)])
    username     = StringField("Username",
                    validators = [USERNAME_LENGTH, Optional(strip_whitespace=True)])
    old_password = PasswordField("Current Password",
                    validators = [InputRequired(message = "Must input old password to make changes"),
                                    PASSWORD_LENGTH])
    new_password = PasswordField("New Password",
                    validators = [PASSWORD_LENGTH, EqualTo("confirm", message="Passwords must match"),
                                    Optional(strip_whitespace=True)])
    confirm      = PasswordField("Repeat New Password")
    submit       = SubmitField("Update Info")

    #! Check phone number is valid:
    def validate_phone(form, field):
        check_phone(field.data)


# Create a Register Class
class RegisterForm(FlaskForm):
    name     = StringField(label="Name",
                validators=[InputRequired(message="Name Required"), NAME_LENGTH])
    phone    = StringField('Phone', validators = [DataRequired()])
    email    = StringField("Email",
                validators=[InputRequired(message = "Email Required"), EMAIL_LENGTH, Email()])
    username = StringField("Username",
                validators=[InputRequired(message = "Username Required"), USERNAME_LENGTH])
    password = PasswordField("Password",
                validators=[InputRequired(message = "Password Required"),
                            PASSWORD_LENGTH, EqualTo('confirm', message = 'Passwords must match')])
    confirm  = PasswordField("Repeat Password")
    submit   = SubmitField("Register")

    #! Check phone number is valid:
    def validate_phone(form, field):
        check_phone(field.data)


# Create a Login Class
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    submit   = SubmitField("Login")


#!__________________________________ Form Functions __________________________________#

# Check phone number is valid and input does not contain invalid characters
def check_phone(ph_number):
    print(ph_number)

    list_invalids = list(string.ascii_lowercase + string.ascii_uppercase + string.punctuation)
    list_invalids.remove("-")
    list_invalids.remove("+")
    for char in list_invalids:
        if ph_number.__contains__(char):
            raise ValidationError(PH_MESSAGE1)

    if len(ph_number) > 16:
        raise ValidationError(PH_MESSAGE2)
    try:
        input_number = phonenumbers.parse(ph_number)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError(PH_MESSAGE3)
    except:
        input_number = phonenumbers.parse("+1" + ph_number)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError(PH_MESSAGE3)