#include <iostream>
#include <istream>
#include <vector>
using namespace std;

typedef long long ll ;
typedef long double ld;

void print(vector<ll>& a){
    for(ll i:a)cout<<i<<" ";
    cout<<"\n";
}
void bubble_sort(vector<ll>& a){
    for(ll i=0;i<a.size()-1;++i){
        for(ll j=0;j<a.size()-i-1;++j){
            if(a[j]>a[j+1]){
                ll c=a[j];
                a[j]=a[j+1];
                a[j+1]=c;
            }
        }
        print(a);
    }
}
int main(){
    vector<ll> a(10);
    for(ll i=0;i<10;++i){
        a[i]=rand()%100;
    }
    print(a);
    bubble_sort(a);
    print(a);
    return 0;
}