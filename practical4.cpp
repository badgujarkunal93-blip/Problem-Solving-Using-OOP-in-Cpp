#include <iostream>
using namespace std;

void readValues(int* values, int n) {
    for (int i = 0; i < n; ++i) {
        cout << "Enter value " << i + 1 << ": ";
        cin >> *(values + i);
    }
}

void analyseValues(const int* values, int n, int& sum, int& maximum) {
    sum = 0;
    maximum = *values;
    for (int i = 0; i < n; ++i) {
        int current = *(values + i);
        sum += current;
        if (current > maximum) {
            maximum = current;
        }
    }
}

int main() {
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    if (n <= 0) {
        cout << "Number of elements must be positive.\n";
        return 0;
    }

    int* values = new int[n];
    readValues(values, n);

    int sum, maximum;
    analyseValues(values, n, sum, maximum);

    cout << "Stored values: ";
    for (int i = 0; i < n; ++i) {
        cout << *(values + i) << " ";
    }
    cout << "\nSum = " << sum;
    cout << "\nMaximum = " << maximum << '\n';

    delete[] values;
    values = nullptr;
    return 0;
}
