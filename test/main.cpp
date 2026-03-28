#include <cmath>
#include <fstream>
#include <iostream>
#include "IEEE_format.hpp"

IEEE_format stack[8];
int top = -1;

void LOAD(double value) {
    if (top < 7) {
        stack[++top] = toIEEE(value);
    } else {
        std::cout<<("Stack Overflow!")<< std::endl;
    }
}

double STORE() {
    if (top >= 0) {
        return fromIEEE(stack[top--]);
    }
    std::cout<<("Stack is empty!")<< std::endl;
    return 0.0;
}

void ADD() {
    if (top < 1) {
        std::cout<<"There are no 2 elements"<<std::endl;
        return;
    }
    double b = fromIEEE(stack[top--]);
    double a = fromIEEE(stack[top]);
    stack[top] = toIEEE(a + b);
}

void SUB() {
    if (top < 1) return;
    double b = fromIEEE(stack[top--]);
    double a = fromIEEE(stack[top]);
    stack[top] = toIEEE(a - b);
}

void MULT() {
    if (top < 1) return;
    double b = fromIEEE(stack[top--]);
    double a = fromIEEE(stack[top]);
    stack[top] = toIEEE(a * b);
}

void DIV() {
    if (top < 1) return;
    double b = fromIEEE(stack[top--]);
    double a = fromIEEE(stack[top]);
    if (b != 0) {
        stack[top] = toIEEE(a / b);
    } else if (a==0 && b==0) {
        std::cout<<("Division zero by zero")<<std::endl;
        stack[top] = toIEEE(NAN);
    } else {
        std::cout<<("Division by zero!")<<std::endl;
        stack[top] = (a>0) ? toIEEE(INFINITY) : toIEEE(-INFINITY);
    }
}

void DUBL() {
    if (top >= 0 && top < 7) {
        stack[top + 1] = stack[top];
        top++;
    } else {
        std::cout<<"Error"<< std::endl;
    }
}

void SWAP() {
    if (top >= 1) {
        IEEE_format temp = stack[top];
        stack[top] = stack[top - 1];
        stack[top - 1] = temp;
    } else {
        std::cout<<"Error"<<std::endl;
    }
}

void print_bits(unsigned long long value, int count) {
    for (int i = count - 1; i >= 0; i--) {
        std::cout << ((value >> i) & 1);
    }
}

void show_stack() {
    if (top == -1) {
        std::cout << "Stack is empty" << std::endl;
        return;
    }
    int i;
    for (i = top; i >= 0; i--) {

        std::cout << "[" << 7+i-top << "] | ";

        print_bits(stack[i].bits.sign, 1);
        std::cout << " | ";

        print_bits(stack[i].bits.characteristics, 12);
        std::cout << " | ";

        print_bits(stack[i].bits.mantissa, 29);

        if (std::isnan(fromIEEE(stack[i]))) std::cout << " | NaN";
        else if (std::isinf(fromIEEE(stack[i]))) std::cout << " | Infinity";
        else std::cout<<" | Double: "<< fromIEEE(stack[i]);
        std::cout<< std::endl;
    }
    for (int j=7+i-top; j>=0; j--) {
        std::cout << "[" << j << "] | ";
        std::cout << "- | ------------ | ----------------------------- | Empty"<<std::endl;
    }
    std::cout << std::endl;
}

int main() {
    std::ifstream file("Commands.txt");
    if (!file.is_open()) {
        std::cout << "Can`t open file!" << std::endl;
        return 0;
    }

    std::string command;
    double val;

    while (file >> command) {
        if (command == "LOAD") {
            file >> val;
            LOAD(val);
            std::cout<<"Load "<<val<<std::endl;
        }
        else if (command == "ADD") {
            ADD();
            std::cout<<"Add "<<std::endl;
        }
        else if (command == "SUB") {
            SUB();
            std::cout<<"Sub "<<std::endl;
        }
        else if (command == "MULT") {
            MULT();
            std::cout<<"Mult "<<std::endl;
        }
        else if (command == "DIV") {
            DIV();
            std::cout<<"Div "<<std::endl;
        }
        else if (command == "DUBL") {
            DUBL();
            std::cout<<"Dubl "<<std::endl;
        }
        else if (command == "SWAP") {
            SWAP();
            std::cout<<"Swap "<<std::endl;
        }
        else if (command == "STORE") {
            double res = STORE();
            std::cout << "Get from store: " << res << std::endl;
        }

        show_stack();
    }

    file.close();
}