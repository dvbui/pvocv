import database
import register
import add_node

def main(username, password, id, content, node_type, keyword, usage_note, vn, source, media):
    """
    This functions use the provided infomation to update the Node having the given id
    Parameters
    ----------
        username : str

        password : str

        id : str
            (int is OK)
            The id of the Node
        content : str
            (in html form)
        node_type : str
            "0" - concept
            "1" - example
        keyword : str
            
        usage_note : str
            (in html form)
        
        vn : str

        source : str

        media : str
            (in html form)
    Returns
    -------
        True if the node is added to the database successfully
    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)
    content_text = add_node.standardize(content)
    usage_note_text = add_node.standardize(usage_note)
    query = """
        UPDATE node
        SET content=%s, content_text=%s, type=%s, keyword=%s, usage_note=%s, usage_note_text=%s, vn=%s, source=%s, media=%s
        WHERE user=%s AND id=%s
    """
    data = (content, content_text, node_type, keyword, usage_note, usage_note_text, vn, source, media, user_id, id)
    database.query(query, data)
    return True
