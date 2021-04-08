from flask import *
import json
import register, add_node, search_node, add_link, get_link_type
import update_node, delete_node
import get_children, get_parent
import node_overview
import delete_link

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
    str
        The login page
    """
    files = ["login.html"]
    total = ""
    for f in files:
        total += render_template(f)
    return total

@app.route("/add_node_page")
def add_node_page():
    """
    This function represents the Add Node page
    The user should be logged in when using this page
    Returns
    -------
    str

    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("add_node.html",username=session.get("username"), password=session.get("password"))
    total += render_template("footer.html")
    return total

@app.route("/link_node_page", methods=["POST", "GET"])
def link_node_page():
    """
    This function represents the Link Node page
    The user should be logged in when using this page
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("link_node.html",username=session.get("username"),password=session.get("password"))
    total += render_template("footer.html")
    return total

@app.route("/edit_node_page", methods=["POST", "GET"])
def edit_node_page():
    """
    This function represents the Edit Node page
    The user should be logged in when using this page
    The id of the Node should also be given
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")) or request.values.get("id","")=="":
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("edit_node.html",username=session.get("username"), password=session.get("password"), node_id=request.values.get("id", ""))
    total += render_template("footer.html")
    return total

@app.route("/register", methods=common_methods)
def register_api():
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
def login_api():
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

@app.route("/logout", methods=common_methods)
def logout_api():
    """
    This function logs the current user out
    -------
    dict
        { "result" : True } if this function runs successfully
    """
    session.pop("username", None)
    session.pop("password", None)
    return { "result": True }

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

@app.route("/add_link", methods=common_methods)
def add_link_api():
    """
    See the documentation at add_link.main
    Returns
    -------
    dict
        { "result" : True } if two nodes are linked successfully,
        { "result" : False } otherwise
    """
    result = add_link.main(request.values["username"], request.values["password"],
                           request.values["node1"], request.values["node2"],
                           request.values["type"])
    return {"result": result}

@app.route("/get_link_type", methods=common_methods)
def get_link_type_api():
    """
    See the documentation at get_link_type.main
    Returns
    -------
    dict
        { "result": x } with x is a list of LinkType objects
    """
    result = get_link_type.main(request.values["username"], request.values["password"])
    return {"result": result}

@app.route("/update_node", methods=common_methods)
def update_node_api():
    """
    See the documentation at update_node.main
    Returns
    -------
    dict
        { "result": True } if the Node is updated successfully 
    """
    result = update_node.main(request.values["username"], request.values["password"],
                              request.values.get("id",None), 
                              request.values.get("content",""), request.values.get("node_type",""), 
                              request.values.get("keyword",""), request.values.get("usage_note",""),
                              request.values.get("vn",""), request.values.get("source",""),
                              request.values.get("media",""))
    return { "result": result }

@app.route("/delete_node", methods=common_methods)
def delete_node_api():
    """
    See the documentation at delete_node.main
    Returns
    -------
    dict
        { "result": True } if succeed
    """
    result = delete_node.main(request.values["username"], request.values["password"], request.values["id"])
    return {"result": result}

"""
@app.route("/get_children", methods=common_methods)
def get_children_api():
    See the documentation at get_children.main
    Returns
    -------
    dict
        { "result": x } with x is a list of LinkType objects
    result = get_children.main(request.values["username"], request.values["password"], request.values["id"])
    return {"result": result}

@app.route("/get_parent", methods=common_methods)
def get_parent_api():
    See the documentation at get_parent.main
    Returns
    -------
    dict
        { "result": x } with x is a list of LinkType objects
    result = get_parent.main(request.values["username"], request.values["password"], request.values["id"])
    return {"result": result}
"""

@app.route("/node_overview", methods=common_methods)
def node_overview_api():
    """
    See the documentation at node_overview.main
    Returns
    -------
    dict
        The structure is described at node_overview.main
    """
    result = node_overview.main(request.values["username"], request.values["password"], request.values["id"], 
    [request.values.get("link1","-1"), request.values.get("link2", "-1")])
    return result

@app.route("/delete_link", methods=["POST", "GET"])
def delete_link_api():
    """
    See the documentation at delete_link.main
    Returns
    -------
    dict
        { "result": True } if succeed
    """
    result = delete_link.main(request.values["username"], request.values["password"], request.values["id"])
    return {"result": result}

