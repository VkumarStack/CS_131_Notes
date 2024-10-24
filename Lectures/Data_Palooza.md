# Data Palooza
## Variables
- A variable is a *symbolic name* that is associated with a storage location, containing either a *value* or a *pointer to a value*
  - A value is a *piece of data* that is either referred to by a variable or computed by a program expression
    - Values *can be pointers*, which themselves refer to *values*
  - E.g. `a: 3.14159` associates the variable with a value whereas `a: ADDR -> 3.14159` associates the variable with a *pointer to a value*
- Facets associated with a variable: *name*, *type*, *value*, *binding*, *storage*, *lifetime* (timeframe over which a variable exists, consider garbage collection), *scope* (when and where the variable name is *visible to the code*), *mutability*
  - For values, we care about its *type*, *value*, *storage*, *lifetime*, and its *mutability*
## Types
- A **type** is a classification used to identify a category of data, defining a *range of values*, *size and encoding*, *operations*, *usage context* (e.g. to functions), and *ways to convert or cast*
- Not all variables in languages have a *type* - if a variable is *bound to a single value*, then it has a type, but otherwise it could be bound to values of differing types over its lifetime (`x = 5` and then later on `x = "bletch"`)
  - Values, however, always have an associated type
- Types of Types:
  - **Primitives**: Integers, Floats, Chars, Enums, Bools, Pointers
  - **Composites**: Unions, Classes, String, Tuples, Structs, Containers
  - Others: Functions, Generics (e.g. Templates), Boxed Type (wrap around a primitive, allowing for them to be mutated)
- Beyond the built-in types provided by languages, it is often possible for users to *define new types* 
  - Every time a class is created, the language *implicitly defines a type* associated with that class
    - This also applies to structs, enums, and interfaces (in general)
  - Example:
    -     class Circle {
            public:
              ...
            private:
              ...
          }
    - This implicitly defines a new type `Circle`
- Many types have a **supertype-subtype** relationship, where a *subtype inherits properties and behaviors from its supertype*
  - A key example of this is with *class inheritance*
    -     class Person {
            public:
              virtual void eat()
                { cout << "Nom Nom"; }
              virtual void sleep()
                { cout << "Zzzzzzz"; }
          }
          class Nerd: public Person {
            public:
              virtual void study()
                { cout << "Studying..."; }
          }
    - This implictly defines types for *Nerd* and *Person*, and *Nerd* is a subtype of *Person*
  - **Interfaces** can also support this relationship, where we say a class *implements an interface*
    - Recall that interfaces are generally *abstract*
    - Example: `Car implements Washable`, so Car is a subtype of Washable
  - Since each type is associated with a specific set of operations, when a subtype is defined it also inherits *all operations of its supertype*
    - There is an operational relationship here, and this can be used to determine operational compatibility between types to support things like *type casting* and *polymorphism*
    - Example:
      -     class Person
              ...
            class Nerd : public Person
              ...
            void bePersoney(Person &p)
              ...

            Nerd nancy;
            bePersoney(nancy);
      - Even though `nancy` is a `Nerd`, it can still be passed into the `bePersoney` method because `Nerd` inherit all functions supported by a `Person`
- **Value types** are types that can be used to instantiate *objects or values* (and define pointers, objects, and references)
  - On the other hand, **reference types** are types that *cannot be used to instantiate objects or values*, but rather can only be used to define *pointers, objects, or references*
    - An example of this is with *abstract classes*
  - Example:
    -     class Dog {
            public:
              Dog(string n) { name = n; }
              void bark() { cout << "Woof"; }
            private:
              string name_;
          }

          class Shape {
            public: 
              Shape(Color c) { color_c = c; }
              virtual double area() = 0;
            private:
              Color color_;
          }

          // This is a value type
          Dog d("Kuma"), *p;

          // This is a reference type; we cannot insantiate a Shape object
          // because it is not implemented (it is abstract), so all we can do 
          // is declare a pointer
          Shape *s;
- **Type equivalence** is the criteria by which programming languages determine whether two values or variables are of equivalent types
  - One approach is to use **name equivalence**, which denotes equivalence if two variables / values have identical type names
      -     struct S { string a; int b; };
            struct T { string a; int b; };

            int main() {
              S s1, s2;
              T t1, t2;
              s1 = s2; // Works
              s1 = t1; // Fails, despite equivalent structure due to name equivalence
            }
      - This is typical to statically typed languages
  - Another approach is **structural equivalence**, which denotes equivalence if structures are identical, regardless of type names
      -     type S = { a: string, b: number };
            type T = { a: string, b: number };

            function main() {
              let s1, s2 : S;
              let t1, t2 : T;
              s1 = s2; // Works
              s1 = t1; // Works
            }
      - This is typical of dynamically typed languages
