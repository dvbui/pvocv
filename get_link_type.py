import database
import register

def main(username, password):
    """
    This function returns a list of relation types that the given user own
    Parameters
    ----------
        username : str

        password : str
    Returns
    -------
        list
            a list of LinkType dictionaries
            The structure of the dictionaries can be found at OBJECT.md
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    query = """
    SELECT * FROM rel_type
    WHERE user IS NULL or user=%s
    """
    data = (user_id,)
    query_result = database.query(query, data)
    result = []
    for row in query_result:
        obj = {
            "id": row[0],
            "rel": row[1],
            "user": row[2]
        }
        result.append(obj)
    return result