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
using namespace std;

void summary(ll n, ll k, ll leftcordon, vector<ll>& a){
    if(k==0){
        for(ll i:a)cout<<i<<" ";
        cout<<"\n";
        return;
    }
    ll start = (leftcordon == 0) ? 1 : leftcordon + 1;
    for(ll i=start; i<=n;++i){
        if(leftcordon==0 || i%leftcordon==0){
            a.push_back(i);
            summary(n,k-1,i,a);
            a.pop_back();
        }
    }
}
int main(){
    ll n=0,k=0;
    cin>>n;
    cin>>k;
    vector<ll> fun;
    summary(n,k,0,fun);
    cout<<"well done";
    return 0;
}
