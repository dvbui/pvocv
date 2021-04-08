import database
import register
import add_link

def check_owner(user_id, link_id):
    """
    This function checks if user with user_id owns the link whose id is link_id
    Parameters
    ----------
        user_id : int

        link_id : int

    Returns
    -------
        True if user owns the link
    """
    query = """
    SELECT node1, node2
    FROM edge
    WHERE id=%s
    """
    data = (link_id,)
    result = database.query(query, data)
    node1_id = result[0][0]
    node2_id = result[0][1]
    return add_link.check_owner(user_id, node1_id) and add_link.check_owner(user_id,node2_id)


def main(username, password, link_id):
    """
    This function deletes a relation from the database
    Parameters
    ----------
        username : str

        password : str

        link_id : int
            The id of a link / edge / relation
    Returns
    -------
        True if the link is deleted successfully
        False if the username, password are wrong
        False if the user does not own the link
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    if not check_owner(user_id, link_id):
        return False
    
    query = """
    DELETE FROM edge
    WHERE id=%s
    """
    data = (link_id,)
    result = database.query(query, data)
    return result