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
ll mySqrt(ll x){
    if(x==0){
        return 0;
    }
    ll leftcordon=0;
    ll rightcordon=x;
    ll mid=rightcordon/2;
    while(leftcordon<=rightcordon){
        if(mid*mid==x)return mid;
        else if(mid*mid<x){
            leftcordon=mid+1;
        }
        else if(mid*mid>x){
            rightcordon=mid-1;
        }
        mid=leftcordon+(rightcordon-leftcordon)/2;
    }
    return rightcordon;
}
int main(){
    int x;
    cin>>x;
    cout<<mySqrt(x);
    return 0;
}