import mysql.connector
import json

def get_connection():
    """
    This function generates a new connection to the MySQL database
    Requires info.json file
    """
    info = {}
    with open("info.json", "r") as f:
        info = json.load(f)
    connection = mysql.connector.connect(host=info["db_host"],
                                         database=info["db_name"],
                                         user=info["db_user"],
                                         password=info["db_pass"])
    return connection


def query(q, d):
    """
    This function executes a query with the provided query and data
    Parameters
    ----------
    q : str
        a query
    d : tuple
        the parameters used in the query
    Returns
    -------
    list
        a list of rows returned by the SQL query
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(q,d)
    result = list(cursor)
    connection.commit()
    cursor.close()
    connection.close()
    return result