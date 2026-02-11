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
ll permutation(vector<ll>& a,ll val){
    ll k=0;
    for(ll i=0;i<a.size();++i){
        if(a[i]!=val){
            a[k]=a[i];
            k++;
        }
    }
    return k;
}

int main(){
    ll n;
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    ll val=0;
    cin>>val;
    ll k=permutation(a,val);
    cout<<k;
    cout<<"\n";
    for(ll i=0;i<n;++i){
        cout<<a[i]<<" ";
    }
    return 0;
}