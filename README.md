# Plants Grow Here

Video Demo - <https://youtu.be/QZ0E7_cbYG8>

## Description

This is a blog web app for Agronomists and Horticulturalists. A place where they can post images link and articles of their own to help farmers and growers worldwide with diseases and other ailments.

## Python

### app.py

- The main file for this web app. It contains all the routes for the app, with redirection and backend logic to interact with the database.

- Validate_on_sumbit is a function from [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) that I encountered while searching for form validation. WTForms checks the form defined in forms.py is valid before handing off to the backend functions. All that remains is checking information matches the database.

- In the contact route I added a simple function to remove admin accounts from the contact.html page then remove the 'id' column from all users.

- I intend to make a route to edit and delete posts, the maker of the post will be able to edit or delete their post. An admin can edit or delete any post.

- Also I will add complexity to password requirements before deployment.

### forms.py

- Using [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) to do all the form validation here in forms.py. This really helped clean up the app.py file as I could offload all the form parameters to this.

- This keeps the route validations in app.py much shorter because the basic frontend validation is taken care of in this file.

- This injects all the html validators into the pages where form = FlaskFormName is called before html is rendered.

- I found a phone number validator function on [Stack Overflow](https://stackoverflow.com/questions/36251149/validating-us-phone-number-in-wtforms) but had to modify it to throw a validation error for any char adding:

    ```python
    list_invalids = list(string.ascii_lowercase + string.ascii_uppercase + string.punctuation)
    list_invalids.remove("-")
    list_invalids.remove("+")
    for char in list_invalids:
        if ph_number.__contains_/_(char):
            raise ValidationError(PH_MESSAGE1)
    ```

    This got all ascii chars and made them into a list, removed '+' and '-' from the list, then checks the users input for any char in list.

- I used [CKeditor](https://ckeditor.com) for a RTF editor to retain the formatting from the users post into the database, when it is rendered in html it contains the exact appearance as the formatted text in the CKeditor

### config.py

- This is where all the app configuration is done.

- Cleans up the app.py.

- I used CSRF Protect from [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) for handling the form validations, this is such a simple integration as all that is needed in the html is:

    ```html
    <form>
    {{ form.csrf_token }}
    --form stuff--
    </form>
    ```

- Imported [CKeditor](https://ckeditor.com) for a RTF editor in the post form.

- Chose the acceptable extensions that a post can attach.

### functions.py

- This is where all the functions for app.py are defined.

- Checks username and emails are not in the database.

- Checks password is correct to the hashed password saved in database.

- Has a simple flash function for app.py routes that have many errors or successes (such as the /account route) where all inputs are optional except the user's current password.

## Templates

### _formhelpers.html

- A macro I found on the [WTForms docs](https://flask.palletsprojects.com/en/1.0.x/patterns/wtforms/#forms-in-templates) to return all errors as an unordered list under a 'form input' if the form was submitted and was invalid, per the validators in forms.py.

### account.html

- From the database paste all current user's information into their "Your Account" card.

- Uses _formhelpers.html macro to list errors as red list items

- Add a form to the page with inputs for changing:

    - name
    - job title
    - phone number
    - email
    - username
    - password

<br>
<br>

- The user must input their old password to change any field.

- A plan for this was to have a user's photo and a list with their posts sorted from most recent. Where users could edit or delete their posts right from the account page.

- In the future, I plan to make the users contact information by default not visible, therefore only their name would show up in the contact page. This is to give creators privacy.

### contact.html

- This page is for all the creators on this blog to have a contact card so any user can contact the creator for help with their agricultural issues.

- From the index page, where the authors name is there is a link to the user's name which will scroll them down to the poster.

- I intend to fix this so the id is used to scroll to the user vs the name, I'm still unsure of how I want to implement this.

### create.html

- This is where the [CKeditor](https://ckeditor.com) is imported into the html.

- Uses _formhelpers.html macro to list errors as red list items

- The editor has plenty of features to add to your article with:
    - headings
    - images
    - image alignment
    - highlighter
    - bold/italics
<br>
<br>

- I love the functionality of this editor where I could save formatted text into the database with just a simple import.

### index.html

- This is the main page of the website, if there are no posts: an info message appears letting the user know there are no posts.

- In each post there is a link to the contact page using the users name to scroll to their card in the contact page.

- Within the database, I initially implemented this without the [CKeditor](https://ckeditor.com), where I had two options: upload an image or a file. This still needs fixed so a user can upload images to the database separately and link them in their post body. As of now I only have a single file upload.

- I planned to have a search function where the user could search through article titles or text in the database to find a solution quickly.

### layout.html

- This is the main html which contains the foundation for all the other documents using jinja.

- Imports:
    - [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
    - warning sign svg
    - check mark svg
    - info icon svg
    - styles.css
    - favicon
<br>
<br>

- The navbar is also created here with navigation to the other pages.

- If the user is logged in, they will links to create post, account and logout.

- If the user is not logged in, they will see links to contacts, register and login.

- Contains the flashing layout for all the pages, with classes:
    - "Danger" - show errors, not dismissible.
    - "Success" - these are confirmations after changes.
    - "Info" - without an icon to welcome a user by name after they have logged in.
    - "Info-svg" - a message after a user makes a post and if there are no posts.
<br>
<br>

- The footer which has a link to credit the creator of the favicon 

### login.html

- A very simple form to log user in.

- Uses _formhelpers.html macro to list errors as red list items.

### register.html

- Alerts user, using a Bootstrap danger card, that some information they use to create their account will be visible to any visitors.

- As I plan to make the users contact information not visible by default, I may add a radio input on each if they want this info visible now.

## Styles

### root.css

- This is a copy of the root.css file from [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/).

- I added some colors to this file and pulled colors into styles.css.

### styles.css

- Needed to use the translateY command for the location of the link (index page to contact page) would position correctly in order avoid scrolling too far.

- .wrapword was found on [Stack Overflow](https://stackoverflow.com/questions/3247358/how-do-i-wrap-text-with-no-whitespace-inside-a-td), to wrap the long emails in the contacts page on smaller displays.

- .sidespacer was needed to keep the contacts from squishing together without any spacing in between.

- I used the @media selectors to get the device width and adjust the sizing of photos and cards to be larger for smaller displays.

- I changed the default formatting for the [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/) cards.

- I repeated the background image using a repeatable image.

- Sizing the images within the posts was difficult because the [CKeditor](https://ckeditor.com) does not add a class to it's <`img> tag before it gets into the database. I plan to find a way to replace <``img ...> with <```img class='post-img' ...>, making this easier to just target post images.

- I plan to fix the footer on the bottom of the pages, I want it to be only visible on the bottom of pages. Using the code commented out, it works for all the long pages but on the login page the text floats in the middle of the screen.

<br>

#### Dedicated to my wife, an agronomist

### This blog is ***still a work in progress***, and will be completed offically after the class
