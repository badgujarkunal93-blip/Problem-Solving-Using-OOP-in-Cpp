#include <iostream>
using namespace std;

class Complex {
private:
    int real;
    int imaginary;

public:
    // Default constructor
    Complex() : real(0), imaginary(0) {}

    // Parameterized constructor
    Complex(int r, int i) : real(r), imaginary(i) {}

    // Overloads + to add two Complex objects.
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imaginary + other.imaginary);
    }

    void display() const {
        cout << real;
        if (imaginary >= 0) {
            cout << " + " << imaginary << "i";
        } else {
            cout << " - " << -imaginary << "i";
        }
    }
};

int main() {
    Complex defaultNumber;          // Calls the default constructor.
    Complex number1(4, 5);          // Calls the parameterized constructor.
    Complex number2(3, -2);         // Calls the parameterized constructor.
    Complex sum = number1 + number2; // Calls the overloaded + operator.

    cout << "Operator Overloading Using Constructors\n";
    cout << "---------------------------------------\n";
    cout << "Object created using default constructor: ";
    defaultNumber.display();
    cout << "\nFirst complex number: ";
    number1.display();
    cout << "\nSecond complex number: ";
    number2.display();
    cout << "\nSum using overloaded + operator: ";
    sum.display();
    cout << endl;

    return 0;
}
