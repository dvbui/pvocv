# Object structure

## Node
- id: integer
- user: integer - the user id
- content: string (in html form)
- content_text: string
- type: int
- keyword: string,
- usage_note: string (in html form)
- vn: string
- source: string
- media: string (in html form)
## LinkType
- id: integer
- rel: str
- user: integer or NULL - the user id. NULL represents common link type.
## Edge
- id: integer - the id of the edge
- node1: Node - the parent node
- node2: Node - the child node
- type: LinkType - the relation between two nodes