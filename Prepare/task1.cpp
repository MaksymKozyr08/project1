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

typedef long long ll ;
typedef long double ld;
using namespace std;
void summary(ll n,ll k,ll leftcordon,vector<ll>& a){
    if(k==0){
        for(ll i:a)cout<<i<<" ";
        cout<<"\n";
        return;
    }
    for( ll i=leftcordon+1;i<=n;++i){
        if(leftcordon==0 || i%leftcordon==0){
            a.push_back(i);
            summary(n, k - 1, i, a);
            a.pop_back();
        }
    }
}

ll factorial( ll n){
    if(n==0)return 1;
    return n* factorial(n-1); 
}

int main(){
    ll n=0,k=0;
    cin>>n;
    cin>>k;
    vector<ll> a;
    summary(n,k,0,a);
    cout<<"done";
    cout<<"\n";
    cin>>n;
    cout<<factorial(n)<<endl;
    cout<<"done";
    return 0;
}