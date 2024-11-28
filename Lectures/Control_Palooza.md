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
- Iterators can be implemented using *traditional classes*, where an iterator is an object defined by a class
  - Example: Python
    -     class OurIterator:
            def __init__(self, arr):
              self.arr = arr
              self.pos = 0
            # Dunder method to get the next method of the 
            # iterator. This also advances the iterator.
            # If the iterator hits the end, it must throw 
            # an exception
            def __next__(self):
              if self.pos < len(self.arr):
                val = self.arr[self.pos]
                self.pos += 1
                return val
              else:
                raise StopIteration

          class ListOfStrings:
            def __init__(self):
              self.array = []
            def add(self, val):
              self.array.append(val)
            # Dunder method to make a class iterable - this method 
            # creates an iterator object and returns it
            def __iter__(self):
              it = OurIterator(self.array)
              return it

          nerds = ListOfStrings()
          nerds.add("Carey")
          nerds.add("David")
          nerds.add("Paul")

          for n in nerds:
            print(n)
  - Example: Java
    -     import java.util.Iterator;
          class ListOfStrings implements Iterable<String> {
            private String[] array;
            private int numItems = 0;, maxsSize = 100;

            public ListOfStrings()
              { array = new String[maxSize]; }
            public void add(String val)
              { array[numItems++] = val; }
            @Override public Iterator<String> iterator() {
              Iterator<String> it = new OurIterator();
              return it;
            }

            // Nested Class
            class OurIterator implements Iterator<String> {
              private int iteratorIndex = 0;
              @Override public boolean hasNext()
                { return iteratorIndex < numItems; }
              @Override public String next()
                { return array[iteratorIndex++]; }
            }
          }
