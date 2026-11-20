#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
using namespace std;

struct Result {
    string name;
    vector<int> order;
    int totalMovement = 0;
    double averageMovement = 0.0;
};

int calculateMovement(int start, const vector<int>& path) {
    int total = 0, current = start;
    for (int track : path) {
        total += abs(track - current);
        current = track;
    }
    return total;
}

Result runFCFS(const vector<int>& requests, int head) {
    Result r;
    r.name = "FCFS";
    r.order = requests;
    r.totalMovement = calculateMovement(head, r.order);
    r.averageMovement = (double)r.totalMovement / requests.size();
    return r;
}

Result runSSTF(const vector<int>& requests, int head) {
    Result r;
    r.name = "SSTF";
    vector<int> remaining = requests;
    int current = head;

    while (!remaining.empty()) {
        auto it = min_element(remaining.begin(), remaining.end(),
            [current](int a, int b) {
                if (abs(a - current) == abs(b - current))
                    return a < b;
                return abs(a - current) < abs(b - current);
            });

        current = *it;
        r.order.push_back(current);
        remaining.erase(it);
    }

    r.totalMovement = calculateMovement(head, r.order);
    r.averageMovement = (double)r.totalMovement / requests.size();
    return r;
}

Result runSCAN(const vector<int>& requests, int head, int diskSize) {
    Result r;
    r.name = "SCAN";
    vector<int> left, right;

    for (int track : requests) {
        if (track < head) left.push_back(track);
        else right.push_back(track);
    }

    sort(left.begin(), left.end(), greater<int>());
    sort(right.begin(), right.end());

    // Initial direction is toward higher-numbered tracks.
    for (int track : right) r.order.push_back(track);
    if (!right.empty() || !left.empty()) r.order.push_back(diskSize - 1);
    for (int track : left) r.order.push_back(track);

    // Do not count an unnecessary movement to an endpoint if no request
    // exists in the opposite direction.
    if (left.empty() && !r.order.empty() && r.order.back() == diskSize - 1)
        r.order.pop_back();

    r.totalMovement = calculateMovement(head, r.order);
    r.averageMovement = (double)r.totalMovement / requests.size();
    return r;
}

Result runCSCAN(const vector<int>& requests, int head, int diskSize) {
    Result r;
    r.name = "C-SCAN";
    vector<int> left, right;

    for (int track : requests) {
        if (track < head) left.push_back(track);
        else right.push_back(track);
    }

    sort(left.begin(), left.end());
    sort(right.begin(), right.end());

    // Initial direction is toward higher-numbered tracks. Moving from the
    // last track back to track 0 is included in the head movement.
    for (int track : right) r.order.push_back(track);
    if (!left.empty()) {
        r.order.push_back(diskSize - 1);
        r.order.push_back(0);
        for (int track : left) r.order.push_back(track);
    }

    r.totalMovement = calculateMovement(head, r.order);
    r.averageMovement = requests.empty()
        ? 0.0
        : static_cast<double>(r.totalMovement) / requests.size();
    return r;
}

void printResult(const Result& result) {
    cout << "\n" << result.name << "\nService order: ";
    for (size_t i = 0; i < result.order.size(); ++i) {
        if (i != 0) cout << " -> ";
        cout << result.order[i];
    }
    cout << "\nTotal head movement: " << result.totalMovement
         << "\nAverage movement per request: " << fixed << setprecision(2)
         << result.averageMovement << "\n";
}

int main() {
    int diskSize, head, requestCount;

    cout << "Disk size (number of tracks): ";
    if (!(cin >> diskSize) || diskSize <= 0) {
        cerr << "Disk size must be a positive integer.\n";
        return 1;
    }

    cout << "Initial head position (0-" << diskSize - 1 << "): ";
    if (!(cin >> head) || head < 0 || head >= diskSize) {
        cerr << "Initial head position is outside the disk range.\n";
        return 1;
    }

    cout << "Number of requests: ";
    if (!(cin >> requestCount) || requestCount <= 0) {
        cerr << "Number of requests must be positive.\n";
        return 1;
    }

    vector<int> requests(requestCount);
    cout << "Enter " << requestCount << " track request(s): ";
    for (int& track : requests) {
        if (!(cin >> track) || track < 0 || track >= diskSize) {
            cerr << "Each request must be between 0 and " << diskSize - 1 << ".\n";
            return 1;
        }
    }

    printResult(runFCFS(requests, head));
    printResult(runSSTF(requests, head));
    printResult(runSCAN(requests, head, diskSize));
    printResult(runCSCAN(requests, head, diskSize));
    return 0;
}

