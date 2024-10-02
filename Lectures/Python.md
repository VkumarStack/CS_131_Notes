# Essential Python
## Allocation of Objects
- In C++, objects can be instantiated either locally via the stack or allocated on the heap
  - Stack: `Circle c(10)`
    - This gives a *direct reference to the object*
  - Heap: `Circle *p = new Circle(20)`
    - This gives a *pointer to the object's memory location*
- In Python, objects can *only* be instantiated via the heap
  - `c = Circle(10)`
  - Objects in Pythons are *pointers*, though they are known as **object references**
    - This means that each variable does not directly reference the object but rather holds the memory address of that object
  - *Every* single thing in Python is an object, even primitives such as Integers
    - Integers are *immutable*, so the following code does not alter the existing Integer value in memory but rather allocates a new Integer
      -     i = 42
            i = i + 1
    - This can obviously be very inefficient
## Class Variables
- Example:
  -     class Thing:
          thing_count = 0
        def __init__(self, v):
          self.value = v
          # This is associated with the class itself
          Thing.thing_count += 1 
          # This is associated with a specific instance of this class
          self.thing_num = Thing.thing_count
  -     from thing import Thing
        t1 = Thing("a")
        print(f"{t1.thing_num} {Thing.thing_count}")

        t2 = Thing("b")
        print(f"{t1.thing_num} {Thing.thing_count}")
        print(f"{t2.thing_num} {Thing.thing_count}")

  - This will print `1 1`, `1 2`, and finally `2 2`
    - This is because the increment in the constructor will increment for the entire *class*, whereas the assignment in the constructor will assign only for that object instance
    - The `thing_count` member variable is *not per object* but for the *entire class* - it is shared
      - Class methods are shared for the *entire class*

## Copying of Objects
-     import math
      class Circle:
        def __init__(self, rad):
          self.rad = rad
        
        def area(self):
          return math.pi * self.rad**2
        
        def set_radius(self, rad):
          self.rad = rad


        c = Circle(10)
        print(c.area(10))
        c2 = c
        c.set_radius(0)
        print(c2.area())

  - This will print `314` and then `0`
    - The assignment `c2 = c` will copy the *address* of the circle object (not copy the object itself), so any changes made to it via *either variable* will change the same object in memory
- To create a copy of an object, one must use the *copy module*
  -     import copy
        c = Circle(10)
        print(c.area())

        c2 = copy.deepcopy(c)
        c.set_radius(0) # Now only affects c's object and not c2
  - A deep copy is *recursive* - it makes a copy of the top-level object *and* every object referred to directly or indirectly by the top-level object
    - `copy.deepcopy`
  - A shallow copy just makes a copy of the *top-level object*
    - `copy.copy`
## Equality in Python
-     fav = 'pizza'
      a = f'I <3 {fav}!'
      b = f'I <3 {fav}!'
      c = a

      # Check for value equality
      if a == b:
        print("Same value")
      # Check for same object reference
      if c is a:
        print("c and a refer to the same obj")
      # Check for differing object reference
      if a is not b:
        print("a and b refer to diff. objs")
  - All three will be printed
## Inheritance
-     class Pet:
        def __init__(self, name="Koda"):
          print(f"Its name is {name}!")
        
        def play(self):
          self.do_playful_thing()

        def do_playful_thing(self):
          print("prance")

      class Dog(Pet):
        def __init__(self):
          print("A dog is born!")
        
        def do_playful_thing(self):
          print("fetch)

        def give_treat(self):
          super().do_playful_thing()
          print("woof!")
  - This will print: `A dog is born`, `prance`, `woof`, `fetch`
    - In Python, the base constructor is *not implicitly called* - it must be explicitly called using `super` - which is why only "A dog is born!" is printed
    - `super` is used to call the base class's version of a method
    - When a method only available to the base class is called, and it calls a method overriden by the derived class, then the *most recent, overriden* version of the method will be called
## Strings
- In Python, strings are *also objects* and are *immutable*
  - Any method or operation that appears to modify strings are actually just creating new ones
  - Example: All of the concatenation operations create *new* strings
    -     fact1 = "Del Taco rules!"
          fact2 = "CS131 is lit"
          truth = fact1 + fact2
## Lists
- Lists in Pythons are implemented using *arrays* 
  - There are O(1) accesses based on an index
  - Appending one list on to another is O(n + m)
  - Lists are represented as arrays of *object references*
    - Each cell / element of a list is an object reference, so it holds the address to the object in memory
- Example:
  -     primes = [1, 2, 3]
        odds = ['carey, 'todd']

        lol = [primes, odds]

        primes[2] = 7
        odds.append('paul')
        odds = [1, 3, 5]

        print(lol)
    - This will print `[[1, 2, 7], ['carey', 'todd', 'paul']]`
## Parameter Passing
- As mentioned earlier, Python passes parameters *only by object reference* (this is the same as pass by pointer in C++)
## Default Parameters
- Example:
  -     def puzzle(w, words = []):
          words.append(w)
          print(words)
        
        puzzle("This")
        puzzle("is")
        puzzle("confusing")

    - This will print out `["This"]`, `["This", "is"]`, `["This", "is", "confusing"]`
    - This is because each function in Python results in a special object being allocated, which contains the *default parameters* as member variables
      - This means that the default parameter is *shared*, so each time the default parameter is used in the function, something is appended to it and this change is reflected across all function calls that use the default parameter
      - If the default parameter were *immutable*, then this would not be an issue since any changes to it would only be reflected locally
  - Fix:
    -     def puzzle(w, words = None):
            if words is None:
              words = []
            words.append(w)
            print(words)
          
          puzzle("This")
          puzzle("is")
          puzzle("confusing")