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

// Вспомогательная функция-шаблон, чтобы не дублировать логику для каждого типа
template <typename T>
double run_test(char op) {
    long n = N_BASE;
    if (op == '/') n /= 5; 

    double sum_ops = 0;
    volatile T a = 10, b = 20, c = 0;
    
    if (op == '/' || op == '*') { a = 10000; b = 2; c = 1; }

    for (int k = 0; k < RUNS; k++) {
        clock_t t1 = clock();
        for (long i = 0; i < n; i++) {
            if (op == '+') { c = a + b; b = a + c; a = b + c; }
            else if (op == '-') { c = a - b; b = a - c; a = b - c; }
            else if (op == '*') { c = a * b; b = a * c; a = b * c; if (i % 100 == 0) { a = 2; b = 3; } }
            else if (op == '/') { c = a / b; b = c + 1; a = b + 10; if (b == 0) b = 1; }
        }
        clock_t t2 = clock();

        double time = double(t2 - t1) / CLOCKS_PER_SEC;
        if (time < 1e-9) time = 1e-9;
        
        sum_ops += (3.0 * n) / time;
    }
    return sum_ops / RUNS;
}

int main() {
    vector<Res> v;
    char ops[] = {'+', '-', '*', '/'};

    // Тестируем int
    for(char op : ops) v.push_back({"int " + string(1, op), run_test<int>(op)});
    
    // Тестируем long
    for(char op : ops) v.push_back({"long " + string(1, op), run_test<long>(op)});
    
    // Тестируем float (новое)
    for(char op : ops) v.push_back({"flt " + string(1, op), run_test<float>(op)});
    
    // Тестируем double
    for(char op : ops) v.push_back({"dbl " + string(1, op), run_test<double>(op)});

    double max_v = 0;
    for(const auto& r : v) {
        if(r.val > max_v) max_v = r.val;
    }

    cout << "----------------------------------------------------------------\n";
    cout << " Type Op     Ops/Sec       Graph\n";
    cout << "----------------------------------------------------------------\n";
    
    for(const auto& r : v) {
        int p = (max_v > 0) ? (int)((r.val / max_v) * 100) : 0;
        int bars = p / 5; // 20 делений (100 / 5)
        
        string g = "[";
        for(int j = 0; j < 20; j++) {
            g += (j < bars) ? "=" : " ";
        }
        g += "]";

        cout << setw(10) << left << r.name 
             << setw(12) << scientific << setprecision(2) << r.val 
             << " " << g << " " << setw(3) << right << p << "%" << endl;
    }
    cout << "----------------------------------------------------------------\n";
    
    return 0;
}