- Iterators can also be implemented using *generators* - these are known as **true iterators**
  - Generators are functions that can be *paused* and *resumed* with its state saved between calls. Under the hood, these are implemented using closures
    - Example: Python
      -     def foo(n):
              for i in range(1, n):
                print(f'i is {i}')
                yield
                print('woot!')
            def main():
              # This does not actually call foo(n) since it is a generator
              # Rather, creates a closure
              p = foo(4) 
              print('CS')
              # This calls the generator, which returns until the 'yield'
              next(p)
              print('is')
              next(p)
              print('cool!)
              next(p)

              # Output:
              # CS
              # i is 1
              # is
              # woot!
              # i is 2
              # cool!
              # woot!
              # i is 3
      - In Python, generators can also *return values* on a yield
        -     def bar(a, b):
                while a > b:
                  yield a
                  a -= 1
              
              f = bar(3, 0)
              print('Eat prunes!')
              t = next(f)
              print(t)
              t = next(f)
              print(t)
              t = next(f)
              print(t)
              print(f'Explosive diarrhea!')

              # Output:
              # Eat prunes!
              # 3
              # 2
              # 1
              # Explosive diarrhea!
  - Generators are *iterable objects*, so they can be used in iterable objects in loops
    - When a generator has no more values to yield (it exits without a `yield` call), an exception is raised, and so it is known that there are no more values to iterate over
    - Example:
      -     def our_range(a, b):
              while a > b:
                yield a
                a -= 1
            
            for t in our_range(3, 0):
              print(t)
  - Iterating using a generator versus a list of the same size would be preferred because it is *more compact* - creating a list of all values to iterate over is expensive compared to generating a value one by one
#### First Class Functions
- Another way to support iteration is through *first-class functions*
  - Example: `items.forEach({elem -> println("$elem")})`
- In this approach, a *function* is provided as an argument to a `forEach` method that loops over the iterable's items
  - Example:
    -     class ListOfStrings:
            def __init__(self):
              self.array = []
            def add(self, val):
              self.array.append(val)
            def forEach(self, f):
              for x in self.array:
                f(x)
          
          yummy = ListOfStrings()
          yummy.add('bindi masala')
          yummy.add('koobideh')

          yummy.forEach(lambda food: print(f'I like {food}'))
- In this approach, an iterable object *does not return an iterator* but rather iterates over its own objects and calls the provided function
- A downside to this approach is that it would not be able to support *nested loops*
## Concurrency
- Concurrency is a paradigm in which a program is decomposed into *simultaneously executing tasks*
  - These tasks might run *parallel on multiple cores* or might be *multiplexed on a single core*
  - These tasks might *operate on totally independent data* (each sorting a different array) or might *operate on shared mutable data*
  - These tasks might be *launched deterministically as part of the regular flow* of a program or might be *launched due to an external event occurring* (e.g. a button press)
### Multi-threading Model
- **Multi-threading model**: Multiple "threads" of execution run concurrently within a program, potentially across multiple cores
  - This is best suited for CPU-bound tasks where parallelization across cores can significantly boost performance
  - Example:
    -     void handle_user_purchase(User u, Item i) {
            if (bill_credit_card(u) == SUCCESS) {
              create_thread(schedule_shipping(u, i));
              create_thread(send_confirm_email(u, i));
            }
          }
- **Thread Management**: Threads enable multiple sequences of instructions to run concurrently within a program
  - Example: C++
    -     #include <thread>
          void f(int n) {
            for (int i = 0; i < n; ++i)
              cout << "Hi!";
          } 

          int main() {
            // Creates a new thread that runs function f
            std::thread t(f, 10);
          }
  - **Fork-Join Pattern**: First, fork one or more tasks so they execute concurrently, then wait for those tasks to complete, and then proceed
    - Example:
      -     function task1(param) { ... }
            function task2(param) { ... }
            function task3(param1, param2) { ... }
            function launch_in_parallel() {
              t1 = run_background(task1(42));
              t2 = run_background(task2("suss"));
              t3 = run_background(task3(3.14, 2.71));

              wait_for_all_tasks_to_finish(t1, t2, t3);
              print("All tasks done");
            }
    - This might be done *recursively*, where a data source is forked until it is at a manageable size for a thread to handle
  - Python supports multithreading but when each thread runs it claims *exclusive access to Python's memory (**Global Interpreter Lock**)*, so only *one thread can do computation at a time*
    - This is because Python's garbage collection system was never designed to be thread-safe 
    - Threading can still be useful in Python for operations that *do not use Python's memory* - e.g. downloading a file or make a network request in the background
- **Synchronization**: Synchronization ensures that threads do not interfere with each other when accessing shared resources
  - These include *mutexes*, *semaphores*, *spinlocks*, *barriers*, *conditions*, *read-wirte locks*, etc.
  - Some languages rely on libraries for synchronization whereas others have built-in synchronization primitives
    - E.g. C++'s `volatile` keyword indicates a variable's value may change over time and thus should never be cached
  - Example:
    -     #include <thread>
          #include <mutex>

          int counter = 0;
          std::mutex mtx;

          void increment(int times) {
            for (int i = 0; i < times; i++) {
              mtx.lock();
              counter++;
              mtx.unlock();
            }
          }

          int main() {
            std::thread thread1(increment, 1000);
            std::thread thread2(increment, 1000);
          }
- **Message Passing**: Message passing allows different threads or processes to safely send messages to one another
  - Some languages prefer messages *not be passed* using shared mutable states but rather through a *built-in message queue* to allow safe communication between threads
  - Example: Go
    -     func genPrimes(messages chan int) {
            for i := 2; ; i++ { // Infinite loop
              if isPrime(i) {
                messages <- i // Send message
              }
            }
          }
          func main() {
            // Defines a channel for integers
            messages :- make(chan int)
            go genPrimes(messages) // launch thread

            for {
              prime := <-messages // dequeue next prime
              fmt.Println(prime)
            }
          }
### Asynchronous Programming Model
- A single-threaded loop manages a queue of tasks, executing them *one at a time* as they become ready
  - This is best suited for I/O-bound operations (e.g. file downloads) and event-driven tasks (e.g. UI clicks), allowing for the system to remain responsive while waiting for external events or operations to complete
  - Example:
    -     function process_payment() { ... }
          void setup_event_associations() {
            button = create_new_button("Pay Now!");
            button.set_func(ON_CLICK, process_payment);
          }
- In **asynchronous programming**, execution does not flow from top-to-bottom, but rather a module called a **runtime** maintains a queue of **coroutines** (aka **async functions**) to execute
  - A coroutine is a function that, once run, can be *paused* and *resumed* where left off
  - The runtime repeatedly dequeues the front coroutine and runs/resumes it
  - As the coroutine runs, the runtime can enqueue other coroutines or initiate a background I/O operation (outside the queue)
  - While waiting for results, the coroutine is suspended, allowing for other coroutines to continue to be dequeued and executed
  - Once the results are ready, the suspended coroutine is added back to the queue where it eventually resumes execution
- The asynchronous programming model is useful when there are long-running I/O tasks such as reading from a database or downloading web data
  - This is because the runtime can *suspend a coroutine* while it is waiting for the I/O to complete
  - The memory usage and context switching are typically lightweight relative to multithreading due to implementation optimizations
  - Example: Python
    -     async def cook_pasta():
            print("Cooking pasta...")
            await asyncio.sleep(5)
            print("Pasta is ready!")
            return "Sphagetti"
          
          async def make_sauce():
            print("making sauce...")
            await asyncio.sleep(4)
            print("Sauce is ready!")
            return "Meatsauce"
          
          async def cook_dinner():
            print("Cooking dinner...")

            task1 = asyncio.create_task(cook_pasta())
            task2 = asyncio.create_task(make_sauce())

            pasta = await task1 # Sleep until task1 is done
            sauce = await task2 # SLeep until task2 is done 
            print(f"{pasta} and {sauce} are ready!")
          
          asyncio.run(cook_dinner())
- The async model is based on the *runtime loop*
  - Pseudocode:
    -     def process_queue(main_coroutine):
            queue = new Queue()
            queue.append(main_coroutine)
            while not queue.empty()
              coroutine = queue.dequeue()
              start_or_resume(coroutine)
  - While running, a coroutine can *call other coroutines for immediate execution*, *queue other coroutines for eventual execution*, *initiate background operations and sleep until their results are ready*
    - Calling other coroutines:
      -     async def boil_water():
              print("Boiling water...")
              await asyncio.sleep(3)
              print("Water is boiled!")
            
            async def cook_pasta():
              print("Starting...")
              # This acts like a regular function call.
              # Meaning the function is called immediately
              # without involving the queue
              await boil_water()
              print("Cooking pasta...")
              await asyncio.sleep(5)
              print("Pasta is ready!")
    - Queuing other coroutines:
      -     async def cook_dinner():
              print("Cooking dinner...")
              ...
              # These are not immediately executed
              # but are rather added to the end of 
              # the queue
              asyncio.create_task(clean())  
              asyncio.create_task(dry())

              print("Done cooking")
    - Initiating background operations and sleeping
      - Note that background operations are *independent* from the tasks on the queue (file opening is done by the operating system, not Python)
      -     from aiofiles import open
            async def load_recipe(file):
              print(f"Reading recipe...")
              # Launches the operation in the background and awaits its result
              # The load_recipe coroutine, thus, sleeps until the background
              # I/O is done. Once it is done, load_recipe is added back to the 
              # queue
              f = await open(file, 'r')
              try:
                # This does the same thing
                recipe = await f.read()
              finally:
                # This also does the same thing
                await f.close()
              return recipe
- Example:
  -     import asyncio
        
        async def heat_oven():
          print("Heaing the oven!")
        
        async def prepare_ingredients():
          print("Preparing ingredients...")
          await asyncio.sleep(3)
          print("Ingredients ready!")
        
        async def main():
          print("Starting dinner prep...")
          asyncio.create_task(heat_oven())
          await prepare_ingredients()
          print("Dinner prep is done!")

        asyncio.run(main())

        # Outputs:
        # Starting dinner prep...
        # Preparing ingredients...
        # Heating the oven!
        # Ingredients ready!
        # Dinner prep is done!
  - When `await prepare_ingredients()` is called, the sleep in the method (which is considered an `I/O`) task pauses the execution of that routine (which is the `main` routine because it is immediately calling prepare_ingredients)
  - This means that the `heat_oven()` routine is queued right after, and once it completes and the sleep finishes, the `main` coroutine continues off from the call from `prepare_ingredients`