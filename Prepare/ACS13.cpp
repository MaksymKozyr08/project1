#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <iomanip>

using namespace std;

struct BenchmarkResult {
    string operation;
    string type_label;
    double ops_per_sec;
};

vector<BenchmarkResult> results_storage;
volatile double sink_hole;

double get_timestamp() {
    auto now = chrono::high_resolution_clock::now();
    return chrono::duration<double>(now.time_since_epoch()).count();
}

template <typename T>
void perform_test(string label) {
    double t_start, t_end, empty_start, empty_end, delta, rate, sum_rate;
    T v1, v2, v3; 

    long total_loops = 2000000;
    T divisor = (T)3;
    if (divisor == 0) divisor = 1;
   
    // Додавання
    sum_rate = 0;
    for (int k = 0; k < 10; k++) {
        v1 = 0; v2 = 1; v3 = 0;
        t_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1 + v2; v2 = v1 + v3; v1 = v2 + v3; v3 = v1 + v2; v2 = v1 + v3;
            v1 = v2 + v3; v3 = v1 + v2; v2 = v1 + v3; v1 = v2 + v3; v3 = v1 + v2;
        }
        t_end = get_timestamp();
        sink_hole = (double)v3;

        v1 = 0; v2 = 1; v3 = 0;
        empty_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1; v2 = v3; v1 = v2; v3 = v1; v2 = v3;
            v1 = v2; v3 = v1; v2 = v3; v1 = v2; v3 = v1;
        }
        empty_end = get_timestamp();
        sink_hole = (double)v3;
        
        delta = (t_end - t_start) - (empty_end - empty_start);
        if (delta <= 1e-9) delta = (t_end - t_start);
        if (delta <= 1e-9) delta = 1e-9; 

        rate = (10.0 * total_loops) / delta;
        sum_rate += rate;
    }
    results_storage.push_back({"+", label, sum_rate / 10.0});

    // Віднімання
    sum_rate = 0;
    for (int k = 0; k < 10; k++) {
        v1 = 0; v2 = 1; v3 = 0;
        t_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1 - v2; v2 = v1 - v3; v1 = v2 - v3; v3 = v1 - v2; v2 = v1 - v3;
            v1 = v2 - v3; v3 = v1 - v2; v2 = v1 - v3; v1 = v2 - v3; v3 = v1 - v2;
        }
        t_end = get_timestamp();
        sink_hole = (double)v3;

        v1 = 0; v2 = 1; v3 = 0;
        empty_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1; v2 = v3; v1 = v2; v3 = v1; v2 = v3;
            v1 = v2; v3 = v1; v2 = v3; v1 = v2; v3 = v1;
        }
        empty_end = get_timestamp();
        sink_hole = (double)v3;
        
        delta = (t_end - t_start) - (empty_end - empty_start);
        if (delta <= 1e-9) delta = (t_end - t_start);
        if (delta <= 1e-9) delta = 1e-9;

        rate = (10.0 * total_loops) / delta;
        sum_rate += rate;
    }
    results_storage.push_back({"-", label, sum_rate / 10.0});

    // Множення
    sum_rate = 0;
    for (int k = 0; k < 10; k++) {
        v1 = 1; v2 = 1; v3 = 1;
        t_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1 * v2; v2 = v1 * v3; v1 = v2 * v3; v3 = v1 * v2; v2 = v1 * v3;
            v1 = v2 * v3; v3 = v1 * v2; v2 = v1 * v3; v1 = v2 * v3; v3 = v1 * v2;
        }
        t_end = get_timestamp();
        sink_hole = (double)v3;

        v1 = 1; v2 = 1; v3 = 1;
        empty_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1; v2 = v3; v1 = v2; v3 = v1; v2 = v3;
            v1 = v2; v3 = v1; v2 = v3; v1 = v2; v3 = v1;
        }
        empty_end = get_timestamp();
        sink_hole = (double)v3;
        
        delta = (t_end - t_start) - (empty_end - empty_start);
        if (delta <= 1e-9) delta = (t_end - t_start);
        if (delta <= 1e-9) delta = 1e-9;

        rate = (10.0 * total_loops) / delta;
        sum_rate += rate;
    }
    results_storage.push_back({"*", label, sum_rate / 10.0});

    // Ділення
    sum_rate = 0;
    for (int k = 0; k < 10; k++) {
        v1 = 1000000; v2 = 1; v3 = 1;
        t_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1 / divisor; v2 = v1 / divisor; v1 = v1 / divisor + 1;
            v3 = v1 / divisor; v2 = v1 / divisor; v1 = v1 / divisor + 1;
            v3 = v1 / divisor; v2 = v1 / divisor; v1 = v1 / divisor + 1;
            v3 = v1 / divisor;
        }
        t_end = get_timestamp();
        sink_hole = (double)v3;

        v1 = 1000000; v2 = 1; v3 = 1;
        empty_start = get_timestamp();
        for (long i = 0; i < total_loops; i++) {
            v3 = v1; v2 = v1; v1 = v1 + 1;
            v3 = v1; v2 = v1; v1 = v1 + 1;
            v3 = v1; v2 = v1; v1 = v1 + 1;
            v3 = v1;
        }
        empty_end = get_timestamp();
        sink_hole = (double)v3;

        delta = (t_end - t_start) - (empty_end - empty_start);
        if (delta <= 1e-9) delta = (t_end - t_start);
        if (delta <= 1e-9) delta = 1e-9;

        rate = (10.0 * total_loops) / delta;
        sum_rate += rate;
    }
    results_storage.push_back({"/", label, sum_rate / 10.0});
}

int main() {
    setlocale(LC_ALL, "");
    
    perform_test<int>("int");
    perform_test<long>("long");
    perform_test<double>("dbl");
    perform_test<float>("flt");

    double max_val = 0;
    for (const auto& r : results_storage) {
        if (r.ops_per_sec > max_val) max_val = r.ops_per_sec;
    }

    cout << "----------------------------------------------------------------------\n";
    cout << left << setw(8) << "Type Op" 
         << setw(15) << "Ops/Sec" 
         << "Graph" << endl;
    cout << "----------------------------------------------------------------------\n";

    for (const auto& r : results_storage) {
        int percent = (max_val > 0) ? (int)((r.ops_per_sec / max_val) * 100) : 0;
        int bars = (max_val > 0) ? (int)((r.ops_per_sec / max_val) * 20) : 0;

        string visual_bar = "[" + string(bars, '=') + string(20 - bars, ' ') + "]";

        cout << left << setw(5) << r.type_label 
             << setw(3) << r.operation
             << setw(15) << scientific << setprecision(2) << r.ops_per_sec
             << setw(23) << visual_bar
             << percent << "%" << endl;
    }
    cout << "----------------------------------------------------------------------\n";

    return 0;
}