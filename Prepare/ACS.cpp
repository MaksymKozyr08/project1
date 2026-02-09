#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <iomanip>

using namespace std;

// Налаштування: 50 млн ітерацій для старту
const long BASE_N = 50000000; 
const int K_RUNS = 5;

struct Result { string name; double ops; };

// --- ФУНКЦІЯ ДЛЯ INT ---
double test_int(char op) {
    long N = BASE_N;
    if (op == '/') N /= 5; // Ділення повільне, зменшуємо ітерації

    double total_ops = 0;
    // volatile int - щоб компілятор не викинув змінні
    volatile int a = 10, b = 20, c = 0;
    if (op == '/' || op == '*') { a=10000; b=2; c=1; }

    for (int k = 0; k < K_RUNS; k++) {
        // 1. Час роботи (Математика + Цикл)
        clock_t t1 = clock();
        for (long i = 0; i < N; i++) {
            if (op == '+')      { c=a+b; b=a+c; a=b+c; }
            else if (op == '-') { c=a-b; b=a-c; a=b-c; }
            else if (op == '*') { c=a*b; b=a*c; a=b*c; if(i%100==0){a=2;b=3;} }
            else if (op == '/') { c=a/b; b=c+1; a=b+10; if(b==0)b=1; }
        }
        clock_t t2 = clock();

        // Збереження
        int ta=a, tb=b, tc=c;

        // 2. Час порожнього циклу
        clock_t t01 = clock();
        for (long i = 0; i < N; i++) {
            c=a; b=c; a=b;
        }
        clock_t t02 = clock();

        double t = double((t2 - t1) - (t02 - t01)) / CLOCKS_PER_SEC;
        if (t < 1e-9) t = 1e-9;
        
        // 3 операції * N ітерацій
        total_ops += (3.0 * N) / t;
    }
    return total_ops / K_RUNS;
}

// --- ФУНКЦІЯ ДЛЯ LONG ---
double test_long(char op) {
    long N = BASE_N;
    if (op == '/') N /= 5;

    double total_ops = 0;
    volatile long a = 10, b = 20, c = 0;
    if (op == '/' || op == '*') { a=10000; b=2; c=1; }

    for (int k = 0; k < K_RUNS; k++) {
        clock_t t1 = clock();
        for (long i = 0; i < N; i++) {
            if (op == '+')      { c=a+b; b=a+c; a=b+c; }
            else if (op == '-') { c=a-b; b=a-c; a=b-c; }
            else if (op == '*') { c=a*b; b=a*c; a=b*c; if(i%100==0){a=2;b=3;} }
            else if (op == '/') { c=a/b; b=c+1; a=b+10; if(b==0)b=1; }
        }
        clock_t t2 = clock();

        long ta=a, tb=b, tc=c;

        clock_t t01 = clock();
        for (long i = 0; i < N; i++) {
            c=a; b=c; a=b;
        }
        clock_t t02 = clock();

        double t = double((t2 - t1) - (t02 - t01)) / CLOCKS_PER_SEC;
        if (t < 1e-9) t = 1e-9;
        total_ops += (3.0 * N) / t;
    }
    return total_ops / K_RUNS;
}

// --- ФУНКЦІЯ ДЛЯ DOUBLE ---
double test_double(char op) {
    long N = BASE_N;
    if (op == '/') N /= 5; 

    double total_ops = 0;
    volatile double a = 10, b = 20, c = 0;
    if (op == '/' || op == '*') { a=10000; b=2; c=1; }

    for (int k = 0; k < K_RUNS; k++) {
        clock_t t1 = clock();
        for (long i = 0; i < N; i++) {
            if (op == '+')      { c=a+b; b=a+c; a=b+c; }
            else if (op == '-') { c=a-b; b=a-c; a=b-c; }
            else if (op == '*') { c=a*b; b=a*c; a=b*c; if(i%100==0){a=2;b=3;} }
            else if (op == '/') { c=a/b; b=c+1; a=b+10; if(b==0)b=1; }
        }
        clock_t t2 = clock();

        double ta=a, tb=b, tc=c;

        clock_t t01 = clock();
        for (long i = 0; i < N; i++) {
            c=a; b=c; a=b;
        }
        clock_t t02 = clock();

        double t = double((t2 - t1) - (t02 - t01)) / CLOCKS_PER_SEC;
        if (t < 1e-9) t = 1e-9;
        total_ops += (3.0 * N) / t;
    }
    return total_ops / K_RUNS;
}

int main() {
    vector<Result> results;

    // Ручне додавання тестів
    results.push_back({"int +", test_int('+')});
    results.push_back({"int -", test_int('-')});
    results.push_back({"int *", test_int('*')});
    results.push_back({"int /", test_int('/')});

    results.push_back({"long +", test_long('+')});
    results.push_back({"long -", test_long('-')});
    results.push_back({"long *", test_long('*')});
    results.push_back({"long /", test_long('/')});

    results.push_back({"dbl +", test_double('+')});
    results.push_back({"dbl -", test_double('-')});
    results.push_back({"dbl *", test_double('*')});
    results.push_back({"dbl /", test_double('/')});

    // Пошук максимуму
    double max_val = 0;
    for (const auto& r : results) if (r.ops > max_val) max_val = r.ops;

    // Вивід таблиці
    cout << "----------------------------------------------------------------\n";
    cout << " Type Op     Ops/Sec       Graph\n";
    cout << "----------------------------------------------------------------\n";
    
    for (const auto& r : results) {
        int percent = (int)((r.ops / max_val) * 100);
        int bars = (percent * 20) / 100;
        
        string graph = "[";
        for(int i=0; i<20; i++) graph += (i < bars ? "=" : " ");
        graph += "]";

        cout << setw(9) << left << r.name 
             << setw(11) << scientific << setprecision(2) << r.ops 
             << " " << graph << " " << setw(3) << percent << "%" << endl;
    }
    cout << "----------------------------------------------------------------\n";
    
    return 0;
}