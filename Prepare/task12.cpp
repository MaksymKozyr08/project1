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
string summary(string a,string b){
    string result(max(a.size(),b.size()),'0');
    if(a.empty()&&b.empty())return "0";
    ll sum=0;
    for(ll i=0;i<result.size();i++){
        if(i<a.size())sum+=(a[a.size()-1-i]-'0');
        if(i<b.size())sum+=(b[b.size()-1-i]-'0');
        result[result.size()-1-i]=(char)((sum%2)+'0');
        sum/=2;
    }
    if(sum){
        result.insert(result.begin(),'1');
    }
    return result;
}
int main(){
    string s1,s2;
    cin>>s1;
    cin>>s2;
    string result=summary(s1,s2);
    cout<<result;
    return 0;
}