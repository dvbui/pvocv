import database
import register
import search_node
import get_parent
import get_children

def generate(username, password, node_id, nodes, edges, visited_nodes, cur_node_info, link_types):
    """
    This is a depth-first-search function to find all nodes and edges connecting to a node
    Parameters
    ----------
        username : str

        password : str

        node_id : int

        nodes : list
            list of Node objects that are visited by the generate functions
            This list is changed by the function
        edges : list
            list of Edge objects that are visited by the generate functions
            This list is changed by the function
        visited_nodes : list
            list of int containing the ids of the visited Nodes
        cur_node_info : dict
            a Node object that represents the current node
        link_types : list
            (list of int)
            The list of relation types that are used to find other nodes
    """
    if node_id in visited_nodes:
        return

    visited_nodes[node_id] = True
    nodes.append(cur_node_info)

    # get all children through relations in link_types
    neighbors = get_children.main(username, password, node_id, link_types)
    for edge in neighbors:
        new_node = edge["node2"]["id"]
        edges.append(edge)
        # note: only add edges from parent to child to avoid duplicates
        generate(username, password, new_node, nodes, edges, visited_nodes, edge["node2"], link_types)

    # get all parents through relations in link_types
    neighbors = get_parent.main(username, password, node_id, link_types)
    for edge in neighbors:
        new_node = edge["node1"]["id"]
        generate(username, password, new_node, nodes, edges, visited_nodes, edge["node1"], link_types)


def main(username, password, node_id, link_types=["-1"]):
    """
        This functions returns a dictionary that contains all information of a node,
        including its internal data, the info of its ancestors and descendants, ...
        that are used in the Edit Node page
        Parameters
        ----------
            username : str

            password : str

            node_id : str
                (int is OK)
                The id of the parent node
            link_types : list
                could be a list of string or a list of int
                The ids of the type of relations that could be used to travel
                on the graph
        Returns
        -------
            dict
                A dictionary with the following (key,value)
                - "node_info": A Node object representing the node with the id node_id
                - "children": A list of Edge objects representing the children
                - "parent": A list of Edge objects representing the parents
                - "nodes": A list of Nodes that are connected to this Node (both directly and indirectly)
                - "edges": A list of Edges that are connected to this Node
    """
    if not register.check_user_pass(username, password):
        return False
    link_types = list(map(int, link_types))
    result = {}
    result["node_info"] = search_node.main(username, password, node_id)[0]
    result["children"] = get_children.main(username,password,node_id, link_types)

    result["parent"] = get_parent.main(username, password, node_id, link_types)

    visited_nodes = {}
    result["nodes"] = []
    result["edges"] = []
    generate(username, password, int(node_id), result["nodes"], result["edges"], visited_nodes, result["node_info"], link_types)

    return result
