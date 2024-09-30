class LinkedList():
  class Node():
    def __init__(self, val, next=None):
      self.val = val
      self.next = next
    
  def __init__(self, head=None):
    self.head = head

  def add_to_front(self, val):
    new_node = self.Node(val, self.head)
    self.head = new_node

  def print(self):
    node = self.head
    while node is not None:
      print(node.val)
      node = node.next

