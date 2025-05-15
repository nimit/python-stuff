# heap is a complete binary tree
# MOST IMPORTANT: All SUB TREES ARE MIN HEAPS!
# This means that only need to heapify if a swap happens.
# Otherwise, one can remain rest assured that everything is perfect.


# [1, 2, 3, 4, 5, 6, 7]
#  0  1  2  3  4  5  6
#         1
#     2        3
#   4   5    6   7

class MinHeap:
    def __init__(self):
        self.tree = []

    def size(self): return len(self.tree)

    def __eq__(self, value):
        if isinstance(value, MinHeap):
            return self.tree == value.tree
        return False

    # There needs to be two methods. One to heapify from bottom-up, other to heapify from top-down....
    # Use the bottom-up when adding and top-down when removing

    def swap(self, index1, index2):
        temp = self.tree[index1]
        self.tree[index1] = self.tree[index2]
        self.tree[index2] = temp

    def heapifyDown(self, index):
        if index >= len(self.tree): return
        left_child = index * 2 + 1
        right_child = index * 2 + 2
        
        if left_child < len(self.tree) and self.tree[left_child] < self.tree[index]:
            self.swap(left_child, index)
            self.heapifyDown(left_child)
        
        if right_child < len(self.tree) and self.tree[right_child] < self.tree[index]:
            self.swap(right_child, index)
            self.heapifyDown(right_child)
        

    # heapify from bottom up, turning each node into its own min heap
    def heapifyUp(self, index):
        if index <= 0: return
        parent = (index - 2) // 2 if index % 2 == 0 else (index - 1) // 2
        # print(f"heapify called at {index} | parent: {parent}")
        if self.tree[index] < self.tree[parent]:
            self.swap(index, parent)
            self.heapifyUp(parent)

    def push(self, element):
        print(f"pushed {element}")
        self.tree.append(element)
        self.heapifyUp(len(self.tree) - 1)

    def pop(self):
        self.swap(0, -1)  # swap 0 & last (optimization so if chilrens' heaps remain intact and nothing changes)
        ret_element = self.tree.pop(-1)
        self.heapifyDown(0)
        return ret_element
    
    def visualize(self):
        if len(self.tree) == 0: return None

        height = int(len(self.tree) ** 0.5) + 1
        start = 0
        offsetMax = 1
        for i in range(height):
            # Improve spacing
            for j in range(start, min(len(self.tree), start + offsetMax)):
                print(" "*(2 ** (height - i - 1) - 1), end=" ")
                print(self.tree[j], end="")
            print()
            start += offsetMax
            offsetMax *= 2


heap = MinHeap()
for i in range(10, 0, -1):
    heap.push(i)

heap.visualize()

for i in range(heap.size()):
    print(heap.pop())