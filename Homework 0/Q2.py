class Point():
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def display(self):
    print("({}, {})".format(self.x, self.y))
    

def modify(p):
  p.x = 50
  p = Point(20, 20)

pt = Point(10, 10)
modify(pt)
pt.display()