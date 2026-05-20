from typing import Self, Any
from collections import deque

class Node:
  children: dict[str, Self]
  value: Any | None
  
  def __init__(self) -> None:
    self.children = {}
    self.value = None
    
  def next(self, char: str):
    self.children.setdefault(char, Node())
    return self.children[char]

  def search(self, char: str) -> Self | None:
    return self.children.get(char, None)

class Trie:
  root: Node
  
  def __init__(self) -> None:
    self.root = Node()
    
  def add(self, key: str, value: Any) -> None:
    if not key:
      raise ValueError("Empty key not allowed")

    node = self.root
    for char in key:
      node = node.next(char)
    node.value = value
  
  def search(self, key: str) -> Any | None:
    node = self.root
    for char in key:
      node = node.search(char)
      if node is None:
        return None
    
    return node.value if node else None
    
  def clear(self) -> None:
    self.root = Node()
    
  def delete(self, key: str) -> None:
    if not key:
      raise ValueError("Empty key not allowed")
    
    node = self.root
    for char in key[:-1]:
      node = node.search(char)
      if node is None:
        raise ValueError(f"{key} not present in trie")
    
    final = node.children.get(key[-1])
    if final is None:
        raise ValueError(f"{key} not present in trie")
    final.value = None

  # TODO: Solution when you also want to prune dead branches (in case of large tries and frequent deletions)
  # def delete(self, key: str) -> None:
  #   pass

  def prefix_match(self, prefix: str) -> list[tuple[str, Any]]:
    node = self.root
    
    for char in prefix:
      node = node.search(char)
      if node is None:
        return []
    
    results = []
    visit = deque([(prefix, node)])
    while len(visit) > 0:
      # deque popleft is O(1) while array's pop(0) is O(n)
      key, node = visit.popleft()
      if node.value is not None:
        results.append((key, node.value))

      for char, child in node.children.items():
        visit.append((key + char, child))
    
    return results

if __name__ == "__main__":
    trie = Trie()

    # === Basic Insertion and Search ===
    trie.add("cat", 1)
    trie.add("car", 2)
    trie.add("dog", 3)

    assert trie.search("cat") == 1
    assert trie.search("car") == 2
    assert trie.search("dog") == 3
    assert trie.search("cow") is None
    assert trie.search("") is None

    # === Prefix Matching ===
    assert set(trie.prefix_match("ca")) == {("cat", 1), ("car", 2)}
    assert set(trie.prefix_match("c")) == {("cat", 1), ("car", 2)}
    assert trie.prefix_match("dog") == [("dog", 3)]
    assert trie.prefix_match("z") == []

    # === Delete Leaf Node ===
    trie.delete("cat")
    assert trie.search("cat") is None
    assert trie.search("car") == 2, f"{trie.search('car')} != 2"  # Ensure sibling unaffected
    assert set(trie.prefix_match("ca")) == {("car", 2)}

    # === Delete Shared Prefix Root ===
    trie.delete("car")
    assert trie.search("car") is None
    assert trie.prefix_match("c") == []

    # === Delete Remaining Node ===
    assert trie.search("dog") == 3
    trie.delete("dog")
    assert trie.search("dog") is None
    assert trie.prefix_match("d") == []

    # === Reinsert and Test ===
    trie.add("cart", 42)
    trie.add("carrot", 99)
    assert trie.search("cart") == 42
    assert trie.search("carrot") == 99
    assert set(trie.prefix_match("car")) == {("cart", 42), ("carrot", 99)}

    # === Delete Node with Descendants ===
    trie.delete("cart")
    assert trie.search("cart") is None
    assert trie.search("carrot") == 99  # Must still exist

    # === Edge Case: Attempt to Delete Nonexistent Key ===
    try:
        trie.delete("nonexistent")
        assert False, "Expected exception for deleting nonexistent key"
    except ValueError:
        pass

    # === Edge Case: Empty String ===
    try:
        trie.delete("")
        assert False, "Expected exception for deleting empty string"
    except ValueError:
        pass

    # === Clear Trie ===
    trie.clear()
    assert trie.search("carrot") is None
    assert trie.prefix_match("") == []

    print("All tests passed.")
