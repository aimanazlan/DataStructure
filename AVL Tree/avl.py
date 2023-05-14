import json
from typing import List
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
# DO NOT MODIFY
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "k": node.key,
            "v": node.value,
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

# Height of (sub)tree rooted at root.
def height(root: Node) -> int:
    if root is None:
        return -1
    else:
        return 1 + max(height(root.leftchild), height(root.rightchild))

# Insert.
def insert(root: Node, key: int, value: str) -> Node:
    if root is None:
        return Node(key=key, value=value)
    elif key < root.key:
        root.leftchild = insert(root.leftchild, key, value)
    else:
        root.rightchild = insert(root.rightchild, key, value)

    bal = height(root.leftchild) - height(root.rightchild)

    if bal > 1 and key < root.leftchild.key:
        return right_rotate(root)

    if bal < -1 and key > root.rightchild.key:
        return left_rotate(root)

    if bal > 1 and key > root.leftchild.key:
        root.leftchild = left_rotate(root.leftchild)
        return right_rotate(root)

    if bal < -1 and key < root.rightchild.key:
        root.rightchild = right_rotate(root.rightchild)
        return left_rotate(root)

    return root

def left_rotate(target):
    y = target.rightchild
    T2 = y.leftchild
    y.leftchild = target
    target.rightchild = T2

    return y

def right_rotate(target):
    y = target.leftchild
    T3 = y.rightchild
    y.rightchild = target
    target.leftchild = T3

    return y

def delete(root: Node, keys: List[int]) -> Node:
    def inorder(root: Node, result: List[Node], tag: List[int]) -> None:
        if root is None:
            return
        inorder(root.leftchild, result, tag)
        if root.key not in tag:
            result.append(root)
        inorder(root.rightchild, result, tag)
    tag = set(keys)
    result = []
    inorder(root, result, tag)

    new_r = None
    for node in result:
        new_r = insert(new_r, node.key, node.value)
    
    return new_r

def search(root: Node, search_key: int) -> str:
    count = 0
    value = None
    curr = root
    while curr is not None:
        if curr.key == search_key:
            value = curr.value
            count += 1
            break
        elif curr.key < search_key:
            curr = curr.rightchild
        else:
            curr = curr.leftchild
        count += 1

    return json.dumps([count, value])


# Range Query.
def rangequery(root: Node, x0: int, x1: int) -> List[str]:
    if root is None:
        return []
    if x0 <= root.key <= x1:
        return [root.value] + rangequery(root.leftchild, x0, root.key - 1) + rangequery(root.rightchild, root.key + 1, x1)
    elif root.key < x0:
        return rangequery(root.rightchild, x0, x1)
    else:
        return rangequery(root.leftchild, x0, x1)

