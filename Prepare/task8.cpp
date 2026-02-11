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
int find(string s,string s1){
    for(ll i=0;i<(s.size()-s1.size());++i){
        if(s[i]==s1[0]){
            for(ll j=0;j<s1.size();++j){
                if(s[i+j]!=s1[j])break;
                if(j==s1.size()-1)return i;
            }
        }
    }
    return -1;
}
int main(){
    string s;
    string s1;
    cin>>s;
    cin>>s1;
    cout<<find(s,s1);
    return 0;
}