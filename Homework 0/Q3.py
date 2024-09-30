def find_biggest(arr):
  if len(arr) == 1:
    return arr[0]
  
  rest = find_biggest(arr[1:])
  return max(arr[0], rest)

def index_find_biggest(arr):
  if len(arr) == 1:
    return 0
  
  rest = index_find_biggest(arr[1:]) + 1
  if arr[0] > arr[rest]:
    return 0
  return rest

def del_item(arr, item):
  if len(arr) == 1:
    return [] if arr[0] == item else [arr[0]]
  
  rest = del_item(arr[1:], item)
  if arr[0] == item:
    return rest
  else:
    return [arr[0]] + rest

print(find_biggest([-1,10,3, 100, 541, 54, 12, -1, 42]))
print(index_find_biggest([-1,10,3, 100, 541, 54, 12, -1, 42]))

print(del_item([6, 1, 2, 6, 4, 5, 6, 6, 6, 6], 6))