# Logic Palooza
- **Logic programming** is a paradigm where a program is expressed as a set of *facts* (relationships held to be true) and a set of *rules* (e.g. if A is true, then B is true). A program can issue *queries* against these facts and rules.
  - Example: 
    - Fact: Martha is Andrea's parent. Andrea is Carey's parent.
    - Rule: If X is the parent of Q, and Q is the parent of Y, then X is the grandparent of Y.
    - Query: Is Martha the grandparent of Carey? `True`.
- Logic programming is *declarative* - programs specify *what* they want to compute rather than *how*
## Prolog
- When given a query, Prolog tries to find a *chain of connections* between the query and the specified facts and rules that leads to an answer
- Every Prolog program is comprised of *facts* about the world and a bunch of *rules* to discover new facts. Lowercase arguments are called *atoms*, which can represent anything. Both functors and atoms *must be lowercase* (variables are *upercase*)
  -     % Facts. The 'function'-like syntax are known as 
        % functors. They are not actually function calls
        outgoing(ren). % ren is outgoing
        silly(ren). % ren is silly
        parent(alice, bob). % alice is bob's parent
        parent(bob, carol). % bob is carol's parent
        age(ren, 80). % ren's age is 80

        % Facts can be nested
        own(carey, car(2021, blue, subaru, forrester)).
        teaches(carey, course(cs, 131)).
- Prolog *rules* define a new fact in terms of one or more existing *facts* or *rules*. Rules have a *head*, which defines what the rule is trying to determine, and a *body*, which specifies the conditions that allow us to conclude the head is true. Rules are defined in terms of variables as well as atoms and numbers. Variables must start with an *uppercase* number. These variables are *placeholders* htat Prolog tries to fill in to answer user queries
  - Commas in the body are equivalent to a logical `AND`
  -     % Rules
        % P is a comedian if P is silly AND P is outgoing
        comedian(P) :- silly(P), outgoing(P).
        
        % X is the grandparent of Y if there is some Q such that
        % X is the parent of Q and Q is the parent of some Y
        grandparent(X, Y) :- parent(X, Q), parent(Q, Y).

        % C is an old_comedian if C is a comedian, C has an age
        % A, and this age A is greater than 60
        old_comedian(C) :- comedian(C), age(C, A), A > 60.
- Prolog rules can be *recursive* and have multiple parts. Having multiple parts acts a logical OR. Prolog matches *rules and facts* from top-to-bottom, so the base case should be included at the *top* of the definition.
  -     % X is the ancestor of Z if X is Z's parent
        ancestor(X, Z) :- parent(X, Z).
        % OR if X is Y's parent and Y is the ancestor of Z
        ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).
- A *predicate* is used to describe a set of related facts and/or rules that have the same number of arguments
  -     % Parent predicate:
        parent(alice, bob).
        parent(bob, carol).

        % Ancestor predicate:
        ancestor(X, Z) :- parent(X, Z).
        ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).
- Prolog operates according to the **Closed World Assumption**, meaning that only things that can be *proven to be true* are true. Everything that *cannot be proven to be true* is false.
- Prolog rules can use *negation*. Prolog first tries to *prove* whatever is inside the negation statement using all of the program's facts and rules. If it cannot be proven as true, then the negation returns as true.
  -     outgoing(ren).
        silly(ren).
        parent(alice, bob).
        parent(bob, carol).
        age(ren, 80).

        serious(X) :- not(silly(X)).

        % Doing serious(alice) would return true
        % because alice cannot be proven as 
        % silly and therefore she is serious
- After defining facts and rules, users can compile the program and issue *queries*
  - Queries asking for True/False can be made:
    -     ?- outgoing(alice)
          true
  - Queries can be used to fill-in-the-blanks
    -     ?- parent(alice, Who)
          Who = bob
          Who = brenda
      - This will find all matches for Who where alice is a parent of Who
    -     ?- grandparent(A, B)
          A = alice, B = caitlin
          A = brenda, B = ned
### Resolution
- The process of coming up with the answer(s) to a query is called **resolution**
- Prolog tries to match a given query with each fact and rule, from *top to bottom*
  -     parent(ted, bill).
        parent(ann, bri).
        parent(bri, cas). % Matches here
  - `?- parent(bri, cas)` will go through *every single* `parent` functor to find a match
