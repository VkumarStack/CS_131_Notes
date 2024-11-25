# Control Palooza
## Expressions, Associativity and Order of Evaluation
- The order in which expressions are evaluated are important, especially if certain functions have *side-effects*
  - Example:
    -     int c = 1, d = 2;
          int f() {
            ++c;
            return 0;
          }

          int main() {
            cout << c - d + f();
          }

      - This can be *either* `1` or `0`, as C++ does not specify what order the terms of an arithmetic expression must be evaluated
- Regardless of the order individual *terms* are evaluated (e.g. f()), most languages use left-to-right associativty when evaluating *mathematical expressions* 
  - `c - d + f()` will always do `(c - d) + f()`, but there is no guarantee of *when* `f()` is evaluated
## Short Circuiting
- Languages that support **short circuiting** will not fully evaluate a boolean expression if its outcome is already known
- Languages will evaluate boolean sub-expressions from left-to-right and skip evaluating the rest of the expression once it finds a condition that satisfies or invalidates the expression  
  - Example:
    -     bool pays_well = true;
          if (pays_well == true || fun == true && interesting == true)
            ...
      - This skips evaluating `fun == true && interesting == true` because the first part of the logical OR satisfies a `true` value
- For an `OR`: short circuits on a left `true`. For an `AND`: short circuits on a left `false`.
## Control Flow
### Unconditional Branching
- `GOTO`: Jumps to a label
  - Example:
    -     if (condition_is_true)
            goto here;
          ...
          here:
            do_other_thing()
- `BREAK`: Terminates the innermost loop and jumps to the statement following it
  - Example:
    -     int main() {
            for (int i = 0; i< 3; ++i) {
              for (int j = 0; j < 10; ++j) {
                if (j == 0)
                  break;
                // This line is skipped when broken out of 
                cout << j << endl;
              }
              // Jumps to here on a break
              cout << i << endl;
            }
          }
  - Some languages allow for breaking out of an *outer loop*:
    - Example: JavaScript
      -     outer_loop:
            for (i = 0; i < 100000; i++) {
                console.log("outer: " + i)
                for (j = 0; j < 10000; j++) {
                  console.log("inner: " + j)
                  if (j == 2) break outer_loop;
                }
            }
- `CONTINUE`: Jumps to the top of the innermost loop and advances to the next iteration
  - Example:
    -     int main() {
            for (int i = 0; i< 3; ++i) {
              for (int j = 0; j < 10; ++j) {
                if (j == 0)
                  continue;
                cout << j << endl;
              }
              cout << i << endl;
            }
          }
- `RETURN`: Exit function
### Conditional Statements
- Beyond just *if-else* statements, some languages offer additional conditional logic
- **Ternary**: `boolean_condition ? A : B` is the same as *if boolean_condition is true return A else return B*
- **Null Coalescing Operator**: `A ?: B` is the same as *if A is not NULL return A else return B*
  - Alternatively, some languages do `??`
  - Example:
    -     fun eat_startup_meal(food: String?) {
            val meal = (food ?: "ramen") + " and redbull"
            println("Time for dinner, let's have a $meal.")
          }

          fun main(args: Array<String>) {
            // Prints: Time for dinner, let's have ramen and redbull.
            eat_startup_meal(null)
            // Prints: Time for dinner, let's have sushi and redbull.
            eat_startup_meal("sushi")
          }
- **Safe Navigation Operator**: `obj?.property?.property` allows for safe access of properties of an object that might be null or undefined without causing a runtime error
  - Example:
    -     function snackTime() {
            var snack = person?.preferences?.snack;
            if (snack != null) console.log("Mmm," + snack + "!!");
            else console.log("Fine I'll have ramen!")
          }

          var alice = {preferences: {snack: "donuts"}};
          // Mmm, donuts!!
          snackTime(alice);

          var bao = {preferences: {drink: "latte"}};
          // Fine, I'll have ramen!
          snackTime(bao);
- **Switch Statements**:
  - Example: C++
    -     int drink
          switch (drinks) 
          {
            // Falls through 1-3
            case 1:
            case 2:
            case 3:
              cout << "I'm chillin\n";
              break;
            case 4:
              cout << "I'm lit!\n";
              cout << "Life is good!\n";
            default:
              cout << "puke!\n";
              break;
          }
  - Languages can differ in handling multi-way selection - Python, for example, allows for switch statements switch have multiple types, akin to *pattern matching*
    - Example:
      -     def greet(x):
              match x:
                case 'person':
                  print('Hi person!')
                case [p1, p2]:
                  print(f'Hi {p1} and {p2}!')
                # Matches dictionary only with a 'name' and 'age' field
                case {'name': n, 'age', a}:
                  print(f"Welcome {n}, you're a {a}")
                case p if 'berg' not in p:
                  print(f"Hello, {p}!")
                case p:
                  printf(f"Go away, {p}!")
### Iteration
#### Iterators
- One way to implement loops is to utilize **iterators**
  - **Iterable objects** are objects that holds, has access to, or can *generate* a sequence of values
    - They can be iterated over to obtain its values
    - These include *container objects* (e.g. arrays, lists, tuples, sets, etc.), *I/O objects* (e.g. can be used to access a disk file or network streams), *generator objects* (e.g. can generate a sequence from a range) 
  - **Iterators** enable the *enumeration of iterable objects* - they essentially allow for a way to access an iterable object's values without exposing its underlying implementation
    - Iterators are typically *separate* from the iterable object because doing so is more *flexible* - we could have multiple iterators pointing to different parts of the same iterable object, for example
    - Typically, to create an iterator, you must "ask" the iterable object to provide one
  - When an iterable object is passed in a language's built-in loops, the language implicitly uses an iterator to move through the items:
    - Example:     
      -     for n in iterable_object:
              ...
            
            // Under the hood:
            val it = iterable_object.iterator()
            while (it.hasNext()) {
              val v = it.next()
              ...
            }
  - Most languages have the following interface for iterators:
    - For containers and external sources:
      - `iter.hasNext()`: Does the iterator refer to a valid value that can be retrieved?
      - `iter.next()`: Get the value pointed to by the iterator and advance the iterator to the next item
    - For abstract sequences:
      - `iter.next()`: Generates and returns the next value in the sequence OR indicate the sequence is over via a return code/exception
- Iterators can be implemented using *traditional classes* 