from __future__ import annotations
import json
import math
from typing import List

# Node Class
# You may make minor modifications.

class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent
    
# Scapegoat Tree Class.
# DO NOT MODIFY.
class SGtree():
    def  __init__(self,
                  a    : int  = None,
                  b    : int  = None,
                  m    : int  = None,
                  n    : int  = None,
                  root : Node = None):
        self.m     = 0
        self.n     = 0
        self.a     = a
        self.b     = b
        self.root  = None
    
    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "k": node.key,
                "v": node.value,
                "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    
    def size(self, node: Node):
        if node is None:
            return 0
        return 1 + self.size(node.leftchild) + self.size(node.rightchild)
        
    def insert(self, key: int, value: str):
        # The implementation is basically creating the node, make it into BST, 
        # use the math and rebuild if necessary, and return it
        node = Node(key, value)
        tree = self.BSTandDepth(node)

        if tree > math.log(self.n) / math.log(self.b/self.a):
            p = node

            while ((self.size(p)/self.size(p.parent)) <= (self.a/self.b)):
                p = p.parent
            newtree = self.rebuildTree(p.parent)

            if (p.parent.parent is not None):
                if(p.parent.key < p.parent.parent.key):
                    p.parent.parent.leftchild = newtree
                else:
                    p.parent.parent.rightchild = newtree
            else:
                self.root = newtree
        self.m += 1
        self.n = self.n + 1
        return tree >= 0
    
    def BSTandDepth(self, node: Node):
        r = self.root
        if r is None:
            self.root = node
            self.n = self.n + 1
            return 0
        settle = False
        depth = 0

        while not settle:
            if node.key < r.key:
                if r.leftchild is not None:
                    r = r.leftchild
                else:
                    r.leftchild = node
                    node.parent = r
                    settle = True
            elif node.key > r.key:
                if r.rightchild is not None:
                    r = r.rightchild
                else:
                    r.rightchild = node
                    node.parent = r
                    settle = True
            else:
                return -1
            depth = depth + 1
        return depth
    
    def rebuildTree(self, root):
        def flat(node, nodes):
            if node == None:
                return
            flat(node.leftchild, nodes)
            nodes.append(node)
            flat(node.rightchild, nodes)
        
        def buildTreeFromSortedList(nodes, start, end, parent):

            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = Node(nodes[mid].key, nodes[mid].value)
            if(parent is None):
                node.parent = None
            else:
                node.parent = parent
            node.leftchild = buildTreeFromSortedList(nodes, start, mid-1, node)
            node.rightchild = buildTreeFromSortedList(nodes, mid+1, end, node)
            return node

        nodes = []
        flat(root, nodes)
        return buildTreeFromSortedList(nodes, 0, len(nodes)-1, root.parent)
    
    def minimum(self, x: Node):
        while x.leftchild != None:
            x = x.leftchild
        return x
    
    def delete(self, key: int):
        node = self.root
        parent = None
        is_left_child = True
        while node.key != key:
            parent = node
            if key > node.key:
                node = node.rightchild
                is_left_child = False
            else:
                node = node.leftchild
                is_left_child = True

        successor = None

        if node.leftchild == None and node.rightchild == None:
            pass
        elif node.leftchild == None:
            successor = node.rightchild
            successor.leftchild = node.leftchild
        elif node.rightchild == None:
            successor = node.leftchild
            successor.parent.leftchild = None
            successor.rightchild = node.rightchild
        else:
            successor = self.minimum(node.rightchild)
            if successor == node.rightchild:
                successor.leftchild = node.leftchild
            else:
                successor.leftchild = node.leftchild
                successor.parent.leftchild = None
                successor.rightchild = node.rightchild

        if parent == None:
            self.root = successor
        elif is_left_child:
            parent.leftchild = successor
        else:
            parent.rightchild = successor

        self.m -= 1
        if self.m > 2 * self.n:
            self.root = self.rebuildTree(self.root, self.size)

    def search(self, search_key: int) -> str:
        node = self.root
        list = []

        while node.key != search_key:
            list.append(node.value)
            if node.key < search_key:
                node = node.rightchild
            else:
                node = node.leftchild
        list.append(node.value)

        return json.dumps(list)