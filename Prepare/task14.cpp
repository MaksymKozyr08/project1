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
int mySqrt(int x){
    if(x==0)return 0;
    ll l=1,r=x,ans=0;
    while(l<=r){
        ll mid=l+(r-l)/2;
        if(mid*mid<=x){
            ans=mid;
            l=mid+1;
        }
        else{
            r=mid-1;
        }
    }
    return ans;
}
int main(){
    int x;
    cin>>x;
    cout<<mySqrt(x);
    return 0;
}