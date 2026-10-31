#include <iostream>
#include <cstdint>
using namespace std;

// Base class for dynamic_cast
class Base {
public:
    virtual void display() {
        cout << "Base class" << endl;
    }
};

// Derived class
class Derived : public Base {
public:
    void show() {
        cout << "Derived class" << endl;
    }
};

int main() {

    // 1. static_cast
    // Converts an integer into a float
    int num = 10;
    float value = static_cast<float>(num);

    cout << "Static Cast: " << value << endl;


    // 2. dynamic_cast
    // Converts a base class pointer to derived class pointer
    Base* basePtr = new Derived();

    Derived* derivedPtr = dynamic_cast<Derived*>(basePtr);

    if (derivedPtr != nullptr) {
        cout << "Dynamic Cast: ";
        derivedPtr->show();
    }

    delete basePtr;


    // 3. const_cast
    // Removes const qualification from a pointer
    int x = 20;
    const int* constPtr = &x;

    int* modPtr = const_cast<int*>(constPtr);

    *modPtr = 30;

    cout << "Const Cast: " << x << endl;


    // 4. reinterpret_cast
    // Converts a pointer into an integer representation
    int a = 50;
    int* ptr = &a;

    uintptr_t address = reinterpret_cast<uintptr_t>(ptr);

    cout << "Reinterpret Cast Address: "
         << address << endl;

    return 0;
}