- Type Checking:
  - Strictness:
    - **Strong Type Checking**: The language's typing system *guarantees* that all operations are only invoked on objects/values of appropriate types
      - This ensures that there will *never be undefined behavior at runtime due to type-related issues*
      - For a language to be strongly typed, it must be **type-safe**, meaning it will prevent an operation on variable *x* if *x*'s type does not support that operation, and it must be **memory-safe**, meaning that inappropriate memory accesses are prevented
        - Memory safety is needed for strong typing because invalid memory accesses can result in types being accessed as if they were a *different type*
          -     int arr[3] = {10, 20, 30};
                float salary = 120000.50;
                // Because of how variables are stored on the stack, this will access the float like it is an int
                cout << arr[3];
      - To implement strong typing:
        - Before an expression is evaluated, the compiler or interpreter *validates* that all of the operands used in the expression have compatible types
          -     y = Dog("Koda")
                x = 5 + y // Error
        - All conversions and casts between different types are checked and if the types are incompatible, some sort of error is generated
          -     y = Dog("Koda")
                x = (int)y // Error
        - Pointers are either set to null or assigned to point at a valid object at creation
          -     Dog *x
                print(x) // Error
        - Accesses to arrays are bound checked
          -     int x[5]
                print(x[100]) // Error
        - The language ensures that objects cannot be used after they are destroyed 
          -     delete d;
                d->bark(); // Error
      - In a strongly typed language, a type cast is *checked* (typically at runtime, at the time of the cast) and throw an error if the cast is illegal
        - `C++` is *not strongly typed*, and so it is possible to perform unsafe casts - that is, casts that will succeed with incompatible types
      - Strongly typed languages are preferred because they reduce software vulnerabilities and can allow for early detection of bugs
        - However, strongly typed languages are *slower* compared to weakly typed languages due to the need to check for safety
    - **Weak Type Cheecking**: The language's type system does *not guarantee* that all operations are invoked on objects/values of appropriate types
      - Weakly typed languages are *not type safe* and are *not memory safe*
      - There are can be *undefined behavior at runtime* since errors are not generated upon illegal operations
        - This usually means that the behavior is *non-deterministic*, though if behavior is *deterministic* (e.g. ran one million times and had the same result each time) for illegal operations then it is not necessarily weakly typed
        - *Implicit behavior* is not indicative of weak typing (e.g. implicit cast of `"cat"` to `0` and `"90"` to `90` when doing `10 + "90" + "cat"`)
  - Compile-Time (or before running) versus Runtime:
    - **Static Typing**: Prior to execution, the type checker determines the type of every expression and ensures all operations are compatible with the types of their operands
      - Some statically typed languages have explicit type annotations - e.g. `C++`: `int add(int a, int b) {return a + b; }`
      - Other statically typed languages *do not have explicit type annotations*: - e.g. `Haskell`: `abs a = if a > 0 then a else (-a)`
        - Here, there is *type inference*, as it can be inferred that `a` is numeric due to the comparison with `0`, and then it can also infer that the return type is also numeric since the `abs` function returns a numeric type
        - Type inference is never completely simple, as there can be ambiguity (e.g. `x + 5` could have `x` inferred as either an `int` *or* a `double`), and so it may be necessary to look at the *entire program*
      - If the type checker cannot assign distinct types to all variables, functions, and so forth, then it generates a *compiler error*
        - If the program type checks, though, it means the code is mostly safe (though there still might be checks done at runtime)
      - To support static typing, languages *must have a fixed type bound to each variable at definition*; once a variable's type is assigned, it cannot be changed
        - Example: Consider Python, which is *not statically typed*
          -     def foo(x):
                  if x > 5:
                    a = 10
                  else:
                    a = "cats"
          - There is no way a compiler could figure out the type of *variable a* when *compiling* this code
      - In statically typed languages, there may still be a need to check *some* types at runtime. This is typically the case when *downcasting* is performed (cast superclass down to a subclass)
        -     class Person { ... };
              class Student : public Person { ... };
              class Doctor : public Person { ... };
              void partay (Person &p) {
                // Assumes only students go to parties 
                Student &s = dynamic_cast<Student &>(p);
                s.getDrunkAtParty();
              }

              int main() {
                Doctor d("Dr Fauci"); 
                // This will be compiled, but at runtime this will cause an error
                partay(d);
              }
        - The downcast *must be checked at runtime* because there is no way to know at runtime, in general, whether or not the Person being passed in can actually be downcasted as a student
      - Static typing checking is *conservative* - it is entirely possible for static type checking to prevent technically correct programs from compiling because the type checker is overly conservative
        -     void handlePet(Mammal& m) {
                m.makeNoise(); // Defined for all mammals
                if (m.name() == "Spot")
                  m.bite(); // Defined only for dogs, not cats
                else (m.name() == "Meowmer")
                  m.scratch(); // Defined only for cats, not for dogs
              }
              int main() {
                Dog d("Spot");
                Cat c("Meowmer");
                handlePet(d);
                handlePet(c);
              }
          - Although this code would work, it *does not compile* because the type checker is conservative
      - Static typing can be beneficial because it produces faster code (fewer runtime checks), detects bugs earlier in development, and does not require custom code to check types
        - As downsides, though, static typing may result in longer compilation and also may not allow perfectly correct code to compile due to the conservative nature of the type checker
    - **Dynamic Typing**: As the program executes (so at *runtime*), the type checker ensures that each primitive operation is invoked with values of the right types
      - During runtime, if an illegal operation occurs on a value, then an exception is generated or the program crashes
        -     def add(x, y):
                print(x + y)
              def foo():
                a = 10
                b = "cooties"
                add(a, b) # This will cause an error during runtime
      - Typically, types are *not assigned to variables* (e.g. Python variables do not have a fixed type, and so they can refer to various types of values over their lifetime)
        - For this reason, types are typically associated with *values* but not the *variables holding them* 
      - Dynamically typed languages perform type checking by storing a *type tag* along with every value, and this information is used to check all operations
        -     a = 10
              b = "nerd"
              a + b 
          - `a` refers to something along the lines of `type: int, value: 10`
          - `b` refers to something along the lines of `type: string, string: "nerd"`
          - When the add is performed, the type tags of the values stored by each variable are checked, and since they are not compatible with the addition operator an error is raised
      - It is typically necessary in these languages to perform **type introspection** in code to check types *explicitly*
        - E.g. `if type(v) == "string" then...`
      - Dynamically typed languages can still have *type annotations*, which require that certain variables (e.g. parameters) must hold a certain type 
        - This does not restrict the variable because variables do not have types - rather it restricts the type of the value held by the variable
        - E.g. `print_n(v, n::Int)`
          - When a variable is passed in for `n`, the value that the variable is referring to (so referencing the pointer or object reference) is checked to see if the type is of an `Int`
      - A consequence of dynamic typing is *duck typing*: at runtime, the program checks the suitability for an operation based on the presence of *required methods* rather than the object's type
        - Because of this, **dynamically typed languages do not involve explicit casting**
        -     class PersonInDuckSuit:
                def quack(self): print('Hi! Uh...I mean quack!')
              class Duck:
                def quack(self): print('Quack quack quack!')
              class Vehicle:
                def drive(self): print('Vroom')
              
              def quack_please(x):
                x.quack()

              p = PersonInDuckSuit()
              d = Duck()
              v = Vehicle()

              quack_please(p) # Works 
              quack_please(d) # Works 
              quack_please(v) # Raises an error
        - Python's Duck Typing allows for classes to support certain interfaces by simply defining methids:
          - `__iter__` and `__next__` allows for a class to be iterable 
            -     class Cubes:
                    def __init__(self, lower, upper):
                      self.upper = upper
                      self.n = lower 
                    def __iter__(self):
                      return self
                    def __next__(self):
                      if self.n < self.upper:
                        s = self.n ** 3
                        self.n += 1
                        return s 
                      else:
                        raise StopIteration

                    for i in Cubes(1, 4):
                      print(i)

          - `__str__` allows for any class to be printable
          - `__eq__` allows for any class to be comparable
        - Duck typing allows for more flexibility, simpler code, faster prototyping, but is slower and more unsafe
    - **Gradual Typing**: One can *choose* whether to specify a type for variables or parameters
      - If a variable is untyped, then type errors for that variable are *only detected during runtime*, but if a variable is typed then *some type errors can be detected at compile time*
        - If an *untyped variable* is passed to a *typed variable* (like in a function), then the code would still compile but there would be a *runtime check*
          -     def square(x : int):
                  return x * x
                def what_happens(y):
                  print(square(y))
      - Gradually typed languages use *type tags* (for runtime checks) and *variable types* (for compilation checks)
