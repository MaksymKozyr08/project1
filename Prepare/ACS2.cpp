#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <iomanip>

using namespace std;

string ops_list[20];
string types_list[20];
double speeds_list[20];
int test_count = 0;

volatile double global_sink;

double Time() {
    auto now = chrono::high_resolution_clock::now();
    return chrono::duration<double>(now.time_since_epoch()).count();
}

template <typename T>
void run_benchmark(string type_name) {
    double t1, t2, t01, t02, t, d, d0;
    T a, b, c; 

    long iterations = 2000000;

    // для ділення
    T safe_divisor = (T)3;
    if (safe_divisor == 0) safe_divisor = 1;
   
    // "+"
    d0 = 0;
    for (int k = 1; k <= 10; k++) {
    
        a = 0; b = 1; c = 0;
        t1 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a + b; b = a + c; a = b + c; c = a + b; b = a + c;
            a = b + c; c = a + b; b = a + c; a = b + c; c = a + b;
        }
        t2 = Time();
        global_sink = (double)c;

        a = 0; b = 1; c = 0;
        t01 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a; b = c; a = b; c = a; b = c;
            a = b; c = a; b = c; a = b; c = a;
        }
        t02 = Time();
        global_sink = (double)c;
        
        t = (t2 - t1) - (t02 - t01);
        if (t <= 1e-9) t = (t2 - t1);
        if (t <= 1e-9) t = 1e-9; 

        d = (10.0 * iterations) / t;
        d0 += d;
    }
    ops_list[test_count] = "+";
    types_list[test_count] = type_name;
    speeds_list[test_count] = d0 / 10;
    test_count++;

    // "-"
    d0 = 0;
    for (int k = 1; k <= 10; k++) {
        a = 0; b = 1; c = 0;
        t1 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a - b; b = a - c; a = b - c; c = a - b; b = a - c;
            a = b - c; c = a - b; b = a - c; a = b - c; c = a - b;
        }
        t2 = Time();
        global_sink = (double)c;

        a = 0; b = 1; c = 0;
        t01 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a; b = c; a = b; c = a; b = c;
            a = b; c = a; b = c; a = b; c = a;
        }
        t02 = Time();
        global_sink = (double)c;
        
        t = (t2 - t1) - (t02 - t01);
        if (t <= 1e-9) t = (t2 - t1);
        if (t <= 1e-9) t = 1e-9;

        d = (10.0 * iterations) / t;
        d0 += d;
    }
    ops_list[test_count] = "-";
    types_list[test_count] = type_name;
    speeds_list[test_count] = d0 / 10;
    test_count++;

    // "*"
    d0 = 0;
    for (int k = 1; k <= 10; k++) {
        a = 1; b = 1; c = 1;
        t1 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a * b; b = a * c; a = b * c; c = a * b; b = a * c;
            a = b * c; c = a * b; b = a * c; a = b * c; c = a * b;
        }
        t2 = Time();
        global_sink = (double)c;

        a = 1; b = 1; c = 1;
        t01 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a; b = c; a = b; c = a; b = c;
            a = b; c = a; b = c; a = b; c = a;
        }
        t02 = Time();
        global_sink = (double)c;
        
        t = (t2 - t1) - (t02 - t01);
        if (t <= 1e-9) t = (t2 - t1);
        if (t <= 1e-9) t = 1e-9;

        d = (10.0 * iterations) / t;
        d0 += d;
    }
    ops_list[test_count] = "*";
    types_list[test_count] = type_name;
    speeds_list[test_count] = d0 / 10;
    test_count++;

    // "/"
    d0 = 0;
    for (int k = 1; k <= 10; k++) {
        a = 1000000; b = 1; c = 1;
        t1 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a / safe_divisor; b = a / safe_divisor; a = a / safe_divisor + 1;
            c = a / safe_divisor; b = a / safe_divisor; a = a / safe_divisor + 1;
            c = a / safe_divisor; b = a / safe_divisor; a = a / safe_divisor + 1;
            c = a / safe_divisor;
        }
        t2 = Time();
        global_sink = (double)c;
        

        a = 1000000; b = 1; c = 1;
        t01 = Time();
        for (long i = 1; i <= iterations; i++) {
            c = a; b = a; a = a + 1;
            c = a; b = a; a = a + 1;
            c = a; b = a; a = a + 1;
            c = a;
        }
        t02 = Time();
        global_sink = (double)c;

        t = (t2 - t1) - (t02 - t01);
        if (t <= 1e-9) t = (t2 - t1);
        if (t <= 1e-9) t = 1e-9;

        d = (10.0 * iterations) / t;
        d0 += d;
    }
    ops_list[test_count] = "/";
    types_list[test_count] = type_name;
    speeds_list[test_count] = d0 / 10;
    test_count++;
}

int main() {
    setlocale(LC_ALL, "");
    cout << "Please wait" << endl;

    run_benchmark<int>("int");
    run_benchmark<long>("long");
    run_benchmark<double>("double");
    run_benchmark<float>("float");

    double max_speed = 0;
    for (int i = 0; i < test_count; i++) {
        if (speeds_list[i] > max_speed) max_speed = speeds_list[i];
    }

    cout << "\n--------------------------------------------------------------------------------------\n";
    cout << left << setw(5) << "Op"
        << setw(10) << "Type"
        << setw(15) << "Ops/Sec"
        << setw(45) << "Diagram"
        << "%" << endl;
    cout << "--------------------------------------------------------------------------------------\n";

    for (int i = 0; i < test_count; i++) {
        int percent = 0;
        if (max_speed > 0) percent = (int)((speeds_list[i] / max_speed) * 100);

        int bar_len = 0;
        if (max_speed > 0) bar_len = (int)((speeds_list[i] / max_speed) * 40);

        string bar = "";
        for (int j = 0; j < bar_len; j++) bar += "-";

        cout << left << setw(5) << ops_list[i]
            << setw(10) << types_list[i]
            << setw(15) << scientific << setprecision(2) << speeds_list[i]
            << setw(45) << bar
            << percent << "%" << endl;
    }
    cout << "--------------------------------------------------------------------------------------\n";

    return 0;
}