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
    string result(max(a.size(), b.size())-1, '0');
    if(result.size()==0)return "";
    ll k=0;
    for(ll i=max(a.size(),b.size());i>=0;i--){
        if((a[i]+b[i]+k)>1){
            result[i]='0';
            k++;
        }
        else{
            result[i]=char(a[i]+b[i]+k);
            k--;
        }
    }
    if(k!=0){
        result.insert(result.begin(), '1');
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