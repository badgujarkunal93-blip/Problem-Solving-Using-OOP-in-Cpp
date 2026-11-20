#include <iostream>
using namespace std;

class Shape {
public:
    virtual void area() {
        cout << "Area of shape" << endl;
    }
};

class Rectangle : public Shape {
public:
    void area() override {
        int length = 5, breadth = 4;
        cout << "Area of Rectangle: "
             << length * breadth << endl;
    }
};

class Circle : public Shape {
public:
    void area() override {
        float radius = 3;
        cout << "Area of Circle: "
             << 3.14 * radius * radius << endl;
    }
};

int main() {
    Rectangle r;
    Circle c;

    Shape *ptr;

    ptr = &r;
    ptr->area();

    ptr = &c;
    ptr->area();

    return 0;
}