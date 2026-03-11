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
void insertionsort(vector<ll>& a){
    if(a.size()<2)return;
    for(size_t i=1;i<a.size();++i){
        ll key=a[i];
        size_t j=i;
        while(j>0 && a[j-1]>key){
            a[j]=a[j-1];
            --j;
        }
        a[j]=key;
    }
}
int main(){
    vector<ll> a(10);
    for(ll i=0;i<10;++i){
        a[i]=rand()%100;
    }
    print(a);
    insertionsort(a);
    print(a);
    return 0;
}