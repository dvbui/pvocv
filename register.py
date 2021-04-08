import database

def is_username_used(username):
    """
    This function checks if the given username is used
    Parameters
    ----------
    username : str
    Returns
    -------
    boolean
        True if the username is used, otherwise False
    """
    query = "SELECT id FROM user WHERE name=%s"
    data = (username,)
    result = database.query(query, data)
    return len(result) > 0

def get_user_id(username):
    """
    This function gets the user id, given his/her username
    Parameters
    ----------
    username : str
    Returns
    -------
    int
        The user id
    """
    query = "SELECT id FROM user WHERE name=%s"
    data = (username,)
    result = database.query(query, data)
    return result[0][0]

def check_user_pass(username, password):
    """
    This function checks if the pair of username, password is correct
    Parameters
    ----------
    username : str

    password : str

    Returns
    -------
    bool
        True if the username and password are correct
    """
    query = "SELECT id FROM user WHERE name=%s AND password=%s"
    data = (username, password)
    result = database.query(query, data)
    return len(result) > 0

def main(username, password):
    """
    This function checks if a register attempt is valid
    Parameters
    ----------
    username : str

    password : str

    Returns
    -------
    bool
        True if the register attempt is successful
        If the username has already been used, returns False
    """
    if is_username_used(username):
        return False
    else:
        query = "INSERT INTO user (name, password) VALUES (%s, %s)"
        data = (username,password)
        database.query(query, data)
        return True