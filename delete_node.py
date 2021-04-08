import database
import register
import add_link
def main(username, password, node_id):
    """
    This function deletes a node from the database
    Parameters
    ----------
        username : str

        password : str

        node_id : str
            (int is OK)
    Returns
    -------
    bool
        True if succeed
        False if the provided username, password are incorrect
        False if the user does not own the node
    """
    # check if the provided username and password are valid
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    # check if the user owns this node
    if not add_link.check_owner(user_id, node_id):
        return False
    query = """
    DELETE FROM node
    WHERE user=%s AND id=%s
    """
    data = (user_id,node_id)
    result = database.query(query, data)
    return result