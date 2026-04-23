#include <iostream>
#include <stdint.h>
#include <stdio.h>

using namespace std;

uint16_t prog[] = {0x2207, 0x2407,

                   0x94BF, 0x14A1,

                   0x1642,

                   0x10E0, 0xF027, 0xF025,

                   0x0012, 0x0020};

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