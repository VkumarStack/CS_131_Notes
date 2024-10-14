# Functional Programming and Haskell
## Functional Programming
- In **functional programming**:
  - All functions must take at least one argument and return a value
  - Functions are just like any other data - meaning they can be *stored in variables* and *passed as arguments*
    - Example:
      -     f(x) = x + 5
            y = f
            z = g(f) # This is another function
  - All variables are *immutable* and therefore can be modified after initialization
  - All functions are *pure*, meaning that calling f(x) with a *given x* will always return the same value *y*
    - This implies that functions may not use or modify external *mutable* state or variables
    - Formal definition of a **Pure Function** (aka **Referentially Transparent Function**):
      - Given a specific input, the function *always returns the same output y*
      - The output is computed *exclusively* based on its input parameters, without relying on or modifying external data that might change call to call (*not constants*, which do not change call from call) - no **side effects**
      - Example:
        -     # Pure
              int f(int p) {
                int q = 5*p*p;
                return q;
              }

              # Impure
              int z;
              int f(int p) {
                return p*z++;
              }
## Imperative versus Functional Programming
- Imperative programming is algorithmic - there are statements and variable changes
  - Functional programming instead relies on transformations through function calls
- Imperative programming relies heavily on change on variable state
  - Functional programming does not allow for mutability, so no changes are allowed
- Imperative programming relies on sequencies of statements, loops, and function calls
  - Functional programming relies on recursion - there are no loops
- Imperative programming relies more effort to make multi-threading to work
  - Functional programming allows for easy multi-threading due to the pure property of functions
- Imperative programming involves correctness from the order of code execution
  - Functional programming can allow for correct programs regardless of the order of execution of functions (due to there being no side effects)
  - This can allow for *lazy evaluation*, where languages (such as Haskell), will not execute functions *until those functions are actually needed* - this means that some computations are deferred until their results are explicitly needed

## Haskell
- Example #1:
  - Haskell Program:
    -     poly :: Double -> Double
          poly x = 3 * x^2
  - C++ Equivalent:
    -     double poly(double x) {
            return 3 * x*x;
          }
  - Function *type signatures* are specified first (`Double -> Double`)
    - The *last type* refers to the return type, and the other types refer to the input types
  - Function bodies are the expressions following an *equal sign*
  - Calling a function simply involves specifying the function name followed by a space and then its parameters (if there are multiple, they are separated by spaces)
- Example #2:
  - Haskell Program:
    -     is_greater :: Int -> Int -> Bool
          is_greater first second = 
            first > second
  - C++ Equivalent:
    -     bool is_greater(int first, int second) {
            return first > second;
          }
- Example #3:
  - This is a valid Haskell function:
    -     is_old age has_aches = 
            (age > (30::Int)) || (has_aches == True)
  - Haskell is capable of *inferring* the parameter and return types, so the function signature is actually *optional*
    - `:t is_old` in GHCI will output `is_old :: Int -> Bool -> Bool`
    - Since *age* was compared to an Int, it was inferred to be an Int
    - Since *has_aches* was compared to a Bool, it was inferred to be a Bool
    - The final result can be inferred from the rest
  - Although Haskell allows for type information to be omitted, it is still *strictly typed*
    - E.g. An error will be raised if a Float is passed into a function expecting an Int (it will not implictly cast)
- Example #4:
  - This is a valid Haskell function, computing $3x^2$:
    -     poly :: Double -> Double
          poly x = (*) 3 x^2
    - Haskell supports *prefix notation*, meaning that any operator with parentheses wrapped around them can support prefix computation
      - E.g. `6 - 5` can also be expressed as `(-) 6 5`
- Example #5:
  -     f :: Int -> Int
        f x = x^2

        g :: Int -> Int
        g x = 3*x

  - Calling `f g 2` throws an error because Haskell evaluates functions *left to right*, so this is interpreted as `(f g) 2`, which results in a type error since *f* expects an Int not a function - the intended way should have been `f (g 2)`
  - Calling `f 5 * 10` is evaluated as `(f 5) * 10` because Haskell always calls *functions* before evaluating operators

  - Example:
    -   f :: Double -> Double -> Doub;e  
        f x y = x * y
        g :: Double -> Double
        g a = f a (sqrt (a + 1))
- Example #6:
  -     bruin_discount :: Int -> Int
        bruin_discount price = 
          if price > 100
          then price - 20
          else price - 10
  - In functional programming, `if` is not a *statement* but rather an *expression*, so it is *required to have an else clause* as every expression must result in a value
