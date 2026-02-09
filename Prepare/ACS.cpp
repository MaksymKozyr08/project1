#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <ctime>
#include <cmath>
#include <algorithm>

using namespace std;

// Кількість прогонів для усереднення (як у твоїх нотатках k=1..10)
const int NUM_TESTS = 10;
// Кількість ітерацій у внутрішньому циклі
const int INNER_ITERATIONS = 1000000;
// Кількість операцій за одну ітерацію (a+b, b+c, a+c) -> 3 операції
const int OPS_PER_ITER = 3;

// Структура для збереження результатів
struct Result {
    string typeName;
    string opName;
    double opsPerSec;
};

// Шаблонна функція для тестування (працює з int, long, double тощо)
template <typename T>
double run_test(char op) {
    double total_ops_per_sec = 0;

    // Змінні оголошуємо volatile, щоб компілятор не викинув "зайвий" код при оптимізації
    volatile T a = 10, b = 20, c = 0; 
    
    // Для ділення беремо інші числа, щоб не ділити на 0 і не зменшувати числа до 0 занадто швидко
    if (op == '/') { a = 10000; b = 2; c = 1; }

    for (int k = 0; k < NUM_TESTS; k++) {
        clock_t t1, t2, t01, t02;

        // 1. Вимірюємо час РОБОЧОГО циклу
        t1 = clock();
        for (int i = 0; i < INNER_ITERATIONS; i++) {
            switch (op) {
                case '+':
                    c = a + b; b = a + c; a = b + c;
                    break;
                case '-':
                    c = a - b; b = a - c; a = b - c;
                    break;
                case '*':
                    // Для множення скидаємо значення, щоб не було переповнення (infinity)
                    c = a * b; b = a * c; a = b * c;
                    if (a > 1000000 || a < -1000000) { a=2; b=3; } 
                    break;
                case '/':
                     // Для ділення простіша логіка, щоб уникнути 0
                    c = a / b; b = c + 2; a = b + 10;
                    break;
            }
        }
        t2 = clock();

        // Відновлюємо значення для чистоти експерименту
        T temp_a = a, temp_b = b, temp_c = c;

        // 2. Вимірюємо час ПОРОЖНЬОГО циклу (тільки присвоєння)
        // Це саме те, що було у твоїх нотатках: c=a; b=c; a=b;
        t01 = clock();
        for (int i = 0; i < INNER_ITERATIONS; i++) {
            c = temp_a; temp_b = c; temp_a = temp_b;
        }
        t02 = clock();

        // 3. Розрахунок чистого часу
        double work_time = (double)(t2 - t1) / CLOCKS_PER_SEC;
        double empty_time = (double)(t02 - t01) / CLOCKS_PER_SEC;
        
        double pure_time = work_time - empty_time;

        // Захист від дуже малих значень (якщо empty_time > work_time через похибку таймера)
        if (pure_time <= 0) pure_time = 0.000001;

        double current_d = (double)(INNER_ITERATIONS * OPS_PER_ITER) / pure_time;
        total_ops_per_sec += current_d;
    }

    return total_ops_per_sec / NUM_TESTS; // Повертаємо середнє
}

int main() {
    vector<Result> results;
    
    cout << "Performing calculations. Please wait..." << endl;

    // --- ТЕСТУВАННЯ ---
    // Тут ти можеш додати або прибрати типи даних відповідно до твого варіанту
    
    // INT
    results.push_back({"int", "+", run_test<int>('+')});
    results.push_back({"int", "-", run_test<int>('-')});
    results.push_back({"int", "*", run_test<int>('*')});
    results.push_back({"int", "/", run_test<int>('/')});

    // LONG
    results.push_back({"long", "+", run_test<long>('+')});
    results.push_back({"long", "-", run_test<long>('-')});
    results.push_back({"long", "*", run_test<long>('*')});
    results.push_back({"long", "/", run_test<long>('/')});

    // FLOAT
    results.push_back({"float", "+", run_test<float>('+')});
    results.push_back({"float", "-", run_test<float>('-')});
    results.push_back({"float", "*", run_test<float>('*')});
    results.push_back({"float", "/", run_test<float>('/')});

    // DOUBLE
    results.push_back({"double", "+", run_test<double>('+')});
    results.push_back({"double", "-", run_test<double>('-')});
    results.push_back({"double", "*", run_test<double>('*')});
    results.push_back({"double", "/", run_test<double>('/')});


    // --- ВІДОБРАЖЕННЯ РЕЗУЛЬТАТІВ ---
    
    // Знаходимо максимальну швидкість для розрахунку відсотків (це буде 100%)
    double max_speed = 0;
    for (const auto& r : results) {
        if (r.opsPerSec > max_speed) max_speed = r.opsPerSec;
    }

    cout << "\n--------------------------------------------------------------------------------------\n";
    cout << setw(8) << "Type" << setw(5) << "Op" << setw(15) << "Ops/Sec" << "   " << "Diagram\n";
    cout << "--------------------------------------------------------------------------------------\n";

    for (const auto& r : results) {
        // Розрахунок відсотків
        int percent = (int)((r.opsPerSec / max_speed) * 100);
        
        // Малюємо діаграму (максимальна довжина - 40 символів 'X')
        int bar_length = (int)((r.opsPerSec / max_speed) * 40);
        string bar(bar_length, 'X');

        cout << setw(8) << r.typeName 
             << setw(5) << r.opName 
             << setw(15) << scientific << setprecision(2) << r.opsPerSec 
             << "   " << left << setw(42) << bar 
             << right << setw(4) << percent << "%" << endl;
    }
    cout << "--------------------------------------------------------------------------------------\n";

    return 0;
}