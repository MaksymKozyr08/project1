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

vector<ll> Hornersmethod(vector<ll>& a, ll x0){
    vector<ll> res(a.size());

    if(a.empty()){
        return res;
    }
    res[0]=a[0];
    for(ll i=1;i<static_cast<ll>(a.size());++i){
        res[i]=x0*res[i-1]+a[i];
    }
    for(ll i:res)cout<<i<<" ";
    return res;
}


ll sorting(vector<ll> a,ll target){
    unsigned left=0, right=a.size(),mid;
    if(a.empty())return 0;
    while(left<right){
        mid=left+((right-left)/2);
        if(target<mid){
            right=mid-1;
        }
        else{
            left=mid+1;
        }
    }
    return left;
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