class Node:

    def __init__(self, symbol):
        self.symbol = symbol
        self.edges = {}

    # conversion factor from self to other
    def add_edge(self, other, factor):
        self.edges[other.symbol] = factor
        other.edges[self.symbol] = 1 / factor


conversion_data = [
    ("m", 3.28, "ft"),
    ("ft", 12, "in"),
    ("hr", 60, "min"),
    ("min", 60, "sec"),
]

# Hashmap, hashed on the symbol to avoid iterating through all nodes
conversion_graph = {}

for sym, factor, other in conversion_data:
    if sym not in conversion_graph:
        conversion_graph[sym] = Node(sym)

    if other not in conversion_graph:
        conversion_graph[other] = Node(other)

    sym_node = conversion_graph[sym]
    other_node = conversion_graph[other]

    sym_node.add_edge(other_node, factor)

# Graph is built

# Searching using BFS to find quickest path.
def search(inp):
    factor, sym, other = inp
    visited = set()
    queue = []
    queue.append((factor, conversion_graph[sym]))
    while len(queue) > 0:
        currVal, next = queue.pop(0)
        if next in visited:
            continue
        
        visited.add(next)
        if other in next.edges:
            return currVal * next.edges[other]
        
        for node, factor in next.edges.items():
            queue.append((factor * currVal, conversion_graph[node]))
    
    return "Not possible"

print(search((2, "m", "in")))
print(search((13, "in", "m")))
print(search((3, "hr", "m")))