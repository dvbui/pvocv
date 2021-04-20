from access_parser import AccessParser
from striprtf.striprtf import rtf_to_text
import pandas as pd
import load_backup


def load_mdb_file(username, password, database_path):
    """
        This function returns everything that is in a user PVO in a form of csv strings
        Parameters
        ----------
            username : str

            password : str

            node_info : str
                A CSV string represents the nodes in the user data
                Note that this string has been escaped by textarea. We need to de-escaped it.
            edge_info : str
                A CSV string represents the edges in the user data
                Note that this string has been escaped by textarea. We need to de-escaped it.
        Returns
        -------
            bool
                False if the load data progress fails
                True if succeeds
    """
    # load tables in database
    db = AccessParser(database_path)
    concept_table = db.parse_table("tblWord")
    example_table = db.parse_table("tblExample")
    concept_relation_table = db.parse_table("tblWordRelation")
    example_relation_table = db.parse_table("tblWordExampleRelation")

    def beautify(s):
        try:
	        return rtf_to_text(s)
        except:
	        return ""

    real_nodes = {
        "id": [],
        "user": [],
        "content": [],
        "content_text": [],
        "type": [],
        "keyword": [],
        "usage_note": [],
        "vn": [],
        "source": [],
        "media": []
    }

    ## convert concepts into nodes
    for i in range(len(concept_table["ID"])):
        real_nodes["id"].append(concept_table["ID"][i])
        real_nodes["user"].append(0)
        real_nodes["content"].append(concept_table["Word"][i])
        real_nodes["content_text"].append("")
        real_nodes["type"].append(0)
        real_nodes["keyword"].append("")
        real_nodes["usage_note"].append(beautify(concept_table["Definition"][i]))
        real_nodes["vn"].append("")
        real_nodes["source"].append("")
        real_nodes["media"].append("")

    ## convert examples into nodes. ID of node = ID of old example + 10^9 
    for i in range(len(example_table["ExampleID"])):
        real_nodes["id"].append(example_table["ExampleID"][i] + 10**9)
        real_nodes["user"].append(0)
        real_nodes["content"].append(beautify(example_table["Description"][i]))
        real_nodes["content_text"].append("")
        real_nodes["type"].append(1)
        real_nodes["keyword"].append(example_table["Keywords"][i])
        real_nodes["usage_note"].append(beautify(example_table["Source"][i]))
        real_nodes["vn"].append("")
        real_nodes["source"].append("")
        real_nodes["media"].append("")

    # write out node_info
    node_df = pd.DataFrame(real_nodes)
    node_info = node_df.to_csv(index=False)
        
    # convert the relations into edges

    real_edges = {
        "id": [],
        "node1": [],
        "node2": [],
        "type": []
    }

    rel_convert = {
        1 : 1,
        4 : 2,
    }
    for i in range(len(concept_relation_table["ID1"])):
        real_edges["id"].append(len(real_edges["id"]))
        real_edges["node1"].append(concept_relation_table["ID1"][i])
        real_edges["node2"].append(concept_relation_table["ID2"][i])
        rel = concept_relation_table["Relation"][i]
        if rel in rel_convert:
	        real_edges["type"].append(rel_convert[rel])
        else:
	        real_edges["type"].append(12)

    rel_convert = {
        0 : 3,
        1 : 4,
        2 : 5,
        3 : 6,
        4 : 7,
        5 : 8,
        6 : 9,
        7 : 10,
        8 : 11,
        9 : 12,
        10 : 12,
        11 : 12
    }

    for i in range(len(example_relation_table["wID"])):
        real_edges["id"].append(len(real_edges["id"]))
        real_edges["node1"].append(example_relation_table["wID"][i])
        real_edges["node2"].append(example_relation_table["eID"][i] + 10**9)
        rel = example_relation_table["Relation"][i]
        if rel in rel_convert:
	        real_edges["type"].append(rel_convert[rel])
        else:
	        real_edges["type"].append(12)
	
	# write out edge_info
    edge_df = pd.DataFrame(real_edges)
    edge_info = edge_df.to_csv(index=False)
    
    return load_backup.main(username, password, node_info, edge_info)






    
