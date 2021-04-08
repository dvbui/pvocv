from flask import *
import json
import register

# setting constants up
app = Flask(__name__)
with open("info.json", "r") as f:
    data = json.load(f)
    app.secret_key = data["app_secret_key"]


common_methods = ["POST", "GET"]

@app.route('/')
def index():
    """
    This function represents the home page.
    The homepage is used when the user is not logged in.
    Returns
    -------
    dict
        The login page
    """
    files = ["login.html"]
    total = ""
    for f in files:
        total += render_template(f)
    return total

@app.route("/register", methods=common_methods)
def register_page():
    """
    This function registers a user to the database
    username : str
        The username
    password : str
        The non-encoded password
    Returns
    -------
    dict
        { "result" : True } if the register attempt is valid, otherwise { "result" : False }
    """
    result = register.main(request.values["username"], request.values["password"])
    return { "result": result }

@app.route("/login", methods=common_methods)
def login_page():
    """
    This function logs an user in with the provided info
    (i.e. set the session values for username and password)
    username : str
        The username
    password : str
        The non-encoded password
        Returns
        -------
        dict
            { "result" : True } if the login attempt is valid, otherwise { "result" : False }
    """
    result = register.check_user_pass(request.values["username"], request.values["password"])
    if result:
        session["username"] = request.values["username"]
        session["password"] = request.values["password"]
    
    return { "result": result }