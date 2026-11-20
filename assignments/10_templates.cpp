#include <iostream>
using namespace std;

// Function Template
// T is a generic data type that can be int, float, etc.
template <class T>
T maximum(T a, T b) {
    // Return the greater of the two values
    return (a > b) ? a : b;
}

// Class Template
// T allows the class to work with different data types
template <class T>
class Calculator {
public:

    // Function to add two values of type T
    T add(T a, T b) {
        return a + b;
    }

    // Function to subtract two values of type T
    T subtract(T a, T b) {
        return a - b;
    }
};

int main() {

    // Create a Calculator object for integer values
    Calculator<int> c1;

    // Create a Calculator object for float values
    Calculator<float> c2;

    // Perform addition using integer values
    cout << "Integer Addition: "
         << c1.add(10, 5) << endl;

    // Perform addition using float values
    cout << "Float Addition: "
         << c2.add(5.5f, 2.5f) << endl;

    // Perform subtraction using integer values
    cout << "Integer Subtraction: "
         << c1.subtract(10, 5) << endl;

    // Call function template with integer values
    cout << "Maximum of 10 and 20: "
         << maximum(10, 20) << endl;

    // Call function template with double values
    cout << "Maximum of 4.5 and 2.3: "
         << maximum(4.5, 2.3) << endl;

    return 0; // End of program
}