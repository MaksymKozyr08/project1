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
void result(vector<ll>& nums1,ll n,vector<ll>& nums2,ll m){
    ll i=m-1;
    ll j=n-1;
    ll k=n+m-1;
    while(j>=0){
        if(i>=0 && nums1[i] > nums2[j]){
            nums1[k--] = nums1[i--];
        }
        else{
            nums1[k--] = nums2[j--];
        }
    }
}
int main(){
    ll n=0,m=0;
    cin>>n;
    cin>>m;
    vector<ll> a(n+m,0);
    vector<ll> b(m);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    for(ll i=0;i<m;++i){
        cin>>b[i];
    }
    result(a,n,b,m);
    return 0;
}