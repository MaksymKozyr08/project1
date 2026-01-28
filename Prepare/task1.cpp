#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cstdio>
#include <cstring>
#include <cctype>
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <cstdarg>

typedef long long ll;
using namespace std;

ll factorial(ll n){
    if(n==0 || n==1)return 1;
    else{
        return n*factorial(n-1);
    }
}
int main(){
    ll n;
    cin>>n;
    int x=10;
    int* p=&x;
    int y=*p;
    *p=20;
    cout<<*p;
    return 0;
}
