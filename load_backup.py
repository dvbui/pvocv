import database
import register
import pandas as pd
from io import StringIO
import json
import add_node
import search_node
import add_link
from bs4 import BeautifulSoup

def beautify(s):
    """
    This function de-escaped a string
    Parameters
    ----------
        s : str
            An string escaped by the textbox
    Returns
    -------
        str
            A de-escaped string
    """
    soup = BeautifulSoup(s, 'html.parser')
    return soup.get_text()

def update_node(username, password, node):
    """
    This function insert a Node to the user's database
    Parameters
    ----------
        username : str
            
        password : str

        node : dict
            The structure of the Node is described in OBJECT.md
    """
    add_node.main(username, password, node["content"], node["type"], node["keyword"],
                   node["usage_note"], node["vn"], node["source"], node["media"])

def update_edge(username, password, edge):
    """
    This function insert an Edge to the user's database
    Parameters
    ----------
        username : str
            
        password : str

        edge : dict
            The structure of the Edge is described in OBJECT.md
    """
    node = edge["node1"]
    node1_id = search_node.main(username, password, None, node["content"], node["type"], node["keyword"],
                   node["usage_note"], node["vn"], node["source"], node["media"])[0]["id"]
    node = edge["node2"]
    node2_id = search_node.main(username, password, None, node["content"], node["type"], node["keyword"],
                   node["usage_note"], node["vn"], node["source"], node["media"])[0]["id"]
    add_link.main(username, password, node1_id, node2_id, edge["type"])

def main(username, password, node_info, edge_info):
    """
        This function returns everything that is in a user PVO in a form of csv strings
        Parameters
        ----------
            username : str

            password : str

            node_info : str
                A CSV string represents the nodes in the user data
                Note that this string has been escaped by textarea. We need to de-escaped it.
            edge_info : str
                A CSV string represents the edges in the user data
                Note that this string has been escaped by textarea. We need to de-escaped it.
        Returns
        -------
            bool
                False if the load data progress fails
                True if succeeds
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    real_nodes = json.loads(pd.read_csv(StringIO(node_info)).to_json())
    real_edges = json.loads(pd.read_csv(StringIO(edge_info)).to_json())
    nodes = {}
    edges = []
    for key in real_nodes["id"]:
        node = {
            "id": real_nodes["id"][key],
            "user": real_nodes["user"][key],
            "content": real_nodes["content"][key],
            "type": real_nodes["type"][key],
            "keyword": real_nodes["keyword"][key],
            "usage_note": real_nodes["usage_note"][key],
            "vn": real_nodes["vn"][key],
            "source": real_nodes["source"][key],
            "media": real_nodes["media"][key]
        }

        for i in node:
            if node[i] is None:
                node[i] = ""
            if isinstance(node[i], str):
                node[i] = beautify(node[i])
        
        nodes[node["id"]] = node
    
    for key in real_edges["id"]:
        edge = {
            "node1": nodes[real_edges["node1"][key]],
            "node2": nodes[real_edges["node2"][key]],
            "type": real_edges["type"][key]
        }
        edges.append(edge)
    
    query = """
        DELETE FROM node
        WHERE user=%s
    """
    data = (user_id,)
    database.query(query, data)

    for i in nodes:
        update_node(username, password, nodes[i])
    
    for e in edges:
        update_edge(username, password, e)
    
    return True