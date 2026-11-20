#include <iostream>
#include <string>
#include <utility>
using namespace std;

class Student {
public:
    string name;

    Student(string n) {
        name = n;
    }

    Student(Student&& obj) {
        name = move(obj.name);
    }
};

int main() {
    Student s1("Kunal");

    Student s2(move(s1));

    cout << "Original object: " << s1.name << endl;
    cout << "New object: " << s2.name << endl;

    return 0;
}