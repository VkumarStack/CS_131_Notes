# Function Palooza
## Parameter Passing
- Languages can vary in syntax and semantics of how they pass parameters to functions
- **Formal parameters** are the name of the parameters in the *function* definition whereas **arguments** are the actual parameters passed in (whenever we call the function)
- In a language that supports **positional parameters**, the order of the arguments must match the order of the formal parameters
  -     bool sum(float arr[], int n) {
          float sum = 0;
          for (int i = 0; i < n; i++)
            sum += arr[i];
          return sum;
        }

        int main() {
          float arr[3] = {78, 99, 65};
          cout << "The sum is: " << sum(arr, 3);
        }
- In a language that supports **named parameters**, the caller explicitly specifies the *name* of each formal parameter for each argument (thus the function can be called without its arguments needing to match the order of the formal parameters)
  -     def net_worth(assets, debt):
          return assets - debt
        
        net_worth(assets=10000, debt=3500)
        net_worth(debt=4500, assets=19000)
        net_worth(1000, debt=3500)
- Some languages allow a combination of *both* positional parameters and named parameters
- Languages can also allow the specification of *default values* for parameters, which make them *optional*
  - In languages without mandatory *named arguments* (so languages that support *positional arguments*), default parameters *must* be placed at the end of the parameter list, as otherwise there would be ambiguity
    - Example:
      -     // cannot do: double net_worth(double assets, double debt=0, double inheritance=0)  
            double net_worth(double assets, double debt=0) {
              return assets - debt + inheritance;
            } 
  - Languages with mandatory named arguments *do allow* default values to be used for any parameter
    - Example:
      -     func net_worth(assets: Double, debt: Double=0, inheritance: Double)
- Some languages (e.g. Python and Fortran) enable *optional parameters* *without default values* - the function can check if a given argument was present when the function was called and act accordingly
  - Example:
    -     # my_optionals is a dictionary of optional argument
          # names and their values
          def net_worth(assets, debt, **my_optionals):
            total_worth = assets - debt
            if "inheritance" in my_optionals:
              total_worth = total_worth + my_optionals["inheritance"]
            return total_worth
          
          print("Net-worth: ", net_worth(10000, 2000))
          print("Net-worth: ", net_worth(10000, 2000, inheritance=50000))
- A **variadic function** is a function that can take a *variable number of arguments* (that is, a number of arguments that is not known ahead of time)
  - An example of this is Python's print function: `print(1)`, `print(1, "a")`, `print(1, 3.1415, "c")`
  - Languages implement this typically by gathering variadic arguments and putting them in a *container* that is passed into the function for processing
  - Example (Python - The `*` in front of a parameter indicates that it is a variadic, creating a *tuple* for the variadic arguments):
    -     def f(fixed, *args):
            print("First param: ", fixed)
            print("Everything after first arg:")
            for arg in args:
              print(arg)
          
          f(1, "two", "three", 4.0)
## Error Handling
- Consider the various types of errors and results in programs:
  - **Bugs**: A flaw in the program's logic - the only solution is aborting execution and fixing the bug
    - E.g. Out of bounds array accesses, dereferences of a nullptr, divide by zero, illegal casts, unmet pre/post conditions
    - Handled by assertions
  - **Unrecoverable Errors**: Non-bug errors where recovery is impossible, and the program must shut down
    - E.g. Out of memory error, network host not found, disk is full, invalid app configuration
    - Handled by assertions
  - **Recoverable Errors**: Non-bug errors where recovery is possible, and the pgoram may continue executing
    - E.g. File not found (look somewhere else), network service temporarily overloaded, email address was malformed
    - Handled by Error Objects, Result Objects, Optional Objects
  - **Results**: An indication of an outcome or status of an operation
    - Handled by Result Objects and Optional Objects
### Error Objects
- **Error objects** are language-specific objects used to return an *explicit error result* from a function to its caller, independent of any valid return value
- Languages typically implement this via a built-in error class to handle common errors, and enable programmers to derive *custom error classes* to add more specific error conditions
  - Example:
    -     class Error:
            def __init__(self, msg, nested = None):
              self.error_msg = msg
              self.nested_error = nested
          class HTTPError(Error):
            def __init__(self, msg, url):
              super().__init__(msg)
              self.url = url
            def get_url(self):
              return self.url
- In languages using Error objects, functions will return error objects *along with a function's result* (as a separate value)
  - Example (Go):
    -     func circArea(rad float32) (float32, error) {
            if rad >= 0 {
              return math.Pi*rad*rad, nil
            }
            else {
              return 0, errors.New("Negative radius")
            }
          }

          func cost(rad float32, cost_per_sqft float32) (float32, error) {
            area, err := circArea(rad)
            if err != nil { return 0, err }
            return cost_per_sqft * area, nil
          }
