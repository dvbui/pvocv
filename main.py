from flask import *
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import json
import register, add_node, search_node, add_link, get_link_type
import update_node, delete_node
import get_children, get_parent
import delete_link
import node_overview, pvo_overview
import get_orphan_node
import load_backup, get_backup
import converter


# setting constants up
app = Flask(__name__)
with open("info.json", "r") as f:
    data = json.load(f)
    app.secret_key = data["app_secret_key"]
    app.config["UPLOAD_FOLDER"] = data["upload_folder"]

common_methods = ["POST", "GET"]

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    
@app.route("/add_concept_page")
def add_concept_page():
    """
    This function represents the Add Concept page
    The user should be logged in when using this page
    Returns
    -------
    str

    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("add_node.html",username=session.get("username"), password=session.get("password"), node_type=0, node_type_name="Concept")
    total += render_template("footer.html")
    return total


@app.route("/add_example_page")
def add_example_page():
    """
    This function represents the Add Example page
    The user should be logged in when using this page
    Returns
    -------
    str

    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("add_node.html",username=session.get("username"), password=session.get("password"), node_type=1, node_type_name="Example")
    total += render_template("footer.html")
    return total

@app.route("/link_node_page", methods=common_methods)
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
    
@app.route("/link_concept_concept_page", methods=common_methods)
def link_concept_concept_page():
    """
    This function represents the Link Concept-Concept page
    The user should be logged in when using this page
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("link_node.html",username=session.get("username"),password=session.get("password"), 
                             rel_name="Concept-Concept", node_1_type_name="Parent Concept", node_2_type_name="Child Concept", 
                             node1_type=0, node2_type=0)
    total += render_template("footer.html")
    return total
    
@app.route("/link_example_concept_page", methods=common_methods)
def link_example_concept_page():
    """
    This function represents the Link Example-Concept page
    The user should be logged in when using this page
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("link_node.html",username=session.get("username"),password=session.get("password"), 
                             rel_name="Example-Concept", node_1_type_name="Concept", node_2_type_name="Example", 
                             node1_type=0, node2_type=1)
    total += render_template("footer.html")
    return total


@app.route("/edit_node_page", methods=common_methods)
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

@app.route("/orphan_node_page")
def orphan_node_page():
    """
    This function represents the Orphan Node page
    The user should be logged in when using this page
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("orphan_node.html",username=session.get("username"), password=session.get("password"))
    total += render_template("footer.html")
    return total

@app.route("/visualizer", methods=common_methods)
def visualizer_page():
    """
    This function outputs the graph containing all Nodes and Edges in the user's PVO
    The user should be logged in when using this page
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    total = render_template("pvo.html")
    total += render_template("visualizer.html",username=session.get("username"), password=session.get("password"))
    total += render_template("footer.html")
    return total

@app.route("/backup", methods=common_methods)
def backup_page():
    """
    This function outputs the backup page
    The user should be logged in when using this page
    Returns
    -------
    str
        
    """
    if not register.check_user_pass(session.get("username"), session.get("password")):
        return redirect(url_for('index'))
    def mdb_file_processor():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'mdb_file' not in request.files:
                return
            file = request.files['mdb_file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return
            if file and allowed_file(file.filename, ["mdb"]):
                filename = secure_filename(session.get("username") + file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                result = converter.load_mdb_file(session.get("username"), session.get("password"), file_path)
                if result:
                    flash("Your data have been loaded")
                os.remove(file_path)
    
    def csv_file_processor():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file1' not in request.files or 'file2' not in request.files:
                return
            file1 = request.files['file1']
            file2 = request.files['file2']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file1.filename == '' or file2.filename == "":
                flash('No selected file')
                return
            if file1 and allowed_file(file1.filename, ["csv"]) and file2 and allowed_file(file2.filename, ["csv"]):
                file1name = secure_filename(session.get("username") + "1" + file1.filename)
                file2name = secure_filename(session.get("username") + "2" + file2.filename)
                file_1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1name)
                file_2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2name)
                file1.save(file_1_path)
                file2.save(file_2_path)
                result = load_backup.from_file(session.get("username"), session.get("password"), file_1_path, file_2_path)
                if result:
                    flash("Your data have been loaded")
                os.remove(file_1_path)
                os.remove(file_2_path)
    
    mdb_file_processor()
    csv_file_processor()
    total = render_template("pvo.html")
    total += render_template("backup.html",username=session.get("username"), password=session.get("password"))
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

@app.route("/delete_link", methods=common_methods)
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

@app.route("/get_orphan_node", methods=common_methods)
def get_orphan_node_api():
    """
    See the documentation at delete_link.main
    Returns
    -------
    dict
        { "result": x } with x is a list of Nodes
    """
    result = get_orphan_node.main(request.values["username"], request.values["password"])
    return { "result": result}

@app.route("/pvo_overview", methods=common_methods)
def pvo_overview_api():
    """
    See the documentation at pvo_overview.main
    Returns
    -------
    dict
        
    """
    result = pvo_overview.main(request.values["username"], request.values["password"], 
    [request.values.get("link1","-1"), request.values.get("link2", "-1")])
    return result

@app.route("/get_backup", methods=common_methods)
def get_backup_api():
    """
    See the documentation at get_backup.main
    Returns
    -------
    dict
        
    """
    result = get_backup.main(request.values["username"], request.values["password"])
    return result

@app.route("/load_backup", methods=common_methods)
def load_backup_api():
    """
    See the documentation at load_backup.main
    Returns
    -------
    dict
        
    """
    result = load_backup.main(request.values["username"], request.values["password"], request.values["node_info"], request.values["edge_info"])
    return {"result": result}

@app.route("/file1.csv", methods=common_methods)
def file1_api():
    """
    This function outputs the first back-up csv file
    Returns
    -------
    str
        
    """
    result = get_backup.main(session.get("username"), session.get("password"))
    """
    The following code is adapted from https://stackoverflow.com/questions/35710361/python-flask-send-file-stringio-blank-files
    """
    result = get_backup.main(session.get("username"), session.get("password"))
    buffer = BytesIO()
    buffer.write(result["node_info"].encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     attachment_filename='file1.csv',
                     mimetype='text/csv')

@app.route("/file2.csv", methods=common_methods) 
def file2_api():
    """
    This function outputs the second back-up csv file
    Returns
    -------
    str
        
    """
    result = get_backup.main(session.get("username"), session.get("password"))
    """
    The following code is adapted from https://stackoverflow.com/questions/35710361/python-flask-send-file-stringio-blank-files
    """
    buffer = BytesIO()
    buffer.write(result["edge_info"].encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     attachment_filename='file2.csv',
                     mimetype='text/csv')
