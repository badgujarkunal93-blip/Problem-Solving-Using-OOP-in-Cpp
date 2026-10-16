
#include <iostream>
using namespace std;

// Single Inheritance
class Animal {
public:
    void eat() {
        cout << "Animal eats" << endl;
    }
};

class Dog : public Animal {
public:
    void bark() {
        cout << "Dog barks" << endl;
    }
};

// Multilevel Inheritance
class Puppy : public Dog {
public:
    void whine() {
        cout << "Puppy whines" << endl;
    }
};

// Multiple Inheritance
class Printer {
public:
    void print() {
        cout << "Printing" << endl;
    }
};

class Scanner {
public:
    void scan() {
        cout << "Scanning" << endl;
    }
};

class Machine : public Printer, public Scanner {
};

// Hierarchical Inheritance
class Shape {
public:
    void showShape() {
        cout << "This is a shape" << endl;
    }
};

class Circle : public Shape {
public:
    void drawCircle() {
        cout << "Circle displayed" << endl;
    }
};

class Rectangle : public Shape {
public:
    void drawRectangle() {
        cout << "Rectangle displayed" << endl;
    }
};

// Hybrid Inheritance
class Person {
public:
    void showPerson() {
        cout << "Person details displayed" << endl;
    }
};

class Student : virtual public Person {
};

class Employee : virtual public Person {
};

class TeachingAssistant : public Student, public Employee {
};

int main() {
    cout << "Single Inheritance" << endl;
    Dog d;
    d.eat();
    d.bark();

    cout << "\nMultilevel Inheritance" << endl;
    Puppy p;
    p.eat();
    p.bark();
    p.whine();

    cout << "\nMultiple Inheritance" << endl;
    Machine m;
    m.print();
    m.scan();

    cout << "\nHierarchical Inheritance" << endl;
    Circle c;
    Rectangle r;
    c.showShape();
    c.drawCircle();
    r.showShape();
    r.drawRectangle();

    cout << "\nHybrid Inheritance" << endl;
    TeachingAssistant ta;
    ta.showPerson();

    return 0;
}
