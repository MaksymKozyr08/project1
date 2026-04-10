#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

typedef long long ll;
using namespace std;
void print_fun(stack<char> s){
    while(!s.empty()){
        cout<<s.top();
        s.pop();
    }
    cout<<endl;
}
int main(){
    string s;
    cin>>s;
    stack<char> st;
    for(size_t i=0;i<s.size();++i){
        if(s[i]=='{' || s[i]=='(' || s[i]=='[')st.push(s[i]);
        else if(st.empty() && (s[i]==']' || s[i]==')' || s[i]=='}'))break;
        else if(!st.empty()){
            if(s[i]=='}' && st.top()=='{'){
                st.pop();
                print_fun(st);
            }
            else if(s[i]==')' && st.top()=='('){
                st.pop();
                print_fun(st);
            }
            else if(s[i]==']' && st.top()=='['){
                st.pop();
                print_fun(st);
            }
        }
    }    
    if(st.empty())cout<<"corect";
    else{cout<<"incorect";}
    return 0;
}