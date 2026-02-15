#include <iostream>
#include <ratio>
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
#include <stack>

typedef long long ll;
typedef long double ld;

using namespace std;

ll fib(int n){
    ll x=1;
    ll y=1;
    ll w=0;
    if(n==1)return 1;
    for(size_t i=0;i<n-1;++i){
        w=x+y;
        y=x;
        x=w;
        //cout<<x<<" "<< y<<" "<<w<<"\n";
    }
    return w;
}

int main(){
    ll n;
    cin>>n;
    cout<<fib(n);
    return 0;
}