## Type Conversions and Casting
- There is a difference between a **type conversion** and a **type cast**
  - A **type conversion** takes a value of type *A* and generates a *new value* of type *B*
    -     int main() {
            float pi = 3.141;
            // This is a conversion, because the bit representations are different (floating point versus int)
            cout << (int) pi; 
          }
    - Type conversions are typically used to convert between *primitives*
  - A **type cast** takes a value of type *A* and *views it as if it were a value of type B* - no new value is created
    -     class Person { ... };
          class Student : public Person { ... };
          int main() {
            Student mary;
            ...
            Person &p = (Person &)mary;
            cout << "Hi " << p.name();
          }
      - When the cast is performed, the attributes of `mary` that correspond to a `Person` object can be accessed, but while `mary` is cast as a person, the attributes corresponding only to a `Student` cannot be accessed
    -     int main() {
            int val = -42;
            // Views val as an unsigned int and prints out 4294967254
            cout << (unsigned int) val;
          }
      - This is an example of casting without classes
    - Type casts are typically used with *objects*
- Conversions and casts can either be *explicit* or *implicit*
  - Explicit Conversion:
    -     void foo(int i) { ... }
          int main() {
            float f = 3.14;
            foo((int)f);
          }
  - Explicit Cast:
    -     void feed_young(Animal *a) {
            if (a->has_fur()) {
              ((Mammal *)a)->produce_milk();
            }
          }
  - Implicit Conversion (aka coercion):
    -     void foo(float f) { ... }
          int main() {
            int i = 42;
            foo(i);  
          }
  - Implicit Cast:
    -     void use_potty(Person *p) { p->poop(); }
          int main() {
            Nerd *n = new Nerd("paul");
            use_potty(n);
          }
    - Most implicit casts are *upcasts*, meaning they go from a subclass to a superclass
      - *Downcasts* are usually explicit because they are not always valid
  