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
using namespace std;

vector<ll> exchenge(vector<ll> a){
    ll k=0;
    for(ll i=1;i<a.size();++i){
        if(a[i-1]==a[i]){
            a[k]=a[i];
            k++;
        }
    }
    return a;
}
int main(){
    ll n;
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        a[i]=rand()%5;
    }
    return 0;
}