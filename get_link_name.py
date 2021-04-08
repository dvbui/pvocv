import database
import register
def main(username, password, id):
    """
    This function returns a LinkType object with the given id
    Parameters
    ----------
        username : str

        password : str

        id : str
            (int is OK)
            The id of the LinkType
    Returns
    ----------
        dict
            the needed LinkType object
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    query = """
    SELECT * FROM rel_type
    WHERE (user IS NULL OR user=%s) AND id=%s
    """
    data = (user_id,id)
    result = database.query(query, data)
    return {
        "id": result[0][0],
        "rel": result[0][1],
        "user": result[0][2]
    }