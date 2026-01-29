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

void sumary(ll n, ll k, ll last, vector<ll>& a) {
    if (k == 0) {
        if (n == 0) {
            for (ll x : a) cout << x << " ";
            cout << "\n";
        }
        return;
    }
    for(ll i=last+1;i<=n;++i){
        a.push_back(i);
        sumary(n - i, k - 1, i, a);
        a.pop_back();
    }
}


int main(){
    ll n=0,k=0;
    cin>>n;
    cin>>k;
    vector<ll> fun;
    sumary(n,k,0,fun);
    return 0;
}
