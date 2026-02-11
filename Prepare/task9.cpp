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
ll find(vector<ll>& a, ll fin){
    for(ll i=0;i<a.size();++i){
        if(a[i]==fin)return i;
    }
    return -1;
}
int main(){
    ll n=0;
    cin>>n;
    ll fin=0;
    cin>>fin;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    cout<<find(a,fin);
    return 0;
}