- A downside of this approach is that it requires programmers to manually include error objects in function returns and ensure that they are checked by calling functions
### Result Objects
- A **result object** can be used by a function to return a single result that can represent *either* a valid value or a distinct error
  - Example:
    -     def get_stonk_price(symbol):
            r = get_stonk_price("goog")
            if r.is_valid():
              print("Price: ", r.get_val())
            else:
              print(r.get_error_details())
- The result object, if there is an error, will contain the *full Error object*, so they can be used to handle multiple distinct modes of failure
- Example Function (Swift):
  -     func my_div(x: Double, y: Double)
          -> Result<Double, FloatingPointError> {
            if y == 0 { return .failure(.divideByZero)}
            else {return .success(x / y)}
        }

        let result = my_div(x:10, y:10)
        switch result {
          case .success(let number):
            print("Successful division: ", number)
          case .failure(let error)
            print("Failed with error: ", error)
        }
### Optional Objects
- An **optional object** is like a result object, but returns *either* a valid value or some *generic* failure
- Example:
  -     def get_stonk_price(symbol):
          r = get_stonk_price("goog")
          if r.is_valid():
            print("Price: ", r.get_val())
          else:
            # We do not know the details of the error
            print("Some error occurred")
- This should be used when there is a *single mode of failure*
- Example (C++):
  -     std::optional<float> divide(float a, float b) {
          if (b == 0)
            return std::nullopt;
          else
            return std::optional(a/b);
        }
        int main() {
          auto result = divide(10.0, 0);
          if (result) // '*' overloaded to access valid value
            cout << "a/b is equal to " << *result; 
          else
            cout << "Error during division!";
        }
### Assertions / Conditions
- An **assertion** is a statement inserted into a program that verifies assumptions about the program's state that must be tree for correct execution. That is, they verify:
  - **Preconditions**: Something that must be true at the *start of the function* for it to work correctly (e.g. argument `arr` is not a nullptr)
  - **Postconditions**: Something that a function guarantees to be true once it finishes (e.g. for a sort, `arr[i] <= arr[i+1]`)
  - **Invariants**: Conditions that are expected to be true across a function's execution
- If an assertion fails an error is raised
- Example (Precondition Assertions):
  -     def selectionSort(array, size):
          assert array != None, "Invalid array"
          assert size >= 0, "Neg array length"
- Example (Invariant Assertions): In a Stack implementation, the number of used slots plus the number of free slots must be always equal to the Stack's maximum size
  -     class IntStack {
          public:
            IntStack(int max_size) {
              array_ = new int[max_size];
              free_slots_ = max_size_ = max_size;
              used_slots_ = 0;
            }
            void push(int val) {
              assert(used_slots_ + open_slots_ == max_size_);
              array_[used_slots_] = val;
              ++used_slots_;
              --open_slots_;
              assert(used_slots_ + open_slots_ == max_size_);
            }
        }
- Assertions can be useful because they can catch bugs during development (which can be very important for critical software)
  - Assertions can be used when errors that cannot be recovered from are encountered
### Exceptions
- Rather than weave error checking directly into the code, **exception handling** separates the handling of exceptional situations from the core problem-solving logic of the program
- With exception handling, there is a **catcher**, which is a block of code that tries to complete one or more operations that *might* result in an error, and a **handler**, which runs if and only if an error occurs during the tried operations. These errors are raised by a **thrower**, which creates an exception object that is caught by the catcher
  - Example:
    -     void f() {
            try {
              g();
              h(); 
              // If an error is raised by h(), then
              // the rest of the lines in the try block
              // are skipped
              i();
            }
            // Only runs if an error was raised
            catch (Exception &e)
              deal_with_issue(e);
          }

          void h() {
            if (some_operation() == failure)
              // Function exits here
              throw runtime_error("details..");
            
            // These statements are skipped if an error is raised
            op_succeeded_so_do_other_stuff();
            do_even_more_stuff();
            finish_with_more_stuff();
          }
- An **exception** is an object with one or more fields which describes an *exceptional situation*
  - At the minimum, every exception has a way to get a description of the problem (e.g. division by zero) but programmers can also use sublassing to create their own exception classes and encode other relevant information
