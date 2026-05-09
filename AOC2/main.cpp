#include <iostream>
#include <stdio.h>
#include <stdint.h>

using namespace std;

uint16_t prog[] = {
    0x2217,  
    0x2417, 
    
    0x56E0, 
    
    0x1260, 
    0x0803, 
    
    0x14A0, 
    0x0805, 
    0x0E06, 
    
    0x14A0,
    0x0609, 
    0x0E03,
    
    0x0000, 
    
    0x96FF,
    0x0E05, 
    
    0x9ABF, 
    0x1B61,  
    0x1A45, 
    0x0601,
    0x96FF, 
    
    0x9ABF, 
    0x1B61, 
    0x1045, 
    
    0xF027, 
    0xF025, 
    
    0x0018,//A
    0x0020 //B
};

int main() {
    FILE *f = fopen("sum.obj", "wb");
    if (!f) {
        cout << "Error!" << endl;
        return 1;
    }
    
    fwrite(prog, sizeof(prog), 1, f);
    fclose(f);
    
    cout << "success" << endl;
    return 0;
}