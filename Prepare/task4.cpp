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
bool check(string s) {
    stack<char> sq;
    for(ll i=0;i<s.size();++i){
        if(s[i]=='(' || s[i]=='[' || s[i]=='{')sq.push(s[i]);
        else{
            if(sq.empty())return false;
            if(s[i]==')' && sq.top()=='(')sq.pop();
            if(s[i]==']' && sq.top()=='[')sq.pop();
            if(s[i]=='}' && sq.top()=='{')sq.pop();
            else{
                return false;
            }
        }
    }
    if(sq.empty())return true;
    return false;
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