- Exceptions can be thrown an *arbitrary number of levels* down from the catcher - doing so will automatically terminate every intervening function on its way back to the handler
  - Example:
    -     void h() {
            if (some_op() == failure)
              throw runtime_error("deets");
            
            // Skipped
            do_other_stuff();
          }
          void g() {
            some_intermediate_code();
            h(); // Error raised here
            // Skipped
            some_more_code();
          }
          void f() {
            try {
              cout << "Before \n";
              g();
              // Skipped
              couter << "After \n";
            }
            catch (Exception &e)
              // Ran due to exception
              deal_with_issue(e);
          }
- An exception handler can specify exactly what type of exceptions it handles. The thrown exception will be directed to the closest handler in the call stack that covers its exception type. If there is no compatible handler, the program will terminate (a **panic**)
  - Example:
    -     void h() {
            throw out_of_range("negative index");
          }
          void g() {
            try {
              h(); // Exception generated
            }
            // Not handled by this catch
            catch (invalid_argument &e) {
              deal_with_invalid_argument_err(e);
            }
          }
          void f() {
            try {
              g(); // Exception generated
            } // Not handled by this catch
            catch (overflow_error &e) {
              deal_with_arithmetic_overflow(e);
            } // Handled by this catch
            catch (out_of_range &e) {
              deal_with_out_of_range_error(e);
            }
          }
- Some languages support a third component to a catcher, called a **finally block** that is guaranteed to run whether the *try block* succeeds or throws. If the exception thrown in the try block is never caught, the `finally` block will run *before* propagating the exception up
  - This is useful for *cleanup code*, which must run whether or not an exception happens
  - Example:
    -     public class FileSaver {
            public void saveDataToFile(String filename, String data) {
              FileWriter writer = null;
              try {
                writer = new FileWriter(filename);
                writer.write(data);
              }
              catch {
                e.printStackTrace();
              }
              finally {
                if (writer != null)
                  writer.close();
              }
            }
          }
  - Example:
    -     void f() {
            do_thing0();
            try {
              do_thing1();
              do_thing2();
              do_thing3();
            }
            catch (Exception &e) {
              deal_with_issue1(e);
              // This return does not exit the function
              // It FIRST goes to the finally block and 
              // THEN returns
              return;
            }
            finally {
              // This occurs regardless if an exception is generated
              do_final_thing1();
            }
            // If an exception is generated, this never runs
            // If no exception is generated, then this runs
            do_post_thing1();
          }
- Exception handling can result in various bugs if not used properly:
  - It is hard to tell whether a function will be impacted by exceptions from the functions that it calls
    - Example:
      -     void h() {
              ...
            }
            void g() {
              int* arr = new int[100];
              h();
              // This could never run if h raises an 
              // Exception that is caught later on
              // So there is a memory leak
              delete [] arr;
            }
            void f() {
              try {
                g();
              }
              catch (Exception &e) {
                deal_with_issue(e);
              }
            }
  - One way to deal with these types of issues is to force programmers to *declare* whether a function throws an exception (rather than deal with it internally) - this is done by Java
    - E.g. `void h() throws IOException`
      - If a different function calls `h()`, the compiler *enforces* that it either catches (via a try catch block) potential errors raised by `h()` or throw an error itself
    - A downside of this is that it makes the code much more verbose
- Good practices with exception handlers (in order from most preferred to least):
  - **No-throw guarantee (Failure Transparency)**: A function guarantees that it will not throw an exception - if an exception occurs in or below the function, it will handle it internally and not throw
    - For instance, this is required of destructors, functions that deallocate memory, swapping functions, etc.
  - **Strong exception guarantee**: If a function throws an exception, it guarantees that the program's state will be rolled-back to the state just before the function call
    - E.g. `vec.push_back()` ensures that the vector does not change if the `push_back` fails
  - **Basic exception guarantee**: If a function throws an exception, it leaves the program in a valid state (no resources are leaked, and all invariants are intact) - there is no guarantee of rolling back here
- A benefit of exception handling is that errors will never be ignored if the programmer forgets to add a try/catch - the program would simply crash
    - In contrast, result or optional objects might involve the programmer forgetting to handle for returned errors
- A downside of exception handling, though, is that programmers must be more careful with their exception handlers - especially in freeing up resources in the handlers
### Panics 
- A panic is used to *abort execution* due to an exceptional situation which cannot be recovered from
    - It can be thought of as an exception which is never caught
    - The panic typically contain both an error message as well as a stack trace to provide the programmer context as to why something failed
