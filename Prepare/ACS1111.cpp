#include <cstdint>
#include <iostream>

// S: State space initialization
uint16_t M[65536] = {0};
int16_t R[8] = {0};
uint16_t PC = 0x3000;
bool HALT = false;

// Isomorphic mapping of the algebraic modulo sequence onto the memory topology
void initialize_instruction_matrix() {
    // Initial vectors: a = 17, b = 5
    R[0] = 17; 
    R[1] = 5;  

    // Instruction set operators 
    M[0x3000] = 0x947F; // R2 <- ~R1 (Bitwise complement)
    M[0x3001] = 0x14A1; // R2 <- R2 + 1 (Two's complement additive inverse)
    M[0x3002] = 0x1002; // R0 <- R0 + R2 (Monotonic subtraction)
    M[0x3003] = 0x0801; // Branch PC <- PC + 1 if Negative flag = 1
    M[0x3004] = 0x0FFD; // Branch PC <- PC - 3 unconditionally
    M[0x3005] = 0x1001; // R0 <- R0 + R1 (Basis restoration)
    M[0x3006] = 0xF025; // Terminal state (HALT)
}

// Evaluation of the transition function delta
void execute_automaton() {
    while (!HALT) {
        uint16_t op = M[PC++];
        uint16_t opcode = op >> 12;
        
        if (opcode == 0x9) { 
            // NOT operation
            R[(op >> 9) & 7] = ~R[(op >> 6) & 7];
        } 
        else if (opcode == 0x1) { 
            // ADD operation
            if ((op >> 5) & 1) { 
                int16_t imm = op & 0x1F;
                if (imm & 0x10) imm |= 0xFFE0; 
                R[(op >> 9) & 7] = R[(op >> 6) & 7] + imm;
            } else { 
                R[(op >> 9) & 7] = R[(op >> 6) & 7] + R[op & 7];
            }
        }
        else if (opcode == 0x0) { 
            // Branch operation
            bool n = R[0] < 0; 
            bool z = R[0] == 0;
            bool p = R[0] > 0;
            bool branch = (((op >> 11) & 1) && n) || 
                          (((op >> 10) & 1) && z) || 
                          (((op >> 9) & 1) && p);
            if (branch) {
                int16_t offset = op & 0x1FF;
                if (offset & 0x100) offset |= 0xFE00;
                PC += offset;
            }
        }
        else if (opcode == 0xF) { 
            // TRAP operation
            if ((op & 0xFF) == 0x25) HALT = true;
        }
    }
}

int main() {
    initialize_instruction_matrix();
    execute_automaton();
    
    // The scalar r converges in R[0]
    std::cout << "r = " << R[0] << "\n"; 
    return 0;
}