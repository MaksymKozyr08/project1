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

typedef long long ll;
typedef long double ld;

using namespace std;


int main(){
    ll n;
    cin>>n;
    vector<string> a;
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    for(ll i:a)cout<<i<<" ";
    cout<<"\n";
    cout<<prefix(a);
    return 0;
}