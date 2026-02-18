#include <iostream>
#include <ratio>
#include <type_traits>
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

typedef long long ll ;
typedef long double ld;

using namespace std;
ll result(vector<ll>& a){
    ll min_price=INT64_MAX;
    ll max_profit=0;

    for(ll i=0;i<a.size();++i){
        if(a[i]<min_price)min_price=a[i];
        else if(a[i]-min_price>max_profit)max_profit=a[i]-min_price;
    }
    return max_profit;
}
int main(){
    ll n;
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        cin>>a[i];
    }
    cout<<result(a);
    return 0;
}