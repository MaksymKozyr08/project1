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
typedef long double ld;

using namespace std;
bool check(string s){
    ll sum1=0;
    ll sum2=0;
    ll sum3=0;
    for(ll i=0;i<s.size();++i){
        if(s[i]=='[' && sum1!=0){
            return false;
        }
        if(s[i]=='{' && sum2!=0){
            return false;
        }
        if(s[i]=='(' && sum2!=0){
            return false;
        }
        if(s[i]=='(')sum1++;
        if(s[i]=='{')sum1++;
        if(s[i]=='[')sum3++;
        if(s[i]=='}')sum1--;
        if(s[i]==']')sum2--;
        if(s[i]==')')sum3--;
    }
    if((sum1+sum2+sum3)!=0)return false;
    return true;
}
int main(){
    string s;
    cin>>s;
    if(check(s))cout<<"true";
    else{
        cout<<"false";
    }
    return 0;
}