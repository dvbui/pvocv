import database
import register
def main(username, password, id):
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