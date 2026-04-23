#include <iostream>
#include <stdio.h>
#include <stdint.h>

using namespace std;

uint16_t prog[] = {
    0x220E, // LD R1, A (18)
    0x240E, // LD R2, B (32)
    
    0x94BF, // NOT R2
    0x14A1, // ADD R2, R2, 1 
    0x1642, // R3 = R1 + R2 (-14)

    // Перевірка на мінус
    0x0704, // BRn (якщо від'ємне, стрибай на 4 рядки вперед)
    0x0E05, // BRnzp (інакше просто стрибай до виводу)

    // Блок виводу мінуса
    0x5020, // AND R0, R0, 0 (обнулили R0)
    0x102D, // ADD R0, R0, #45 (код символу '-')
    0xF021, // TRAP 0x21 (вивід символу '-')
    
    // Робимо число додатним для виводу
    0x96FF, // NOT R3
    0x16E1, // ADD R3, R3, 1

    // Фінальний вивід числа
    0x10E0, // R0 = R3
    0xF027, // Вивід числа (беззнаковий, бо ми вже зробили його додатним)
    0xF025, // HALT
    
    0x0012, // A (18)
    0x0020  // B (32)
};

int main() {
    FILE *f = fopen("sum.obj", "wb");
    if (!f) {
        cout << "Error!" << endl;
        return 1;
    }
    
    // запис у файл
    fwrite(prog, sizeof(prog), 1, f);
    
    cout << "success" << endl;
    // cout << "Розмір масиву: " << sizeof(prog) << " байт" << endl;
    
    fclose(f);
    return 0;
}