### Error Handling Practices
- To check for errors that should never occur if the code is correct (e.g. bugs, unmet preconditions, etc.) or to build unit tests that validate individual classes or functions, *assertions* should be used
- When a function needs to return either a value *or* an error for a common, recoverable failure case, either an *optional* (for one possible failure mode) or *result* object should be used (for multiple failure modes)
- When a function is unable to fulfill its "contract" and the error is incredibly rare (and is recoverable), then *exceptions* should be used
- When there is no reasonable way to recover from an error, then *panics* should be used
## First Class functions
- In languages with **first-class functions**, functions can be passed to or returned from other functions, variables can be assigned to functions, functions can be stored in data structures, functions can be compared for equality, and functions can be expressed as anonymous *or* literal values
    - Essentially, functions are *first-class citizens* because they are data objects that can be manipulated like any other data in a program
    - In languages with *second-class functions*, in contrast, functions can be passed as arguments but not returned or assigned to values
    - In languages with *third-class functions*, functions can be called but nothing else
- Example: C++ leverages first-class functions via function pointers, which have a general syntax of `rtype (*)(type1 parm1, type2 parm2, ...)`
    -     int square(int val) { return val * val; }
          int fivex(int val) { return val * 5; }
          // Like a macro to simplify expressing pointer type
          using IntToIntFuncPtr = int (*)(int val);

          // Take in a function
          void apply(IntToIntFuncPtr f, int val) {
            cout << "f(" << val << ") is " << f(val) << endl;
          }

          // Return a function
          IntToIntFuncPtr pickAFunc(int r) {
            if (r == 0) return square;
                else return fivex;
          }

          int main() {
            IntToIntFuncPTr f = pickAFunc(rand() % 2);
            // Comparing functions
            if (f == square) cout << "Picked square\n";
                else cout << "Picked fivex\n";
            apply(f, 10);
          }
### Anonymous (Lambda) Functions
- **Lambda functions** are just like any other function, but they do not have a name
    - Typically, lambda functions are used to define simple helper functions that do not warrant a full function definition
    - Although lambdas are *typically pure*, they can still mutate state
- Example: C++
    -     auto create_lambda_func() {
            int m = 5;
            int b = 3;
            // The free variables to capture must be explicitly
            // specified unlike other languages
            // Parameter type -> Return Type
            return [m, b](int x) -> int { return m*x + b; }
          }

          int main() {
           auto slope_intercept = create_lambda_func();
           cout << "5*100 + 3 is: " << slope_intercept(100); 
          }
    - In C++, closures capture by *value*, so copies of the values (`m` and `b`) are made
        - This is not necessarily the same of all programming languages
- Languages vary in how they capture free variables - some do by value (copy), some do by reference, and others even do by environment
## Polymorphism (Generics and Templates)
- Polymorphism is a language feature that allows a *function*, *class*, or *operator* to operate on different types of values, exhibiting varied behaviors based on the type of its inputs
    - This allows for algorithms to be expressed with minimal assumptions about the data that they operate on, allowing them to be as interoperable as possible (e.g. a generalized linked list that holds any type)
### Polymorphism in Statically Typed Languages
- **Subtype polymorphism**: A function is designed to operate on objects of a base class B (e.g. Shape) and on objects of all subclasses derived from B (e.g. Circles)
    -     class Shape { ... }
          class Square: public Shape { ... }
          class Circle: public Shape { ... }

          void processShape(Shape& s) {...}
          Circle c(10);
          processShape(c);
          Square s(5);
          processShape(s);
- **Ad-hoc polymorphism**: We (the *programmer*) define specialized versions of the same function for each type we want to support - this is also known as *overloading*
    -     bool scarier(Dog a, Dog b) { ... }
          bool scarier(Cat a, Cat b) { ... }
    - In this case, the language defines which version of the function to call based on the *type of arguments*
    - This is not possible in dynamically typed languages since such languages are *duck typed* - we cannot distinguish `def greater(a, b)` and `def greater(a, b)` in Python solely based on the function signature
        - Rather, these languages must utilize *type inspection* inside of the function:
            -     def greater(a, b):
                    if type(a) == type(b) == int:
                        ...
                    if type(a) == type(b) == Cat:
                        ...
