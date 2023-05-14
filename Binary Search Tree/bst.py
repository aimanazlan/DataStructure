import json
from collections import deque
# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self, 
                  key        = None, 
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.

def dump(root: Node) -> str:
    def _to_dict(node) -> dict:    
        return {
            "k": node.key,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else 
None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else 
None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr)


# For the tree rooted at root, insert the given key and return the root node.
# The key is guaranteed to not be in the tree.
def insert(root: Node, key: int) -> Node:
    if root is None:
        return Node(key)
    if key < root.key:
        root.leftchild = insert(root.leftchild, key)
    else:
        root.rightchild = insert(root.rightchild, key)
    return root

# For the tree rooted at root, delete the given key and return the root node.
# The key is guaranteed to be in the tree.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    if root is None:
        return None
    elif key < root.key:
        root.leftchild = delete(root.leftchild, key)
        return root
    elif key > root.key:
        root.rightchild = delete(root.rightchild, key)
        return root
    else:
        if root.leftchild is None:
            return root.rightchild
        elif root.rightchild is None:
            return root.leftchild
        else:
            curr = root.rightchild
            while curr.leftchild is not None:
                curr = curr.leftchild
            root.key = curr.key
            root.rightchild = delete(root.rightchild, curr.key)
    return root

# For the tree rooted at root, calculate the list of keys on the path from the root to the search key.
# Return the json stringified list.
# The key is guaranteed to be in the tree.
def search(root: Node, search_key: int) -> str:
    pathway = []
    curr = root
    pathway.append(curr.key)
    if search_key < curr.key:
        curr = curr.leftchild
    elif search_key > curr.key:
        curr = curr.rightchild
    else:
        return(json.dumps(pathway))

# For the tree rooted at root, dump the preorder traversal to a stringified JSON list and return.
def preorder(root: Node) -> str:
    res = []
    preOrder(root, res)
    return(json.dumps(res))

def preOrder(root: Node, res: list):
    if root is not None:
        res.append(root.key)
        preOrder(root.leftchild, res)
        preOrder(root.rightchild, res)
    else:
        return

# For the tree rooted at root, dump the inorder traversal to a stringified JSON list and return.
def inorder(root: Node) -> str:
    res = []
    inOrder(root, res)
    return(json.dumps(res))

def inOrder(root: Node, res: list):
    if root is not None:
        inOrder(root.leftchild, res)
        res.append(root.key)
        inOrder(root.rightchild, res)
    else:
        return
    
# For the tree rooted at root, dump the postorder traversal to a stringified JSON list and return.
def postorder(root: Node) -> str:
    res = []
    postOrder(root, res)
    return(json.dumps(res))

def postOrder(root: Node, res: list):
    if root is not None:
        postOrder(root.leftchild, res)
        postOrder(root.rightchild, res)
        res.append(root.key)
    else:
        return

# For the tree rooted at root, dump the BFT traversal to a stringified JSON list and return.
# The DFT should traverse left-to-right.
def bft(root: Node) -> str:
    if root is None:
        return "[]"
    queue = deque([root])
    res = []
    while len(queue) > 0:
        node = queue.popleft()
        res.append(node.key)
        if node.leftchild is not None:
            queue.append(node.leftchild)
        if node.rightchild is not None:
            queue.append(node.rightchild)
    return json.dumps(res)  