#include <iostream>
#include <vector>
#include <ctime>
#include <iomanip>
#include <string>
#include <cmath>
#include <algorithm>

using namespace std;

struct TestResult {
    string label;
    double ops_per_sec;
    double error_pct;
};

// Function to perform a series of measurements and ensure stability
TestResult run_benchmark(string label, char op, string type) {
    const int SAMPLES = 10;
    long long iterations = 10000000; // Starting point for iterations
    vector<double> results;

    // We run 12 samples: 2 for "warm-up" and 10 for the actual statistics
    for (int s = 0; s < SAMPLES + 2; s++) {
        volatile double a = 41.25, b = 1.5, c = 0;
        volatile long long al = 41, bl = 9, cl = 0;

        clock_t t1 = clock();
        for (long long i = 0; i < iterations; i++) {
            if (type == "int") {
                if (op == '+') cl = al + bl;
                else if (op == '*') cl = al * bl;
                else if (op == '/') cl = al / bl;
            } else {
                if (op == '+') c = a + b;
                else if (op == '/') c = a / b;
            }
        }
        clock_t t2 = clock();

        double duration = (double)(t2 - t1) / CLOCKS_PER_SEC;
        
        // Adaptive iteration adjustment to ensure duration is long enough for accuracy
        if (duration < 0.1 && s < 2) {
            iterations *= 10;
            s = -1; // Reset and try again with more iterations
            continue;
        }

        if (s >= 2) {
            results.push_back((double)iterations / duration);
        }
    }

    // Calculate Average (Mean)
    double sum = 0;
    for (double r : results) sum += r;
    double mean = sum / SAMPLES;

    // Calculate Standard Deviation for Error Margin
    double sq_sum = 0;
    for (double r : results) sq_sum += pow(r - mean, 2);
    double stdev = sqrt(sq_sum / SAMPLES);
    double error_pct = (stdev / mean) * 100;
    
    return {label, mean, error_pct};
}

void display_results(vector<TestResult>& results) {
    double max_speed = 0;
    for (auto& r : results) if (r.ops_per_sec > max_speed) max_speed = r.ops_per_sec;

    cout << "\n" << string(90, '-') << endl;
    cout << setw(15) << left << "Operation" << " | " 
         << setw(12) << "Ops/Sec" << " | " 
         << setw(40) << "Performance Diagram (Relative)" << " | " 
         << "Error %" << endl;
    cout << string(90, '-') << endl;

    for (auto& r : results) {
        int bar_length = (int)((r.ops_per_sec / max_speed) * 40);
        string bar(bar_length, 'X');

        cout << setw(15) << left << r.label << " | " 
             << scientific << setprecision(2) << r.ops_per_sec << " | " 
             << setw(40) << left << bar << " | " 
             << fixed << setprecision(2) << r.error_pct << "%" << endl;
    }
    cout << string(90, '-') << endl;
}

int main() {
    cout << "Starting hardware performance benchmark..." << endl;
    cout << "Note: Please remain idle for better precision (Target < 2%)." << endl;

    vector<TestResult> results;
    
    // Testing various data types and operations
    results.push_back(run_benchmark("int addition", '+', "int"));
    results.push_back(run_benchmark("int multiply", '*', "int"));
    results.push_back(run_benchmark("int division", '/', "int"));
    results.push_back(run_benchmark("double add",   '+', "double"));
    results.push_back(run_benchmark("double div",   '/', "double"));

    display_results(results);
    
    return 0;
}