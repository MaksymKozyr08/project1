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
    for(size_t i=0;i<a.size();++i){
        
        

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