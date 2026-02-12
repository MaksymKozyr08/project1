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
typedef long  long ld;

using namespace std;

vector<ll> Hornersmethod(vector<ll>& a, ll x0){
    vector<ll> res;
    for(ll i:res)cout<<i<<" ";
    return res;
}
int main(){
    ll n;
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    ll x0;
    cin>>x0;
    vector<ll> res=Hornersmethod(a,x0);
    return 0;
}