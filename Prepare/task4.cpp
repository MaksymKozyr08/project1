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
    stack<char> st;
    for (int i = 0; i < s.size(); ++i) {
        if (s[i] == '(' || s[i] == '{' || s[i] == '[') {
            st.push(s[i]);
        } else {
            if (st.empty()) return false;
            char top = st.top();
            if ((s[i] == ')' && top == '(') || 
                (s[i] == '}' && top == '{') || 
                (s[i] == ']' && top == '[')) {
                st.pop();
            } else {
                return false;
            }
        }
    }
    return st.empty();
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