#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <iomanip>

using namespace std;

const long N_BASE = 50000000; 
const int RUNS = 5;

struct Res {
    string name;
    double val;
};

double test_int(char op) {
    long n = N_BASE;
    if (op == '/') n /= 5; 

    double sum_ops = 0;
    volatile int a = 10, b = 20, c = 0;
    
    if (op == '/' || op == '*') { a=10000; b=2; c=1; }

    for (int k = 0; k < RUNS; k++) {
        clock_t t1 = clock();
        for (long i = 0; i < n; i++) {
            if (op == '+') { c = a + b; b = a + c; a = b + c; }
            else if (op == '-') { c = a - b; b = a - c; a = b - c; }
            else if (op == '*') { c = a * b; b = a * c; a = b * c; if (i % 100 == 0) { a=2; b=3; } }
            else if (op == '/') { c = a / b; b = c + 1; a = b + 10; if (b == 0) b = 1; }
        }
        clock_t t2 = clock();

        int ta = a, tb = b, tc = c;

        clock_t t3 = clock();
        for (long i = 0; i < n; i++) {
            c = a; b = c; a = b;
        }
        clock_t t4 = clock();

        double time = double((t2 - t1) - (t4 - t3)) / CLOCKS_PER_SEC;
        if (time < 1e-9) time = 1e-9;
        
        sum_ops += (3.0 * n) / time;
    }
    return sum_ops / RUNS;
}

double test_long(char op) {
    long n = N_BASE;
    if (op == '/') n /= 5;

    double sum_ops = 0;
    volatile long a = 10, b = 20, c = 0;
    if (op == '/' || op == '*') { a=10000; b=2; c=1; }

    for (int k = 0; k < RUNS; k++) {
        clock_t t1 = clock();
        for (long i = 0; i < n; i++) {
            if (op == '+') { c = a + b; b = a + c; a = b + c; }
            else if (op == '-') { c = a - b; b = a - c; a = b - c; }
            else if (op == '*') { c = a * b; b = a * c; a = b * c; if (i % 100 == 0) { a=2; b=3; } }
            else if (op == '/') { c = a / b; b = c + 1; a = b + 10; if (b == 0) b = 1; }
        }
        clock_t t2 = clock();

        long ta = a, tb = b, tc = c;

        clock_t t3 = clock();
        for (long i = 0; i < n; i++) {
            c = a; b = c; a = b;
        }
        clock_t t4 = clock();

        double time = double((t2 - t1) - (t4 - t3)) / CLOCKS_PER_SEC;
        if (time < 1e-9) time = 1e-9;
        sum_ops += (3.0 * n) / time;
    }
    return sum_ops / RUNS;
}

double test_double(char op) {
    long n = N_BASE;
    if (op == '/') n /= 5;

    double sum_ops = 0;
    volatile double a = 10, b = 20, c = 0;
    if (op == '/' || op == '*') { a=10000; b=2; c=1; }

    for (int k = 0; k < RUNS; k++) {
        clock_t t1 = clock();
        for (long i = 0; i < n; i++) {
            if (op == '+') { c = a + b; b = a + c; a = b + c; }
            else if (op == '-') { c = a - b; b = a - c; a = b - c; }
            else if (op == '*') { c = a * b; b = a * c; a = b * c; if (i % 100 == 0) { a=2; b=3; } }
            else if (op == '/') { c = a / b; b = c + 1; a = b + 10; if (b == 0) b = 1; }
        }
        clock_t t2 = clock();

        double ta = a, tb = b, tc = c;

        clock_t t3 = clock();
        for (long i = 0; i < n; i++) {
            c = a; b = c; a = b;
        }
        clock_t t4 = clock();

        double time = double((t2 - t1) - (t4 - t3)) / CLOCKS_PER_SEC;
        if (time < 1e-9) time = 1e-9;
        sum_ops += (3.0 * n) / time;
    }
    return sum_ops / RUNS;
}

int main() {
    vector<Res> v;

    v.push_back({"int +", test_int('+')});
    v.push_back({"int -", test_int('-')});
    v.push_back({"int *", test_int('*')});
    v.push_back({"int /", test_int('/')});

    v.push_back({"long +", test_long('+')});
    v.push_back({"long -", test_long('-')});
    v.push_back({"long *", test_long('*')});
    v.push_back({"long /", test_long('/')});

    v.push_back({"dbl +", test_double('+')});
    v.push_back({"dbl -", test_double('-')});
    v.push_back({"dbl *", test_double('*')});
    v.push_back({"dbl /", test_double('/')});

    double max_v = 0;
    for(size_t i = 0; i < v.size(); i++) {
        if(v[i].val > max_v) max_v = v[i].val;
    }

    cout << "----------------------------------------------------------------\n";
    cout << " Type Op     Ops/Sec       Graph\n";
    cout << "----------------------------------------------------------------\n";
    
    for(size_t i = 0; i < v.size(); i++) {
        int p = (int)((v[i].val / max_v) * 100);
        int bars = (p * 20) / 100;
        
        string g = "[";
        for(int j = 0; j < 20; j++) {
            if (j < bars) g += "=";
            else g += " ";
        }
        g += "]";

        cout << setw(9) << left << v[i].name 
             << setw(11) << scientific << setprecision(2) << v[i].val 
             << " " << g << " " << setw(3) << right << p << "%" << endl;
    }
    cout << "----------------------------------------------------------------\n";
    
    return 0;
}