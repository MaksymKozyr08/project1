#include <iostream>
#include <vector>
#include <string>
using namespace std;


typedef long long ll ;
typedef long double ld;

string prefix(const vector<string>& a) {
    if (a.empty()) return "";
    string s = a[0];
    for (size_t i = 1; i < a.size(); ++i) {
        size_t j = 0;
        while (j < s.size() && j < a[i].size() && s[j] == a[i][j]) {
            ++j;
        }
        s = s.substr(0, j);
        if (s.empty()) break;
    }
    return s;
}

int main() {
    ll n;
    cin >> n;
    vector<string> s(n);
    for (ll i = 0; i < n; ++i) {
        cin >> s[i];
    }
    cout << prefix(s) << endl;
    return 0;
}