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


ll sorting(vector<ll> nums,ll target){
    ll 
    left=0,
    right=nums.size()-1,
    mid;

    if(nums.empty())return -1;
    while(left<=right){
        mid=left+((right-left)/2);
        if(nums[mid]==target)return mid;
        else if(target<nums[mid]){
            right=mid-1;
        }
        else{
            left=mid+1;
        }
    }
    return left;
}

ll lastword(string s){
    ll k=0;
    for(size_t i=s.length()-1;i>=0;i--){
        if(s[i]!=' ')k++;
        if(s[i]==' ' && k!=0)return k;
    }
    return k;
}
int main(){
    /*
    ll n;
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    ll x0;
    cin>>x0;
    vector<ll> res=Hornersmethod(a,x0);
    */
    ll n=0;
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    ll target=0;
    cin>>target;
    cout<<sorting(a,target);
    return 0;
}