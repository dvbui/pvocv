import database
import register
import search_node
import get_children
def main(username, password, link_types=[-1]):
    """
        This function returns everything that is in a user PVO
        Parameters
        ----------
            username : str

            password : str

            link_types : list
                (list of str or int)
                This list restricts the type of relations that can be used
                to travel from one node to another

        Returns
        -------
            dict
                A dictionary with the following (key,value)
                - "nodes": A list of Nodes in the user's PVO
                - "edges": A list of Edges in the user's PVO
    """
    link_types = list(map(int, link_types))
    result = {}
    result["nodes"] = search_node.main(username, password, node_type="0") + search_node.main(username, password, node_type="1")
    result["edges"] = []
    for node in result["nodes"]:
        result["edges"] += get_children.main(username, password, node["id"], link_types)
    return result