- If a query includes a variable, then prolog treats it as a wildlife during matching. If there is a match, Prolog establishes an association between the Variable and its corresponding value.
    -     parent(ted, bill).
          parent(ann, bri). % Matches here, X -> bri
          parent(bri, cas).
    - `?- parent(ann, X)`
- If a query matches a *rule*, Prolog performs the matching process with the rule's subgoals. In doing this, it *replaces* variables with the mappings discovered so far. Once a query and all subgoals have been matched, then Prolog outputs an answer. Prolog enumerates *every match*, not just the first one found - backtracking if running into a dead end.
  -     attend(ann, usc).
        attend(bri, ucla).
        is_smart(Pers) :- attend(Pers, ucla).
  - `?- is_smart(bri)`
    - This maps `Pers` to `bri`, and now tries to prove that `Pers <=> bri` attends ucla
- Example:
  -     parent(ted, bill).
        parent(ann, bob).
        parent(ann, bri).
        parent(bri, cas).
        parent(bob, sam).
        grand_parent(X, Y) :- 
          parent(X, Q), parent(Q, Y).
  - `?- grand_parent(ann, sam)`
      - This first tries to match `grand_parent(ann, sam)`, matching the rule `grand_parent(X, Y)`
        - Mappings: `ann <=> X`, `sam <=> Y`
      - Then, tries to prove the subgoals
      - The first subgoal (left to right) is `parent(X, Q) <=> parent(ann, Q)`
        - The first one matching is `parent(ann, bob)`, so now the mapping is `Q <=> bob`
      - Using this mapping, the second subgoal is now attempted to be matched, to prove `parent(bob, sam)`
        - This is matched with `parent(bob, sam)`. 
      - Now that all subgoals have been proven (there are none left), then the result is `true`      
  - `?- grand_parent(ann, W)`
    - This matches the rule `grand_parent(X, Y)`, extracting mappings `ann <=> X`, `Y <=> W`
    - This now tries to prove the subgoals, with the first `parent(X, Q) <=> parent(ann, Q)`
      - The first one matching is `parent(ann, bob)`, so `Q <=> bob`
    - This now tries to match the next subgoal `parent(Q, Y) <=> parent(bob, Y)`. This matches with `parent(bob, sam)`, so `Y <=> sam`
      - Since there are no more pending subgoals, so `W <=> Y <=> sam` 
    - This *outputs* `W <=> sam`, but now it backtracks to find *more* matches
    - From `parent(Q, Y) <=> parent(bob, Y)`, continuing *after* `parent(bob, sam)`. Nothing matches here, though, so it backtracks to proving `parent(X, Q) <=> parent(ann, Q)`, continuing *after* `parent(ann, bob)`. This matches `parent(ann, bri)` and now tries to prove the second subgoal `parent(Q, Y) <=> parent(bri, Y)`. This matches `parent(bri, cas)`.
      - There are no more pending subgoals, `W <=> Y <=> cas`, so this *outputs* `W <=> cas`
    - Prolog continues to backtrack (from the second subgoal), but nothing else matches after fully backtracking.
- Resolution Pseudocode:
  -     def resolution(database, goals, cur_mappings):
          if there are no goals left:
            tell the user we found a solution and output our discovered mappings
            return
          for each fact_or_rule in the database:
            succes, new_mappings = unify(goals.top(), fact_or_rule, cur_mappings)
            if success:
              tmp_mappings = curr_mappings + new_mappings
              tmp_goals = sub_goals(fact_or_rule) + goals.all_but_top()
              resolution(database, tmp_goals, tmp_mappings) # recursion
          # if we get here, backtrack
  - When a query is called, there are no initial mappings - e.g. `resolution(database, ["gparent(ann, cas)")], {})`
