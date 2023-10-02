from flask import Flask
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor
from cs50 import SQL  # TODO: mysql implementation


#!__________________________________ Configure Application __________________________________#


app = Flask(__name__)

# Files locations for database
UPLOAD_FOLDER = "static/posts"
# TODO pick all file extensions needed
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'])

# Create key for csrf
csrf = CSRFProtect()
# TODO: change this before implementation
app.config["SECRET_KEY"] = "secret_key_1"
ckeditor = CKEditor(app)
app.config['CKEDITOR_PKG_TYPE'] = 'standard'  # 'full'
csrf.init_app(app)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies) #TODO: learn more about sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blog.db")

# Clear cache


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
