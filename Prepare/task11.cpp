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

vector<ll> permutation(vector<ll>& a){
    for(ll i=a.size();i>=0;i--){
        if(a[i]<9){
            a[i]++;
            return a;
        }
        a[i]=0;
    }
    a.insert(a.begin(),1);
    return a;
}

int main(){
    ll n;
    cin>>n;
    vector<ll> a;
    permutation(a);
    for(ll i:a)cout<<i<<" ";
    return 0;
}