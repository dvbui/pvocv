import database
import register
import add_node
from bs4 import BeautifulSoup
def beautify(s):
    """
    This function detects the words that should be used as node label
    Parameters
    ----------
    s : str
        The given string (in html form)
    Returns
    -------
    str
        One of the following options:
        - The text represented by s
        - The bold part of the text.
        If the bold part is empty, the first option is used.
        Otherwise, the second option is used
    """
    soup = BeautifulSoup(s, 'html.parser')
    s1 = soup.get_text()
    s2 = []
    for bold in soup.find_all("strong"):
        # ensure that there's no None in s2
        if bold is not None and bold.text is not None:
            s2.append(bold.text)
    s2 = " ".join(s2)
    if s2!="":
        return s2
    return s1

def main(username, password, id=None, content="", node_type="", keyword="", usage_note="", vn="", source="", media="", exact=False):
    """
    This function finds the nodes that satisfy the given info
    The info (except username, password, id) could be given in partial form
    If all parameters except username, password are empty, this function returns all nodes 
    Parameters
    ----------
    username : str
        
    password : str

    id : str
        The id of the node. If this param is provided, other info is ignored.
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
    list
        a list of Node objects, which are described in OBJECT.md
    """

    if not register.check_user_pass(username, password):
        return False
    
    user_id = register.get_user_id(username)
    query = ""
    data = None
    if id is not None:
        query = "SELECT * FROM node WHERE user=%s AND id=%s"
        data = (user_id, id)
    else:
        content = add_node.standardize(content)
        usage_note = add_node.standardize(usage_note)
        query = """
        SELECT *
        FROM node
        WHERE user=%s AND (type=%s OR %s = %s) 
        AND content_text LIKE %s AND keyword LIKE %s AND usage_note_text LIKE %s
        AND vn LIKE %s AND source LIKE %s
        """
        if not exact:
            data = (user_id, node_type, node_type, "", "%"+content+"%", "%"+keyword+"%", "%"+usage_note+"%", "%"+vn+"%", "%"+source+"%")
        else:
            data = (user_id, node_type, node_type, "", content, keyword, usage_note, vn, source)
    
    query_result = database.query(query, data)
    result = []
    for row in query_result:
        obj = {
            "id": row[0],
            "user": row[1],
            "content": row[2],
            "content_text": beautify(row[2]),
            "type": row[4],
            "keyword": row[5],
            "usage_note": row[6],
            "vn": row[8],
            "source": row[9],
            "media": row[10]
        }
        result.append(obj)
    
    return result