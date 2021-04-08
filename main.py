from flask import *
import json
import register, add_node, search_node

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

@app.route("/add_node", methods=common_methods)
def add_node_api():
    """
    This function adds a node into the database with the provided info
    username : str
        The username
    password : str
        The non-encoded password
    Returns
    -------
    dict
        { "result" : True } if the login attempt is valid, otherwise { "result" : False }
    """
    result = add_node.main(request.values["username"], request.values["password"],
                           request.values["content"], request.values["node_type"],
                           request.values["keyword"], request.values["usage_note"], 
                           request.values["vn"], request.values["source"], 
                           request.values["media"])

    return { "result": result }

@app.route("/search_node", methods=common_methods)
def search_node_api():
    """
    This function finds nodes into the database with the provided info
    Returns
    -------
    dict
        { "result" : x } with x is a list of Nodes that 
        match the provided info
        Node structure is described in OBJECT.md 
    """
    result = search_node.main(request.values["username"], request.values["password"],
                              request.values.get("id",None), 
                              request.values.get("content",""), request.values.get("node_type",None), 
                              request.values.get("keyword",""), request.values.get("usage_note",""),
                              request.values.get("vn",""), request.values.get("source",""),
                              request.values.get("media",""))
    return {"result": result}