- Example #7:
  -     evaluateExam :: Int -> String -> String
        evaluateExam score prof
          | score < 50 && prof == "Eggert" =
            "Given the curve, you got a B+."
          | score < 50 =
            "You got an F."
          | score == 10 = 
            impress prof
          | otherwise =
            "You passed."

        impress :: String -> String
        impress prof = prof ++ " is impressed!"
  - These are **guards** in Haskell, which act as a compact syntax for *nested if-else statements*
    - The format is:
      -     |condition1 = action1
            |condition2 = action2
            ...
            |otherwise = action
    - Guards are evaluated from *top to bottom*, so the first one that matches is evaluated and the rest are not ran
    - If using guards, there is *no equal sign after the function signature* - rather, the equal sign is after *each guard condition* (view the equal sign as a return statement)
    - Example: Factorial
      -     fact :: Int -> Int
            fact n
            | n == 0 = 1
            | otherwise = n * fact (n - 1)
- Example #8: Local Bindings:
  -     get_nerd_status gpa study_hrs =
          let 
            gpa_part = 1 / (4.01 - gpa)
            study_part = study_hrs * 10
            nerd_score = gpa_part + study_part
          in 
            if nerd_score > 100 then
              "You are super nerdy!"
            else "You're a nerd poser."
  - The `let` construct allows for *bindings* to be created, which are then accessible in the indented block inside of the `in` keyword
- Example #9: Where Construct:
  -     get_nerd_status gpa study_hrs =
          if nerd_score > 100
            then "You are super nerdy!"
            else "You're a nerd poser."
          where
            gpa_part = 1 / (4.01 - gpa)
            study_part = study_hrs * 10;
            nerd_score = gpa_part + study_part
  - The `where` construct is similar to the let, though it can be placed at the *end of the function* rather than at the beginning
  - `where` is useful in instances when defining a variable for use across *multiple expressions*:
    - Example:
      -     evaluatePerformance :: Int -> String
            evaluatePerformance score
              | score >= excellentThreshold =
                "Excellent"
              | score >= goodThreshold =
                "Good"
              | otherwise =
                "Needs improvement"
            where
              excellentThreshold = 90
              goodThreshold = 75
    - This can *only be done with guards* using a `where` expression - it is not possible with `let`
- Bindings can be used to define *nested functions*
  -     whats_the_behavior_of name = 
          if name == "Carey"
            then behaves_like name "twelve year old"
            else behaves_like name "grown up"
          where
            behaves_like n what =
              n ++ " behaves like a " ++ what ++ "!"
    - This nested function has visibility of *all enclosing function bindings*, so this function could be rewritten
      -     whats_the_behavior_of name = 
            if name == "Carey"
              then behaves_like "twelve year old"
              else behaves_like "grown up"
            where
              behaves_like what =
                name ++ " behaves like a " ++ what ++ "!"
### Tuples
- **Tuples** allow for related data (of possibly varying types) into a single value - they can be used for *simple, temporary groupings* (e.g. to return multiple values from a function)
  - `school_and_rank  "(UCLA", 1)`
  - There are *built-in* functions to extract the first and second elements from two-tuples, `fst` and `snd` respectively
- Example: Function halves the value or negative halves it:
  -     halveOrNegate :: (Double, String) -> Double
        halveOrNegate t =
          if snd t == "neg"
          then fst t * (-1.0)
          else fst t / 2.0
