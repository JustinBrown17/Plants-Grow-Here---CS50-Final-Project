from flask import redirect, session
from flask import flash
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

#* Import needed modules from config.py
from config import db, ALLOWED_EXTENSIONS




#!__________________________________ Define Functions __________________________________#


def login_required(f):

    #*______ Decorate routes to require login ______#
    #* https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash(u"You must be logged in to access this page", "danger")
            return redirect("/posters-login") #TODO redirect to home page
        return f(*args, **kwargs)
    return decorated_function




def this_username_not_in_db(username):

    #*______ Make sure we do not have repeat usernames ______#

    othernames = db.execute("SELECT username FROM users")
    for name in othernames:
        if name["username"] == username:
            return False
    # no errors
    return True




def this_email_not_in_db(email):

    #*______ Make sure we do not have repeat emails ______#

    other_emails = db.execute("Select email FROM users")
    for emails in other_emails:
        if emails["email"] == email:
            return False
    # no errors
    return True




def db_password_is_correct(input_password, id):

    #*______ Check users password ______#

    rows = db.execute("SELECT * FROM users WHERE id = ?", id)

    # Ensure password is correct
    if not check_password_hash(rows[0]["hash"], input_password): #'''len(rows) != 1 or'''
        return False
    else:
        return True




def generate_hash(password):

    #*______ Create hash for new passwords ______#

    hash_pass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    return hash_pass





def allowed_file(filename):

    #*______ Define allowed files ______#

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





def flash_alerts(errors, success):

    #!______ Flash errors and success messages ______#

    if errors:
        for message in errors:
            flash(message, "danger")

    if success:
        for message in success:
            flash(message, "success")
    return