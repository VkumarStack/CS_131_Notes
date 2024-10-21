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
      - This can be checked either at runtime or at compilation
    - **Weak Type Cheecking**: The language's type system does *not guarantee* that all operations are invoked on objects/values of appropriate types
  - Compile-Time (or before running) versus Runtime:
    - **Static Typing**: Prior to execution, the type checker determines the type of every expression and ensures all operations are compatible with the types of their operands
      - Some statically typed languages have explicit type annotations - e.g. `C++`: `int add(int a, int b) {return a + b; }`
      - Other statically typed languages *do not have explicit type annotations*: - e.g. `Haskell`: `abs a = if a > 0 then a else (-a)`
        - Here, there is *type inference*, as it can be inferred that `a` is numeric due to the comparison with `0`, and then it can also infer that the return type is also numeric since the `abs` function returns a numeric type
        - Type inference is never completely simple, as there can be ambiguity (e.g. `x + 5` could have `x` inferred as either an `int` *or* a `double`), and so it may be necessary to look at the *entire program*
      - If the type checker cannot assign distinct types to all variables, functions, and so forth, then it generates a *compiler error*
        - If the program type checks, though, it means the code is mostly safe (though there still might be checks done at runtime)
      - To support static typing, languages *must have a fixed type bound to each variable at definition*, once a variable's type is assigned, it cannot be changed
        - Example: Consider Python, which is *not statically typed*
          -     def foo(x):
                  if x > 5:
                    a = 10
                  else:
                    a = "cats"
          - There is no way a compiler could figure out the type of *variable a* when *compiling* this code
    - **Dynamic Typing**: As the program executes (so at *runtime*), the type checker ensures that each primitive operation is invoked with values of the right types
