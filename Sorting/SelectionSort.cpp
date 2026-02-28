#include <cstddef>
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
void selectionsort(vector<ll>& a){
    for(size_t i=0;i<a.size();++i){
        size_t min_element=i;
        for(size_t j=i+1;j<a.size();++j){
            if(a[j]<a[min_element])min_element=j;
        }
        ll k=a[i];
        a[i]=a[min_element];
        a[min_element]=k;
    }
}

int main(){
    vector<ll> a(10);
    for(ll i=0;i<10;++i){
        a[i]=rand()%100;
    }
    print(a);
    selectionsort(a);
    print(a);
    return 0;
}