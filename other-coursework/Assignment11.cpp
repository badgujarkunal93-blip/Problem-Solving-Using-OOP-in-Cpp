#include <iostream>
#include <list>
#include <vector>
#include <iterator>
using namespace std;

int main() {

    // -------- LIST CONTAINER --------

    // Create a list of integers
    list<int> l = {10, 20, 30, 40};

    // Display the original list
    cout << "Original List: ";
    for (int x : l) {
        cout << x << " ";
    }

    // Insert elements at the beginning and end
    l.push_front(5);
    l.push_back(50);

    // Delete the first and last elements
    l.pop_front();
    l.pop_back();

    // Insert 25 at the third position
    auto it = l.begin();
    advance(it, 2);
    l.insert(it, 25);

    // Display the updated list
    cout << "\nUpdated List: ";
    for (int x : l) {
        cout << x << " ";
    }


    // -------- VECTOR CONTAINER --------

    // Create a vector of integers
    vector<int> v = {10, 20, 30, 40};

    // Display the original vector
    cout << "\n\nOriginal Vector: ";
    for (int x : v) {
        cout << x << " ";
    }

    // Insert elements at the beginning and end
    v.push_back(50);
    v.insert(v.begin(), 5);

    // Delete the last element
    v.pop_back();

    // Display the updated vector
    cout << "\nUpdated Vector: ";
    for (int x : v) {
        cout << x << " ";
    }

    // Access an element using its index
    cout << "\nElement at index 2: " << v[2];

    // Display the size of the vector
    cout << "\nSize of Vector: " << v.size();

    return 0;
}