import database
import register
def check_owner(user_id, node_id):
    """
    This function checks if the given node actually belongs to the user
    Parameters
    ----------
        user_id : int
            
        node_id : int
    Returns
    ----------
        True if the node belongs to the user
    """
    query = """
    SELECT *
    FROM node
    WHERE user=%s AND id=%s
    """
    data = (user_id, node_id)
    result = database.query(query,data)
    return len(result) == 1

def main(username, password, node1, node2, link_type):
    """
    This function attempts to link two nodes together
    Parameters
    ----------
        username : str
            
        password : str

        node1 : int
            The id of the parent node
        node2 : int
            The id of the child node
        link_type : int
            The id of the relation type
    Returns
    ----------
        True if two nodes are linked successfully
        False if the user is not logged in or a node does not belong to the user
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    if not (check_owner(user_id, node1) and check_owner(user_id, node2)):
        return False
    # TODO: check if the type belongs to the user
    query = """
    INSERT INTO edge (node1, node2, type)
    VALUES (%s,%s,%s)
    """
    data = (node1, node2, link_type)
    database.query(query, data)
    return True