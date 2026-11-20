#include <iostream>
using namespace std;

class Student
{
    int rollno;
    float marks;

public:
    Student()
    {
        rollno = 0;
        marks = 0;
    }

    void getData()
    {
        cout << "Enter roll number: ";
        cin >> rollno;

        cout << "Enter marks: ";
        cin >> marks;
    }

    void display()
    {
        cout << "\nStudent Details" << endl;
        cout << "Roll Number: " << rollno << endl;
        cout << "Marks: " << marks << endl;
    }

    void result()
    {
        if (marks >= 40)
            cout << "Result: Pass" << endl;
        else
            cout << "Result: Fail" << endl;
    }

    ~Student()
    {
    }
};

int main()
{
    Student s;

    s.getData();
    s.display();
    s.result();

    return 0;
}