#include <iostream>
using namespace std;
class Student
{
private:
    int rollNo;
    string name;
    float marks;

public:
    Student()
    {
        rollNo = 0;
        name = "Unknown";
        marks = 0;
        cout << "Default Constructor Called" << endl;
    }

    Student(int r, string n, float m)
    {
        rollNo = r;
        name = n;
        marks = m;
        cout << "Parameterized Constructor Called" << endl;
    }

    Student(const Student &s)
    {
        rollNo = s.rollNo;
        name = s.name;
        marks = s.marks;
        cout << "Copy Constructor Called" << endl;
    }

    void display()
    {
        cout << "\nStudent Details:" << endl;
        cout << "Roll No : " << rollNo << endl;
        cout << "Name    : " << name << endl;
        cout << "Marks   : " << marks << endl;
    }

    void calculateGrade()
    {
        if (marks >= 80)
            cout << "Grade : A" << endl;
        else if (marks >= 60)
            cout << "Grade : B" << endl;
        else if (marks >= 40)
            cout << "Grade : C" << endl;
        else
            cout << "Grade : F" << endl;
    }
};

int main()
{
    Student s1;
    s1.display();
    s1.calculateGrade();

    Student s2(100, "Kunal", 90.0);
    s2.display();
    s2.calculateGrade();

    Student s3(s2);
    s3.display();
    s3.calculateGrade();

    return 0;
}