import database
import register
import search_node
import pandas as pd

def main(username, password):
    """
        This function returns everything that is in a user PVO in a form of csv strings
        Parameters
        ----------
            username : str

            password : str

        Returns
        -------
            dict
                A dictionary with the following (key,value)
                - "node_info": A CSV string represents the nodes in the user database
                - "edge_info": A CSV string represents the edges in the user database
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    all_nodes = search_node.main(username, password, node_type=0) + search_node.main(username, password, node_type=1)
    # ensure that a correct csv file would be produced
    real_nodes = {
        "id": [],
        "user": [],
        "content": [],
        "content_text": [],
        "type": [],
        "keyword": [],
        "usage_note": [],
        "vn": [],
        "source": [],
        "media": []
    }
    for node in all_nodes:
        for key in node:
            if key not in real_nodes:
                real_nodes[key] = []
            real_nodes[key].append(node[key])
    
    node_df = pd.DataFrame(real_nodes)

    query = """
        SELECT *
        FROM edge
        WHERE node1 IN (SELECT id FROM node WHERE user=%s)
    """
    data = (user_id,)
    result = database.query(query, data)
    real_edges = {
        "id": [],
        "node1": [],
        "node2": [],
        "type": []
    }

    for row in result:
        real_edges["id"].append(row[0])
        real_edges["node1"].append(row[1])
        real_edges["node2"].append(row[2])
        real_edges["type"].append(row[3])
    
    edge_df = pd.DataFrame(real_edges)
    return { "node_info": node_df.to_csv(index=False), "edge_info": edge_df.to_csv(index=False) }