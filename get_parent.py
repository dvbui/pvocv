import database
import register
import search_node
import get_link_name
import add_link

# TODO: get_parent and get_children should be combined
def main(username, password, child_id, link_types=[-1]):
    """
    This function gets the edges connecting the child with its children
    Parameters
    ----------
        username : str

        password : str

        parent_id : str
            (int is OK)
            The id of the child node
        link_types : list
            must be a list of int
            The ids of the type of relations that could be used to travel
            on the graph
    Returns
    -------
    list
        a list of Edge objects. The structure of each Edge object is described in OBJECT.md
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    if not add_link.check_owner(user_id, child_id):
        return False
    query = """
    SELECT *
    FROM edge E
    WHERE E.node2=%s
    """
    data = (child_id,)
    result = database.query(query, data)
    output = []
    for row in result:
        obj = {
            "id": row[0],
            "node1": search_node.main(username, password, row[1])[0],
            "node2": search_node.main(username, password, row[2])[0],
            "type": get_link_name.main(username, password, row[3])
        }
        if -1 in link_types or obj["type"]["id"] in link_types:
            output.append(obj)
    return output
