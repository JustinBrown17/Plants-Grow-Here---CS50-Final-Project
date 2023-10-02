
#! TODO: user privileges, Admin: full privilege
# TODO: emails to registered person vs signup

import os
from flask import flash, redirect, render_template, request, session, url_for
from datetime import date
from werkzeug.utils import secure_filename
from config import app

# * Import all WTForms form layouts from forms.py
from forms import PostForm, AccountForm, RegisterForm, LoginForm

# * Import all functions + db from function.py
from functions import db, login_required, this_username_not_in_db, this_email_not_in_db, db_password_is_correct, generate_hash, allowed_file, flash_alerts


#!__________________________________ Application Routes __________________________________#


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # *____________ Create a post ____________#

    form = PostForm()

    if form.validate_on_submit():  # * needed with csrf:

        user_id = session["user_id"]
        title = form.title.data
        body = form.content.data
        curDate = date.today()
        curDate = curDate.strftime("%B %d, %Y")

        # if post has picture/file -> upload text+file to db, otherwise just upload text
        if form.file.data:
            file = form.file.data

            # prevent user from uploading unauthorized files
            if not allowed_file(file.filename):
                flash(u'Not a supported file', "danger")
                return render_template("create.html", form=form)

            # secure file name then save to static folder
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)

            # Validate the filename or extension is not null
            if name == '' or ext == '':
                flash(u'Invalid file name', "danger")
                return render_template("create.html", form=form)

            # valid picture extensions, used in jinja to determine if the file is rejected or a download
            pic_ext = [".jpeg", ".jpg", ".img", ".png"]  # '.pdf'

            saved_img = db.execute("SELECT image_path FROM posts;")
            for name in saved_img:
                if filename == name["image_path"]:
                    flash(u'File name already taken', "danger")
                    return render_template("create.html", form=form)

            saved_file = db.execute("SELECT file_path FROM posts;")
            for name in saved_file:
                if filename == name["file_path"]:
                    flash(u'File name already taken', "danger")
                    return render_template("create.html", form=form)

            # save file to static folder
            file.save(os.path.join(os.path.abspath(os.path.dirname(
                __file__)), app.config['UPLOAD_FOLDER'], filename))

            if ext in pic_ext:
                # insert post with pic into db + save to database with picture link
                db.execute("INSERT INTO posts (user_id, title, body, image_path, date) VALUES (?, ?, ?, ?, ?)",
                           user_id, title, body, filename, curDate)

            # file extension was not an image, will be rendered on webpage as a download link
            else:
                db.execute("INSERT INTO posts (user_id, title, body, file_path, date) VALUES (?, ?, ?, ?, ?)",
                           user_id, title, body, filename, curDate)

        # if user does not select file, save the post without file/filename
        else:
            db.execute("INSERT INTO posts (user_id, title, body, date) VALUES (?, ?, ?, ?)",
                       user_id, title, body, curDate)

        flash("Your post was successful!", "info-svg")
        return redirect("/")

    return render_template('create.html', form=form)


@app.route("/")
@app.route("/home")
def index():
    # *____________ Show Blog ____________#
    # if there is any blog posts
    if db.execute("SELECT * FROM posts"):

        posts = db.execute(
            "SELECT user_id, title, body, image_path, file_path, date, (SELECT name FROM users WHERE id = user_id) AS name, (SELECT title FROM users WHERE id = user_id) AS job FROM posts ORDER BY id DESC")

        return render_template("index.html", posts=posts)

    flash(u'No posts yet! Come back later!', "info-svg")
    return render_template("index.html")


