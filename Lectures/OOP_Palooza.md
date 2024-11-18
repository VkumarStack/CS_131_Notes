# Object-Oriented Programming Palooza
## Essential Components of OOP
- **Classes**: A class is a *blueprint* for creating new objects, defining a *public interface*, *code for methods*, and *data fields*
  - Object-oriented languages do not necessarily need to have classes
- **Objects**: A representation of a particular "thing", with an *interface*, *code*, and *field values*
- **Interfaces**: A related group of function declarations that we want one or more classes to implement
- **Inheritance**: A derived class inherits either the *code*, the *interface*, or *both* from a base class, and a derived class can override the base class's code or expand its interface
- **Subtype Polymorphism**: Code designed to operate on objects of type `T` can operate on any object that is a subtype of `T`
- **Dynamic Dispatch**: The actual code that runs when a method is called depends on the target object, and can only be determined at runtime
- **Encapsulation**: The bundling of public interface and private data fields/code together into a cohesive unit
## Classes
- Typical classes consist of an *interface* (its public methods), its *fields* (member variables), *private methods*, and *method implementations*
- Example (C++):
  -     class Nerd {
          public:
            Nerd(const string& name);
            ~Nerd();
            string talk() const;

          private:
            string name_;
            int IQ_;

            void study(int hrs);
        };

        Nerd::Nerd(const string& name) {
          this->name = name;
          IQ_ = 100;
          study(3);
        }

        Nerd::~Nerd() { IQ_ = 0; }
        string Nerd::talk() const {
          return name_ + " likes closures.";
        }

        void Nerd::study(int hrs) { IQ_ += hrs; 
        }
- Some languages (e.g. Go and Rust), isolate its data members from its methods
  -     type Nerd struct {
          name string
          iq int
        }

        func NewNerd(name_nerd string) *Nerd {
          nerd := Nerd {
            name: nerd_name,
            iq: 100,
          }
          nerd.study(3)
          return &nerd
        }
    - `NewNerd` is like any other function, and it creates a Nerd struct and then returns it
## Objects
- Objects are often created from a class blueprint, and each object has its *own copy* of fields and methods
- Objects, however, do not necessarily come from classes
  - JavaScript, for example, *only has objects* (classes are syntactic sugar) - all objects are dictionaries
    -     var student1 = {
            first: "Alan",
            last: "Kay",
            phone: "818-555-1212",
            student_id: 95833245,
            fullName: function () { return this.first + " " + this.last; }
          }

          student1["tellJoke"] = function() { return "Two mice walk into a bar"; }
          console.log(student1.fullName() + " says " + student1.tellJoke());
  - Classes are typically used, however, to *ensure* that objects are constructed in the *same way* - we have a standardization of object fields and methods
## Encapsulation and Access Modifiers
- Encapsulation is the *guiding principle* behind the object-oriented programming paradigm
  - The goal is to bundle *public interface*, *data*, and *code* together into a cohesive, problem-solving unit
  - Private *data* and *implementation details* are hidden from clients, forcing them to use the *public interface*
- Encapsulation allows for safer, more efficient software development:
  - **Simpler Programs**: There is *reduced coupling* between modules because each class only depends on the *public interface* of other classes (and not any private data or implementation details)
  - **Easier Improvements**: Implementations can be improved without impacting other components, since we can change how the *internal code* of a class works without altering its *public interface*
  - **Better Modularity**: Once a class is built, it can be reused in different contexts - this allows for designing and testing of code to be isolated from other code
- Languages typically provide **access modifiers** which specify the visibility/accessibility of methods or fields to code outside of a class
  - **Public**: Any part of the program can access the method or data
  - **Protected**: Only the class and its subclasses can access the method or data
  - **Private**: Only the class (not any subclasses) can access the method or data
  - Example (C++):
    -     class Person {
            public:
              Person(string name) { name_ = name; }
              void talk()
              { cout << "Hi, I'm " << name_ << "\n"; }
            
            protected:
              void daydream() { cout << "Rainbow goats\n"; }
            
            private:
              void poop() { cout << "Grunt... plop\n"; }
              string name_;
          }

          class Student: public Person {
            ...
            void dostuff() {
              talk(); // Works - talk is public
              daydream(); // Works - daydream is protected
              poop(); // Error - poop is private
            }
          }

          int main() {
            Person p("Irna");
            p.talk(); // Works - public
            p.daydream(); // Error - protected
            p.poop(); // Error - private
          }
  - Example (Python): All methods are public by default. A protected method has a leading underscore. A private method has two leading underscores (but not trailing underscores, as this would be a dunder method which are public). Protected methods are actually *not enforced* (though private methods are)
    -     class Person:
            def __init__(self, name):
              self.__name = name # Private
            # Public
            def talk(self):
              print("Hi, my name is " self.__name)
            
            # Protected (not enforced)
            def _daydream(self):
              print("Rainbow narwhals")

            # Private
            def __poop(self):
              print("Grunt... plop!")

              a = Student("Cindi")
              a.talk() # Works
              a._daydream() # Works but shouldn't
              a.__poop() # Raises an error
- Best practices:
  - Design classes such that they *hide all implementation details* from other classes
  - Make all member fields, constants, and *helper* methods private
  - Avoid providing *getters/setters* for fields that are specific to the current implementation (as to reduce coupling)
  - Make sure constructors completely initialize objects, so users do not have to call other methods to create a fully-valid object
## This and Self
- When a method runs, it needs some way to determine *what object* it is operating on, and this can accomplished by passing a special parameter to each method: `this` or `self`
  - Some languages require that this be explicitly specified (e.g. Python function methods must be of the form `def funcName(self, ...)`) while other languages treat this as optional (e.g. C++ `this` is implicitly passed to each class method, and `this` is only necessary in classes to disambiguate from local/global variables)
  - Whenever a method call is made (e.g. `n.talk()`), the object before the method is implicitly passed to the method
