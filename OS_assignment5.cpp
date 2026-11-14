
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <limits>
using namespace std;

struct Result {
    string algorithm;
    int faults = 0, hits = 0;
    double hitRatio = 0, faultRatio = 0;
};

void displayFrames(const vector<int>& frames, int capacity) {
    cout << "[ ";
    for (int i = 0; i < capacity; i++) {
        if (i < (int)frames.size())
            cout << frames[i] << " ";
        else
            cout << "- ";
    }
    cout << "]";
}

// FIFO Algorithm
Result FIFO(vector<int> pages, int capacity) {
    Result r;
    r.algorithm = "FIFO";
    vector<int> frames;
    int pointer = 0;

    cout << "\n========== FIFO ==========\n";
    cout << "Page\tFrames\t\tStatus\n";

    for (int page : pages) {
        auto it = find(frames.begin(), frames.end(), page);
        string status;

        if (it != frames.end()) {
            r.hits++;
            status = "HIT";
        } else {
            r.faults++;
            status = "FAULT";

            if ((int)frames.size() < capacity)
                frames.push_back(page);
            else {
                frames[pointer] = page;
                pointer = (pointer + 1) % capacity;
            }
        }

        cout << page << "\t";
        displayFrames(frames, capacity);
        cout << "\t" << status << "\n";
    }

    r.hitRatio = (double)r.hits / pages.size();
    r.faultRatio = (double)r.faults / pages.size();
    return r;
}

// LRU Algorithm
Result LRU(vector<int> pages, int capacity) {
    Result r;
    r.algorithm = "LRU";
    vector<int> frames, lastUsed;

    cout << "\n========== LRU ==========\n";
    cout << "Page\tFrames\t\tStatus\n";

    for (int time = 0; time < (int)pages.size(); time++) {
        int page = pages[time];
        auto it = find(frames.begin(), frames.end(), page);
        string status;

        if (it != frames.end()) {
            r.hits++;
            status = "HIT";
            int index = it - frames.begin();
            lastUsed[index] = time;
        } else {
            r.faults++;
            status = "FAULT";

            if ((int)frames.size() < capacity) {
                frames.push_back(page);
                lastUsed.push_back(time);
            } else {
                int victim = min_element(
                    lastUsed.begin(), lastUsed.end()
                ) - lastUsed.begin();

                frames[victim] = page;
                lastUsed[victim] = time;
            }
        }

        cout << page << "\t";
        displayFrames(frames, capacity);
        cout << "\t" << status << "\n";
    }

    r.hitRatio = (double)r.hits / pages.size();
    r.faultRatio = (double)r.faults / pages.size();
    return r;
}

// Optimal Algorithm
Result Optimal(vector<int> pages, int capacity) {
    Result r;
    r.algorithm = "Optimal";
    vector<int> frames;

    cout << "\n========== OPTIMAL ==========\n";
    cout << "Page\tFrames\t\tStatus\n";

    for (int i = 0; i < (int)pages.size(); i++) {
        int page = pages[i];
        auto it = find(frames.begin(), frames.end(), page);
        string status;

        if (it != frames.end()) {
            r.hits++;
            status = "HIT";
        } else {
            r.faults++;
            status = "FAULT";

            if ((int)frames.size() < capacity) {
                frames.push_back(page);
            } else {
                int victim = -1;
                int farthest = -1;

                for (int j = 0; j < (int)frames.size(); j++) {
                    int nextUse = numeric_limits<int>::max();

                    for (int k = i + 1; k < (int)pages.size(); k++) {
                        if (pages[k] == frames[j]) {
                            nextUse = k;
                            break;
                        }
                    }

                    if (nextUse > farthest) {
                        farthest = nextUse;
                        victim = j;
                    }
                }

                frames[victim] = page;
            }
        }

        cout << page << "\t";
        displayFrames(frames, capacity);
        cout << "\t" << status << "\n";
    }

    r.hitRatio = (double)r.hits / pages.size();
    r.faultRatio = (double)r.faults / pages.size();
    return r;
}

// Display comparison
void compareResults(vector<Result> results) {
    cout << "\n========== PERFORMANCE COMPARISON ==========\n";

    cout << left << setw(12) << "Algorithm"
         << setw(12) << "Faults"
         << setw(12) << "Hits"
         << setw(15) << "Hit Ratio"
         << setw(15) << "Fault Ratio" << "\n";

    for (auto r : results) {
        cout << left << setw(12) << r.algorithm
             << setw(12) << r.faults
             << setw(12) << r.hits
             << fixed << setprecision(2)
             << setw(14) << r.hitRatio * 100 << "%"
             << r.faultRatio * 100 << "%\n";
    }

    int minimum = results[0].faults;
    for (auto r : results)
        minimum = min(minimum, r.faults);

    cout << "\nBest performing algorithm: ";
    for (auto r : results) {
        if (r.faults == minimum)
            cout << r.algorithm << " ";
    }
    cout << "\nMinimum Page Faults: " << minimum << "\n";
}

int main() {
    cout << "============================================\n";
    cout << " VIRTUAL MEMORY AND PAGE REPLACEMENT SIMULATOR\n";
    cout << "              FOR ML WORKLOADS\n";
    cout << "============================================\n";

    int n, capacity;

    cout << "\nEnter number of page references: ";
    if (!(cin >> n) || n <= 0) {
        cout << "Invalid input!\n";
        return 1;
    }

    vector<int> pages(n);

    cout << "Enter page reference string:\n";
    for (int i = 0; i < n; i++) {
        cin >> pages[i];
        if (!cin || pages[i] < 0) {
            cout << "Invalid page number!\n";
            return 1;
        }
    }

    cout << "Enter number of physical frames: ";
    if (!(cin >> capacity) || capacity <= 0) {
        cout << "Invalid frame count!\n";
        return 1;
    }

    cout << "\nPage Reference String: ";
    for (int p : pages)
        cout << p << " ";

    cout << "\nPhysical Frames: " << capacity << "\n";

    vector<Result> results;

    results.push_back(FIFO(pages, capacity));
    results.push_back(LRU(pages, capacity));
    results.push_back(Optimal(pages, capacity));

    compareResults(results);

    cout << "\nML WORKLOAD INTERPRETATION\n";
    cout << "Pages represent model parameters, tensor data,\n";
    cout << "or intermediate computations.\n";
    cout << "A page fault means the required page is not in\n";
    cout << "physical memory and must be loaded.\n";

    return 0;
}