### Unification
- During resolution, Prolog repeatedly compares the *current goal* with each fact/rule from top-to-bottom to see if they are a match. If there is a match, Prolog extracts mappings between variables and atoms. The process of comparing a goal and extracting mappings is known as **unification**. During resolution, *many unifications* might be done.
  -     def unify(goal, fact_or_rule, existing_mappings):
          if the goal with the existing mappings match the current fact/rule:
            mappings = extract variable mappings between goal and fact/rule
            return (True, mappings) # Unified, return discovered mappings
          otherwise
            return (False, {}) # Could not unify, so no mappings found
- Apply all current mappings to a goal and treat both the mapped goal and the head of the fact/rule as trees
  - Compare each node of the goal tree with the corresponding node in the fact/rule tree
    - If both nodes are fuctors, make sure the functors are the same and have the same number of children (**arity**)
    - If both nodes hold atoms, make sure the atoms are the same
    - If a goal node holds an unmapped variable, it will match ANY item in the corresponding node of the fact/rule
    - If a fact or rule node holds an unmapped variable, it will match ANY item in the corresponding node of the goal
  - Once it is found that the goal matches, the mappings can be extracted by iterating through each pairs of nodes in both trees, and creating a mapping between an unmapped variable in either tree that maps to an atom/number in the other tree
    - If there is an unampped variable that maps to an unmapped variable in the other tree, then create a bidirectional mapping between the variables
### Misc
- In Prolog, it is important to order subgoals properly as to avoid infinite recursion. It is good practice to keep recursive calls at the *right* and *to the bottom*. 
  -     ancestor(X, Z) :- parent(X, Z).
        % Results in infinite recursion because it keeps trying to do ancestor(X, Y)
        % forever whenever the first one does not match
        % ancestor(X, Z) :- ancestor(X, Y), parent(Y, Z).

        % Fix:
        % Aborts after parent fails
        ancestor(X, Z) :- parent(Y, Z), ancestor(X, Y).
### Lists
- Lists in Prolog are just like lists in Haskell or Python, They can contain *numbers*, *atoms*, or *other lists*. Since Prolog is dynamically typed, the items of the list do not need to be of the same type
- Prolog uses a combination of *pattern matching* and *unification* to process lists
  - List processing is done with *facts* and *rules*
-     is_head_item(X, [X | XS]).
  - `?- is_head_item(lit, [lit, dank, snack])` returns `true.`
  - `?- is_head_item(drip, [lit, dank, snack])` returns `false.` because `drip` not the same as `lit`
-     is_second_item(Y, [X, Y | XS])
  - `?- is_second_item(dank, [lit, dank, snack])` returns `true.`
  - `?- is_second_item(lit, [lit, dank, snack])` returns `false.`
-     is_member(X, [X | Tail]).
      is_member(Y, [_ | Tail]) :- is_member(Y, Tail).
  - `?- is_member(dank, [lit, dank, snack])` returns `true.`
    - First tries to match `is_member(dank, [lit | [dank, snack]])` but fails
    - Recurses onto `is_member(dank, [_ | [dank, snack]])`, now trying to prove `is_member(dank, [dank, snack])`
    - This now matches `is_member(dank, [dank | [snack]])`, so `true.` is returned. However, Prolog would continue to search after this.
-     delete(Item, [], []).
      delete(Item, [Item | Tail], Tail).
      delete(Item, [Head | Tail], [Head | FinalTail]) :- delete(Item, Tail, FinalTail).
  - `?- delete(carey, [carey, david, paul], X)` returns `X = [david, paul]`, matching the second predicate
  - `?- delete(david, [carey, david, paul], X)` matches the third predicate, recursing to `delete(david, [david, paul], FinalTail)`
    - This resolves `FinalTail = [paul]`, and so the result is `X = [Head_ | FinalTail] = [carey | [paul]] = [carey, paul]`
- Built-in methods:
  - `append(X, Y, Z)`: Determines if list X concatenated with list Y is equal to list Z
  - `reverse(X, Y)`: Determines if list X is the reverse of list Y
  - `sort(X, Y)`: Determines if the elements in Y are the same as X, but in sorted order
  - `member(X, Y)`: Determines if X is a member of list Y 
  - `permutation(X, Y)`: Determines if elements in Y are the same elements of X but in a different ordering  
  - `sum_list(X, Y)`: Determines if the sum of all elements in X sum up to Y