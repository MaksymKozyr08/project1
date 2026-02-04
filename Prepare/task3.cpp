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

string prefix(vector<string>& a){
    string s=a[0];
    if(a.empty())return "";
    while(s.size()>0){
        for(ll i=1;i<a.size();++i){
            if(a[i].substr(0,s.size())!=s){
                s.pop_back();
            }
        }
        return s;
    }
    return "";
}

int main(){
    ll n;
    cin >> n;
    vector<string> a(n);
    for (ll i = 0; i < n; ++i) {
        cin >> a[i];
    }
    for(string i:a)cout<<i<<" ";
    cout<<"\n";
    cout<<prefix(a);
    return 0;
}