- The `this` or `self` constructs are syntactic sugar:
  - Code:
    -     class Nerd {
            private:
              string name;
              int iq;
            public:
              Nerd(const string& name) {
                this->name = name;
                IQ = 100;
              }

              string talk() {
                return this->name + " likes PI.";
              }
          }

          Nerd n("Carey");
          cout << n.talk();
  - Under the Hood:
    -     struct Nerd {
            string name;
            int IQ;
          }

          void init(Nerd *this, const string& name) {
            this->name = name;
            this->IQ = 100;
          }

          string talk(Nerd *this) {
            return this->name + " likes PI.";
          }

          Nerd n;
          init(&n, "Carey");
          cout << talk(&n);
## Getters and Setters
- It may be necessary to expose a *field* of an object for external use, and this can be achieved through the usage of **accessors** (getters) and **mutators** (setters)
  - Rather than directly expose the field, doing this can allow for the implementation to be hidden and can even create the illusion that an object holds a field (when it does not)
- Example:
  -     class Student {
          public:
            void changeName(const string& name) {
              name_ = name;
            }
            double getGPA() const {
              double GPA = 0;
              for (auto c: courses_ )
                GPA += c.score();
              return GPA / courses_.size();
            }
          private:
            double name_;
            std::vector<Course> courses_;
        };
- In Python, decorators can be used to specify getters and setters for an object *as if they were property accesses or mutations*
  -     class Person:
          ...
          @property
          def age(self):
            return self._age

          @age.setter
          def age(self, age):
            if age >= 0 and age <= 130:
              self._age = age
            else:
              raise ValueError("Invalid age!")
          
          a = Person("Archna")
          print(a.age) # Calls getter
          a.age = 45 # Calls setter
  - A property method should be used when exposing the state of a class, or exposing a state that requires *minor computation*
  - Traditional methods should be used when exposing behaviors of a class (which are not necessarily a member variable) or exposing a state that requires heavy computation
## Inheritance
- **Interface Inheritance**: An interface defines a group of function *declarations* that we want a class to implement. A class *implements* an interface `I` by providing code for all of `I`'s functions
  - This should be used when *unrelated classes* must provide a common set of behavors, but there is no common implementations to inherit
    - Example: `Media Players` like Spotify (`Music`) and Netflix (`Video`) play media, but do so in a different way
      -     interface Playable {
              public void play();
              public void pause();
              public void fast_forward();
              public void rewind(int sec);
            }
            class Netflx implements Playable {
              public void play()
                { /* logic to play a movie */ }
              ...
            }
            class Spotify implements Playable {
              public void play()
                { /* logic to play a song */ }
              ...
            }

            public void launch_media(Playable p) {
              p.play();
            }
  - Interfaces allow for a single class to support multiple *personas*. When a class implements an interface, objects of that class have *multiple types* (a type associated with the class, and a type associated with the interface)
    - Example (C++):
      -     class Washable {
              public:
                virtual void wash() = 0;
                virtual void dry() = 0;
            }
            class Drivable {
              public:
                virtual void accelerate() = 0;
                virtual void brake() = 0;
            }
            class Car: public Washable, public Driable {
              public:
                // Car methods
                void turnOn() { ... }

                // Washable methods
                void wash() { ... }
                void dry() { ... }

                // Drivable methods
                void accelerate() { ... }
                void brake() { ... }
            }

            void cleanUp(Washable& w) {
              w.wash();
              w.dry();
            }

            void driveToUCLA(Drivable d) {
              d.accelerate();
              d.brake();
            }

            int main() {
              Car forrester;
              cleanUp(forrester);
              driveToUCLA(forrester);
            }
  - Common use of interfaces: Making objects comparable with each other (e.g. Java `Comparable` interface), specifying common operations across differing container classes (e.g. supporting `add`, `remove`, `size`, `iterate`, etc. for `List`, `Vector`, `Maps`, `Sets`, `etc`)
  - Interface inheritance should be used when there is a *can-support* relationship between a class and a group of behaviors or when there are different classes that all need to support related behaviors but are not related to the base class 
    - Abstract classes should be used instead of interfaces when a base class has common code that multiple derived classes can inherit and use (e.g. an abstract `Car` class has an implemented `drive` method common across all cars, but derived classes might have other differing implementations like `refuel` for `ElectricCar` versus `refuel` for `GasCar`)
- **Implementation Inheritance**: A base class's method is *reused privately*. A derived class inherits method implementations from a base class.
- **Subclassing Inheritance** (Mixture of both): A base class provides a *public interface and implementations* for its methods. A derived class inherits both the base class's interface *and* its implementations
  - The base class defines *public methods* with optional implementations as well as private/protected methods. The derived class inhrerits the base class's public interface and all of its method's implementations. The derived class may add new methods or override existing implementations
  - Example: C++ (only `virtual` methods must be overriden; non-virtual functions are *final*)
    -     class Shape {
            public:
              Shape(float x, float y) { x_ = x; y_ = y; }
              void setColor(Color c) { color_c = c; }
              virtual void disappear() { setColor(Black); }
              virtual float area() const = 0;
              ...
            protected:
              void printShapeDebugInfo() const { ... }
          }
          class Circle : public Shape {
            public:
              Circle(float x, float y, float r) : Shape (x, y)
                { rad_r = r; }
              float radius() const { return rad_; }
              float area() const { return PI * rad_ * rad_; }
              virtual void disappear() {
                for (int i = 0; i < 10; ++i)
                  rad_ *= 0.1;
                  Shape::disappear();
              }
          }