- **Parametric polymorphism**: We define a single version of a function or class that can operate on many, potentially unrelated types (not necessarily derived types)
    -     ArrayList<String> nerds = new ArrayList<String>();
          ...
          ArrayList<Dog> doggos = new ArrayList<Dog>();
    - In C++, for instance, this can be achieved via templated classes:
        -     template<typename T>
              class HoldItems {
                public:
                    void add(T val) { arr_[size_++] = val; }
                    T get(int j) { return arr_[j]; }
                private:
                    int size_ = 0;
                    T arr_[10];
              }

              HoldItems<Dog> doggos;
              Dog f("Fido");
              doggos.add(f);
              Dog d = doggos.get(0);

              template<typename T>
              void swap2(T& a, T& b) {
                T temp = a;
                a = b;
                b = temp;
              }

              int a = 10, b = 5;
              swap2<int>(a, b);
    - Parametric polymorphism can be implemented in two ways:
        - **Templates**: In languages that use the *template approach*, each time a template is used with a *different type*, the compiler generates a new concrete version of the template function/class by substituting the type parameter 
            -     template <typename T>
                  // During compilation, this function is duplicated
                  // replacing T with Dog and int respectively in each
                  // version
                  void swap(T &x, T &y) {
                    T temp = x;
                    x = y;
                    y = temp;
                  }

                  // Results in a Dog swap method
                  // generated
                  Dog fido(35), benji(75);
                  swap(fido, benji);

                  // Results in an int swap method
                  // generated
                  int x=42, y=100;
                  swap(x, y);
          - The newly generated function/class is compiled as any other piece of code normally would
          - This implies that any operations used in the templated code must be supported by the types being templated
              -     template <typename T>
                    void takeANap(T &x) { x.sleep(); }

                    class Dog { void sleep() {...}}
                    class Person { void sleep() {...}}

                    // Both classes support a sleep method, 
                    // so the following works
                    Dog puppers;
                    takeANap(puppers); // Compiles!
                    person carey;
                    takeANap(carey); // Compiles

                    // This does not compile because
                    // string does not have a takeANap
                    // method, so when the template is replaced
                    // with a string, it will not compile
                    string val;
                    takeANap(val);
          - Templates still ensure type safety, because the compiler still checks for type safety once the templated function/class is generated
          - Templates also do not sacrifice any runtime efficiency because there is no "checking" being done at runtime since all versions of the functions are compiled - this is the same efficiency as ad-hoc polymorphism
        - **Generics**: In languages that use a *generics approach*, the code inside a generic function/class is required to be type-agnostic (only operations compatible with all possible types are allowed, like comparing object references or assignment)
            - Only *one version of a generic is compiled* - not one for each type because of the guarantee of type agnostic operations
                -     class HoldItems<T> {
                        public void add(T val) { arr_[size_++] = val; }
                        public T get(int j) { return arr_[j]; }
                        // This would fail, because quack() is not generic
                        // public void beADuck(int j) { arr_[j].quack(); }

                        T[] arr_ = new T[10];
                        int size_ = 0;
                    }
            - Once a generic is parameterized, strict type checking is still performed at *compile time* - so there is still a guarantee of type safety
                -     HoldItems<Duck> ducks = new HoldItems<Duck>();
                      // Invalid parameter type
                      ducks.add(new Robot("HAL"));
                      // Invalid return type
                      Robot r = ducks.get(0);
            - Generics can be *bounded*, where there is a restriction on what types can be used with a generic - this is typically done with interfaces
                - This is similar to subtype polymorphism, but it is more general because it can be used for *classes* (whereas subtype polymorphism is usually used for *functions*)
                -     interface DuckLike {
                        public void quack();
                        public void swim();
                      }

                      class HoldItems<T> where T: DuckLike {
                        public void add(T val) { arr_[size_++] = val; }
                        public T get(int j) { return arr_[j]; }
                        // Because of the bounding to DuckLike objects
                        // this is now legal
                        public void beADuck(int j) { arr_[j].quack(); }

                        T[] arr_ = new T[10];
                        int size_ = 0;
                      }

                      HoldItems<Mallard> raft = new HoldItems<Mallard>();
                      raft.add(new Mallard("Willard"));
                      raft.beADuck(0);
      - **Specialization** involves defining a dedicated version of a function or class for a *specific type* so that the specialized version is used instead of the generic/templated version.
          - Example: Specialized sort for bools
              -     template<>
                    void sort(bool items[], int len)
                    {
                      int n_false = 0;
                      for (int i = 0; i < len; ++i) { if (!items[i]) ++n_false; }
                      for (int i = 0; i < n_false; ++i) items[i] = false;
                      for (int i = n_false; i < len; ++i) items[i] = true;
                    }

                    template <typename T>
                    void sort(T items[], int len)
                    {
                      // General code here
                    }

                    int main() {
                      bool bools[] = {true, false, false, true};
                      sort(bools, 4); // Uses a specialized version

                      int ints[] = {17, 22, 3, 33, 4, -10};
                      sort(ints, 6); // Uses generic version of sort
                    }