- Example: Function that performs a division and returns if it was safe or not
  -     safeDivide :: Int -> Int -> (Bool, Int)
        safeDivide num denom
          | denom /= 0 = (True, quotient)
          | otherwise = (False, 0)
        where
          quotient = num `div` denom
    - In this example, since Haskell is lazy, it will never actually perform the unsafe division because `quotient` is only needed when denom is non-zero
    - Not-equal is denoted as `/=`
    - Integer division can be performed using the `div` function
    - A named function can be made infix by surrounding it with backticks - e.g. \`div\`
### Lists
- Haskell lists can hold *zero or more items* of the *same type* (*cannot be of different types*)
- Example:
  -     primes :: [Int]
        primes = [2, 3, 5, 7, 11, 13]

        jobs = ["SWE", "Chef", "Writer"]

        lol :: [[int]]
        lol = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]

        lot :: [(String, Int)]
        lot = [("foo", 1), ("bar", 2), ("boo", 3)]

        mt = []
- Functions:
  - Example: 
    - `primes = [2, 3, 5, 7, 11, 13]`
    - `jobs = ["SWE", "Chef", "Writer"]`
  - `head` returns the first element of the list
    - `head primes` -> `2`
  - `tail` returns the list *except the first element*
    - `tail primes` -> `[3, 5, 7, 11, 13]`
  - `null` returns whether or not the list is empty
    - `null []` -> `True`
  - `length` returns the length of the list
    - `length primes` -> `6`
  - `take n` returns the first `n` items of the list (in a copy)
    - `take 3 primes` -> `[2, 3, 5]`
  - `drop n` returns the lsit with the first `n` items dropped (in a copy)
    - `drop 4 primes` -> `[11, 13]`
  - `elem item` returns whether `item` is an element of the list
    - `elem "Chef" jobs` -> `True`
  - `sum` returns the sum of the items in a list
    - `sum primes` -> `41`
  - `or` takes the logical or of all booleans in a list (defaulting to False for empty lists)
    - `or [True, False, False]` -> `True`
  - `and` takes the logical and of all booleans in a list (defaulting to True for empty lists)
  - `zip l1 l2` returns a two-tuple of each element from each list, truncating if necessary
    - `zip [10, 20, 30] ["A", "B", "C", "D"]` -> `[(10, "A"), (20, "B"), (30, "C")]`
  - `++` concatenates two lists *of the same type* and returns a new list
    - `["stalking", "llamas"] ++ ["in", "pajamas"]` -> `["stalking", "llamas", "in", "pajamas"]`
  - `:` prepends a *single element* to a list and returns a new list
    - `"stealthily" : ["stalking", "llamas"]` -> `["stealthily" "stalking", "llamas"]`
    - The `:` operator is *right associative*, so `"barking" : "dogs" : []` -> `["barking", "dogs"]`
- New lists can be constructed via *ranges*
  - `one_to_ten = [1..10]`
    - This is [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  - `oddities = [1, 3..10]`
    - Define the first two elements and an upper bound, and this will create a list with spacing between the first two elements up until the upper bound
    - This is [1, 3, 5, 7, 9]
  - `whole_lotta_numbers = [42..]`
    - This is an *infinite list*, but since Haskell is lazily evaluated, it will not attempt to evaluate this list until needed
    - You can do `take 5 whole_lotta_numbers`, for example, to get `[42, 43, 44, 45, 46]`
  - `tricycle = cycle [1, 3, 5]`
    - This is an infinite list, cycling `[1, 3, 5, 1, 3, 5, 1, 3, 5]` in this case
- Strings are implemented using Lists of Chars under the hood, so all operations that work on lists also work on Strings 
  - Strings are denoted by double quotations, `""` whereas characters are denoted by single quotations `''`
- Example #2: Count the number items in a list and return the product of the list
  -     count :: [Double] -> Int
        count   lst 
          | null lst = 0
          | otherwise = 1 + count (tail list)
  -     prod :: [Double] -> Double
        prod    lst
          | null lst = 1
          | otherwise = head * prod (tail lst)
- Example: Given a list, return a list where each corresponding item is squared
  -     sqrt_it lst
          | lst == [] = []
          | otherwise = first_sqr : (sqr_it rest)
        where
          first_sqr = (head lst) ^ 2
          rest = tail lst
- Example: Reverse a list
  -     rev lst
          | lst == [] = []
          | otherwise = (rev rest) ++ [first]
        where
          first = head lst
          rest = tail lst
- Example: Smallest item in a list
  -     sm0lest lst
          | lst == [] error "empty list"
          | length lst == 1 = first
          | otherwise = min first (sm0lest rest)
        where
          first = head lst
          rest = tail lst
### List Comprehensions
- A list comprehension is a construct that allows for a new list to be created based on one or more existing lists, requiring:
  - One or more input lists to be drawn from (generators)
  - A set of filters on the input lists (guards)
  - A transformation applied to the inputs before items are added to the output list
  - Pseudocode:
    -     process(input_list):
            out = []
            for each x in input_list:
              if guard(x) == True:
                z = f(x)
                out.append(z)
            return out
  - Haskell Syntax:
    - `output_list = [(f x) | x <- input_list, (guard x)]`
      - The guard is optional (perform the function on every single item in the input list)
      - There can be *multiple guards*, but in this case *all guards must pass* 
- Example: Square numbers
  -     input_list = [1..100]
        square_nums1 = [x^2 | x <- input_list]
        square_nums2 = [x^2 | x <- input_list, x > 5]
        square_nums3 = [x^2 | x <- input_list, x > 5, x < 20]
- For multiple input lists, the pseudocode is as follows:
  -     process(input_list1, input_list2):
          out = []
          for x in input_list1:
            for y in input_list2:
              if guard(x) == True && guard(y) == True then
                z = f(x, y)
                out.append(z)
          return out
  - Haskell:
    - `output_list = [(f x y) | x <- input_list1, y <- input_list2, (guard1 x), (guard2 y)]`
  - Example:
    - `all_products3 = [x*y | x <- list1, y <- list2, even x, odd y, x * y < 15]`
- Example: Find the first five numbers from 1000 onward that is divisible by 29
  - `div_by_29 = take 5 [x | x <- [1000..], (mod x 29) == 0]`
- Example: Generate right triangles:
  - `tuples = [(a, b, c) | a <- [1..10], b <- [a..10], c <- [b..10], a^2 + b^2 == c^2]`
    - Here, there are *dependent generators* (`b` uses `a`, `c` uses `b`)
- Example: Quicksort
  -     qsort lst
          | lst == [] = []
          | otherwise = (qsort less_eq) ++ [pivot] ++ (qsort greater)
        where 
          pivot = head lst
          rest_lst = tail lst
          less_eq = [a | a <- rest_lst, a <= pivot]
          greater_eq = [a | a <- rest_lst, a > pivot]
### Pattern Matching
- Pattern matching is syntactic sugar that simplifies writing functions for processing tuples and lists
  - *Multiple versions* of the same function can be defined (each with the same number and types of arguments)
- Example:
  -     course_critic :: String -> String -> String
        course_critic "Carey" "CS131" =
          "Get ready for pop-tarts and Haskell"
        course_critic "Eggert" course =
          course ++ " is gonna be difficult"
        course_critic prof "CS131" =
          "I hope you like coding in 20 languages!"
        course_critic prof course = 
          course ++ " with " ++ prof ++ " is fun!"
    - The first version is only ran if the first two arguments are "Carey" and "CS131"
    - The second version is ran if the first argument is "Eggert"; the second argument can be any string
    - The third version is ran if the second argument is "CS131"; the first argument can be any string
    - The last version is ran if the first three patterns do not match
    - If multiple patterns match, the topmost one is matched\
- Example: Factorial
  -     factorial 0 = 1
        factorial n = n * factorial(n - 1)
- Example: Length
  -     list_len :: [a] -> Int
        list_len [] = 0
        list_len lst = 1 + list_len (tail lst)
- Example: Exponentiation
  -     exp :: (Int, Int) -> Int
        exp (base, 0) = 1
        exp (base, exponent) = base ^ exponent
    - *Tuples* can also be pattern matched, as shown
- Lists can be pattern matched using parentheses:
  - Example:
    -     get_first_item (first:rest) = 
            "The first item is " ++ (show first)
    -     get_rest_items (first:rest) = 
            "The last n-1 items are " ++ (show rest)
    -     get_second_item (first:second:rest) = 
            "The second item is " ++ (show second)
  - Example:
    -     favorites :: [String] -> String
          favorites [] = "You have no favorites"
          favorites (x:[]) = "Your favorite is " ++ x
          favorites (x:y:[]) = "You have two favorites: " ++ x ++ " and " ++ y
          favorites ("chocolate":xs) = "You have many favorites, but chocolate is #1"
          favorites (x:y:_) = "You have at least three favorites!"
      - Order matters: For example, the fourth function will only be called for lists with at least three elements
### Type Variables
- Example: Function returns the last value in a list of *any type*
  -     get_last_item :: [t] -> t
        get_last_item lst = 
          head (reverse lst)
  - Here, *t* is a *type variable* - which is the equivalent of a *generic type*; it allows for any type to be passed in to the function
    - In Haskell, type variables *must be lowercase* since actual types start with an uppercase
  - A function may have more than one type variable if necessary (e.g. `t1` and `t2`)
- Example: Consider the built-in `max` function which returns the larger of its two arguments
  - `max 10 5` -> `10`
  - `max "cs" "math"` -> `math`
  - Inspecting the type yields: `:t max` -> `max :: Ord a => a -> a -> a`
  - The `Ord a` is a type class that indicates that type `a` can only be used with values that are orderable  
### First Class and Higher-Order Functions
- In functional languages, it is possible to treat functions like any other values (**first-class functions**):
  - Functions can be stored in variables
  - Functions can be passed as arguments to other functions
  - Functions can be returned as values by functions
  - Functions can be stored in data structures
- **Higher-order functions** are functions that either accept another function as an argument or return another function
  - Example:
    -     insult :: String -> String
          insult name = name ++ " is so cringe!"

          praise :: String -> String
          praise name = name ++ " is dank!"
    -     talk_to :: String -> (String -> String) -> String
          talk_to name talk_func
            | name == "Carey" = "No comment."
            | otherwise = (talk_func name)
    - Usage: `talk_to "Devan" praise` -> `Devan is dank!`
    - Usage: `talk_to "Brendan" insult` -> `Brendan is so cringe!`
  - Example:
    -     get_pickup_func :: Int -> (String -> String)
          get_pickup_func born 
            | born >= 1997 && born <= 2012 = pickup_genz
            | otherwise = pickup_other
            where 
              pickup_genz name = name ++ ", you've got steez!"
              pickup_other name = name ++ ", you've got style!"
    - Usage:
      -     pickup_fn = get_pickup_func 2003 
            pickup_fn "Jayathi"
        - One-line equivalent: `get_pickup_func 2003 "Jayathi"`
          - First`get_pickup_func 2003` is evaluated to return a pickup function, and then the returned function is evaluated on input "Jayathi" 
      - Output: `"Jayathi, you've got steez!"`
- Many functional programming languages define a key set of higher-order utility functions to process lists:
  - **mappers** are functions that perform a one-to-one transformation from one list of values to another list of values using a *transformation function*
    - `map f l` calls the function `f` on each value in `l` to produce an output list
    - The type signature of `map` is `(a -> b) -> [a] -> [b]`
    - Example:
      -     cube :: Double -> Double
            cube x = x^3

            is_even :: Int -> Bool
            is_even x = x `mod` 2 == 0
      - Usage:
        - `map cube [2, 4, 10]` -> `[8, 64, 1000]`
        - `map is_even [1, 2, 3, 4, 6]` -> `[False, True, False, True, True]`
    - Map implementation:
      -     map :: (a -> b) -> [a] -> [b]
            map func [] = []
            map func (x:xs) = (func x) : map func xs
  - **filters** are functions that filter out items from one list of values using a *predicate function* to produce another list of values
    - `filter p l` returns a list containing the elements in `l` which, when inputted to `p`, cause it return True
    - Example:
      -     keep_if_even :: Int -> Bool
            keep_if_even val = val `mod` 2 == 0
      - Usage:
        - `filter keep_if_even [1..10]` -> `[2, 4, 6, 8, 10]`
    - Filter implementation:
      -     filter :: (a -> Bool) -> [a] -> [a]
            filter predicate [] = []
            filter predicate (x:xs) 
              | (predicate x) = x : (filter predicate xs)
              | otherwise = filter predicate xs
  - **reducers** are functions that operate on a list of values and collapses them into a single value
    - Reducers take three inputs: a list of items to operate on, an initial accumulator value, and a function that takes the current accumulator value and a list element x and returns an updated accumulator value
      - The reducer goes through each item in the list, passes the current item and current accumulator into the function to get an updated accumulator value
      - The final accumulator value is returned as a result
    - Haskell has two types of reducers: `foldl` and `foldr`
      - `foldl` pseudocode:
        -     foldl(f, initial_accum, lst):
                accum = initial_accum
                for each x in lst:
                  accum = f(accum, x)
    - `foldl` implementation:
      -     (b -> a -> b) -> b -> [a] -> b
            foldl f accum [] accum
            foldl f accum (x:xs) = 
              foldl f new_accum xs
            where 
              new_accum = (f accum x) 
    - Example:
      -     adder acc x = acc + x
            foldl adder 0 [7, -4, 2]
      - This evaluates like: `((0 + 7) + (-4)) + 2`
### Lambda Functions
- A **lambda function** is like any other function, but it does not have a *function name* 
  - Example:
    -     cube x = x^3
          \x -> x^3
  - Lambda functions are used in higher order functions when we do not want to bother defining a whole new named function - typically in the case of simple function
    - Example:
      -     squarer lst = map (\x -> x^2) lst
  - Syntax:
    - `\param1 ... param2 -> expression`
  - Example:
    - `(\x y -> x^3 + y^2) 10 3` -> `1009`
    - `map (\x -> 1/x) [3..5]` -> `[0.333333333, 0.25, 0.2]`