from typing import Self

# Jane Street Interview Q
# https://blog.janestreet.com/what-a-jane-street-dev-interview-is-like/

def f(x):
    # Computationally intensive function
    return x ** 100

# Simple hashtable memoization
class Memo:

    def __init__(self):
        self.state = {}

    def f(self, x):
        if x in self.state:
            return self.state[x]
        
        self.state[x] = f(x)
        return self.state[x]


MAX_CACHE_QUEUE_LEN = 100

# Now, adding a limit
class Memo2:

    def __init__(self):
        self.state = {}
        self.cacheQ = []

    def f(self, x):
        if x in self.state:
            return self.state[x]
        
        if len(self.cacheQ) > MAX_CACHE_QUEUE_LEN:
            self.cacheQ.pop(0)

        self.cacheQ.append(x)
        self.state[x] = f(x)
        return self.state[x]


class Node:
    left: Self
    right: Self
    input: int  # key for the state

class DoublyLinkedList:
    start: Node
    end: Node

    def add_to_end(self, other: Node):
        other.left = self.end
        self.end.right = other
        self.end = other
        other.right = None


class StateItem:
    return_val: int  # computationally intensive function return val
    cache_node: Node

    def __init__(self, return_val, cache_node):
        self.return_val = return_val
        self.cache_node = cache_node

# Implementing an LRU cache
class Memo3:

    def __init__(self):
        self.state = {}
        self.lru = DoublyLinkedList()

    def f(self, x):
        if x in self.state:
            state_item = self.state[x]
            state_item.cache_node.left.right = state_item.cache_node.right
            self.lru.add_to_end(state_item.cache_node)
            return state_item.return_val
        
        if len(self.state) > MAX_CACHE_QUEUE_LEN:
            key = self.lru.start.input
            # key is going to be evicted (LRU)
            self.state.pop(key)
            self.lru.start = self.lru.start.right
            self.lru.start.left = None


        state_item = StateItem(f(x), Node())
        if self.start == None:
            self.lru.start = self.lru.end = state_item.cache_node
        else:
            self.lru.add_to_end(state_item.cache_node)
        self.state[x] = state_item
        return state_item.return_val
        
