import database
import register
from bs4 import BeautifulSoup
def standardize(s):
    """
    This function removes html tags and special characters from a string so that the info can be searched
    easily in the MySQL database
    Parameters
    ----------
    s : str
        The given string
    Returns
    -------
    str
        The given string without special characters and html tags
    """
    soup = BeautifulSoup(s, 'html.parser')
    s = soup.get_text()
    s = s.replace(" ","")
    s = s.replace("\n","")
    s = s.lower()
    return s
def main(username, password, content, node_type, keyword, usage_note, vn, source, media):
    """
    This functions attempts to add a new node to the database 
    Parameters
    ----------
    username : str
        
    password : str

    content : str
        The name of the concept, or an example sentence (in html form)
    node_type : str
        The type of the node, "0" = concept, "1" = example
    keyword : str
        The keywords used as special search terms
    usage_note : str
        (in html form)
    vn : str
        The Vietnamese translation
    source : str
    media : str
        (in html form)
    Returns
    -------
    boolean
        True if the node is added successfully
        False if the provided username, password are invalid
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    content_text = standardize(content)
    usage_note_text = standardize(usage_note)
    query = "INSERT INTO node (user, content, content_text, type, keyword, usage_note, usage_note_text, vn, source, media) VALUES "
    query += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (user_id, content, content_text, node_type, keyword, usage_note, usage_note_text, vn, source, media)
    database.query(query, data)
    return True