# Gotchas
- For Python lists, there is a difference in doing `lst1 += lst2` and `lst1 = lst1 + lst2`
  - `lst1 += lst2` *mutates* the list - it is shorthand for `lst1.extend(lst2)`
  - `lst1 = lst1 + lst2` *creates a shallow copy of lst1 and lst2* and assigns it to `lst1`'s variable
  - Python list operations that create copies (e.g. slicing or `+`) create *shallow* copies not deep copies
