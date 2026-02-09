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

vector<ll> exchenge(vector<ll>& a){
    ll k = 0;
    for (ll i = 1; i < (ll)a.size(); ++i) {
        if (a[i - 1] == a[i]) {
            a[k] = a[i];
            k++;
        }
    }
    a.resize(k);
    return a;
}
int main(){
    ll n;
    cin>>n;
    vector<ll> a(n);
    ll k=(rand()%10)+1;
    for(ll i=0;i<n;++i){
        if(i%2==0)a[i]=k;
        else{
            a[i]=rand()%10;
        }
    }
    for(ll i:a)cout<<i<<" ";
    cout<<"\n";
    vector<ll> result = exchenge(a);
    for(ll i : result) cout << i << " ";
    cout << "\n";
    return 0;
}