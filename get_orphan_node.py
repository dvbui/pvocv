import database
import register
import search_node
def main(username, password):
    """
        This function returns a list of Nodes that are not connected with other Nodes
        Parameters
        ----------
            username : str

            password : str

        Returns
        -------
            list
                A list of Node objects

    """
    if not register.check_user_pass(username, password):
        return False
    user_id = register.get_user_id(username)

    query = """
    SELECT N.id
    FROM node N
    WHERE N.user=%s AND N.id NOT IN (SELECT node1 AS id FROM edge UNION SELECT node2 AS id FROM edge)
    """
    data = (user_id,)
    result = database.query(query, data)
    output = []
    for row in result:
        obj = search_node.main(username, password, row[0])[0]
        output.append(obj)
    return output