#   TODO: change url
@app.route("/posters-login", methods=["GET", "POST"])
def login():
    # *___________ Log user in ___________#

    form = LoginForm()

    # User reached route via POST (as by submitting a form via POST)
    if form.validate_on_submit():

        rows = db.execute(
            "SELECT * from users WHERE username = ?", form.username.data)
        if len(rows) != 1:
            # NOTE: username is invalid, returning Username/Password to prevent brute force username
            flash("Invalid Username/Password", "danger")
            return render_template("login.html", form=form)

        id = rows[0]["id"]

        if db_password_is_correct(form.password.data, id):

            # Remember which user has logged in
            session["user_id"] = id

            # Greet and redirect user to home page
            flash(f"Welcome {rows[0]['name']}", "info")
            return redirect("/")

        else:
            flash("Invalid Username/Password", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    # *____________ Log user out ____________#

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# TODO: make this inaccessible or delete for security purposes:
    #!  we dont want users making posts
@app.route("/register", methods=["GET", "POST"])
def register():
    # *____________ Register new user ____________#

    form = RegisterForm()

    if form.validate_on_submit():

        # get form data
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # validate username, if errors flash and reload page
        if this_username_not_in_db(username):

            # hash users password then save user to database
            # TODO: remove this add email notification to admins
            hash_pass = generate_hash(password)
            db.execute("INSERT INTO users (username, hash, name, phone, email) VALUES(?, ?, ?, ?, ?)",
                       username, hash_pass, name, phone, email)

            # find new_user id, then log them in (with session)
            rows = db.execute(
                "SELECT id FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            flash(u"Registered!", "success")

            # Redirect new user to homepage
            return redirect("/")
        else:
            flash(u"Username is taken! Try another!", "danger")

    return render_template("register.html", form=form)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # *____________ Edit users profile ____________#

    form = AccountForm()

    # hand off function to validate_un/pw
    id = session["user_id"]
    account = db.execute(
        "SELECT username, name, title, phone, email FROM users WHERE id = ?", id)

    if form.validate_on_submit():
        # keep track of success and errors
        errors = []
        success = []

        # get form data
        name = form.name.data
        phone = form.phone.data
        job = form.job.data
        email = form.email.data
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.new_password.data

        # if old password is right continue checking
        if db_password_is_correct(old_password, id):

            if username:
                # Checks if username is taken
                if this_username_not_in_db(username):
                    db.execute(
                        "UPDATE users SET username = ? WHERE id = ?", username, id)
                    success += ["Username was updated!"]
                else:
                    errors += ["Username is taken. Try another username!"]

            if name:
                db.execute("UPDATE users SET name = ? WHERE id = ?", name, id)
                success += ["Name was updated!"]

            if job:
                db.execute("UPDATE users SET title = ? WHERE id = ?", job, id)
                success += ["Job Title was updated!"]

            if phone:
                db.execute(
                    "UPDATE users SET phone = ? WHERE id = ?", phone, id)
                success += ["Phone number was updated!"]

            if email:
                if this_email_not_in_db(email):
                    db.execute(
                        "UPDATE users SET email = ? WHERE id = ?", email, id)
                    success += ["Email was updated!"]
                else:
                    errors += ["Email is taken. Try another email!"]

            if new_password:
                # vaidate new password is different than old password
                if old_password != new_password:
                    hash_pass = generate_hash(new_password)
                    db.execute(
                        "UPDATE users SET hash = ? WHERE id = ?", hash_pass, id)
                    success += ["Password was updated!"]
                else:
                    errors += ["Invalid new password. New password and old password are the same!"]

        #! Current password was wrong
        else:
            errors = ["Invalid current password. Cannot update inputs"]

        # * Flash all errors/successes, then reload page
        flash_alerts(errors, success)

        if errors:
            return render_template("account.html", form=form, account=account)

        return redirect(url_for('account'))

    return render_template("account.html", form=form, account=account)


@app.route("/contact")
def contact():
    # *____________ Contact page of all users except admins ____________#

    if db.execute("SELECT * FROM users"):
        # TODO: add privacy setting so users can hide their contact info

        # Collect all users for contact page
        contacts = db.execute(
            "SELECT id, name, title, phone, email FROM users  ")

        #! Delete admins from contacts list
        res = list(filter(lambda i: i['id'] != 2, contacts))
        res = list(filter(lambda i: i['id'] != 6, res))
        print(res)
        for items in res:
            if "id" in items:
                del items["id"]
        contacts = res

        return render_template("contact.html", contacts=contacts)

    # TODO: no contacts (beside admins), check this
    return render_template("contact.html")


#!__________________________________ Run Application __________________________________#
if __name__ == "__main__":
    app.run(debug=True)  # TODO: remove debug
