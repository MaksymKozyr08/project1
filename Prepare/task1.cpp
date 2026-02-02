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

typedef long long ll ;
typedef long double ld;
using namespace std;


void summary(ll n,ll k,ll leftcordon,vector<ll>& a){
    if(k==0){
        for(ll i:a)cout<<i<<" ";
        cout<<"\n";
        return;
    }
    for( ll i=leftcordon+1;i<=n;++i){
        if(leftcordon==0 || i%leftcordon==0){
            a.push_back(i);
            summary(n, k - 1, i, a);
            a.pop_back();
        }
    }
}

ll factorial( ll n){
    if(n==0)return 1;
    return n* factorial(n-1); 
}

void outout(ll n,ll k, ll cordon, vector<ll> a){
    if(k==0){
        for(ll i:a)cout<<i<<" ";
        cout<<"\n";
        return;
    }

    for(ll i=cordon+1;i<n;++i){
        a.push_back(i);
        outout(n,k-1,i,a);
        a.pop_back();
    }
}

void task28(ll n,ll k,ll parny,ll cordon,vector<ll> a){
    if(k==0){
        if(parny==a.size()/2){
            for(ll i:a)cout<<i<<" ";
            cout<<"\n";
            return;
        }
    }
    
    for(ll i=cordon+1;i<=n;++i){
        a.push_back(i);
        task28(n, k-1,parny+(i%2==0),i,a);
        a.pop_back();
    }
}

void task29(ll n,ll k,ll leftkordon,ll parn,vector<ll>& a){
    if(k==0){
        if(parn>=(a.size()+1)/2){
            for(ll i:a)cout<<i<<" ";
            cout<<"\n";
            return;
        }
    }
    for(ll i=leftkordon+1;i<=n;++i){
        a.push_back(i);
        task29(n,k-1,i,parn+(i%2==0),a);
        a.pop_back();
    }
}

void moveleft(vector<ll>& a){
    ll b=a[0];
    for( ll i=0;i<a.size()-1;++i){
        a[i]=a[i+1];
    }
    a[a.size()-1]=b;
    for(ll i:a)cout<<i<<" ";
    cout<<endl;
}

void moveright(vector<ll>& a){
    ll b=a[a.size()-1];
    for( ll i=a.size()-1;i>0;i--){
        a[i]=a[i-1];
    }
    a[0]=b;
    for(ll i:a)cout<<i<<" ";
    cout<<endl;
}

void task30(ll n,ll k,vector<ll>& a,vector<bool>& b){
    if(a.size()==n){
        for(ll i:a)cout<<i<<" ";
        cout<<"\n";
        return;
    }

    for(ll i=1;i<=n;++i){
        if(b[i])continue;

        if(a.empty() || abs(a.back() - i) <= k){
            a.push_back(i);
            b[i]=true;
            task30(n,k,a,b);
            a.pop_back();
            b[i]=false;
        }
    }
}

ll sumrum(string s){
    vector<ll> a;
    ll sum=0;
    for(ll i=0;i<s.size();++i){
        if(s[i]=='I'){
            a.push_back(1);
        }
        else if(s[i]=='V'){
            a.push_back(5);
        }
        else if(s[i]=='X'){
            a.push_back(10);
        }
        else if(s[i]=='L'){
            a.push_back(50);
        }
        else if(s[i]=='C'){
            a.push_back(100);
        }
        else if(s[i]=='D'){
            a.push_back(500);
        }
        else if(s[i]=='M'){
            a.push_back(1000);
        }
    }
    for(ll i:a)cout<<i<<" ";
    cout<<"\n";
    for(ll i=1;i<a.size();++i){
        if(a[i]>a[i-1]){
            sum=sum+a[i]-a[i-1];
            cout<<"1:"<<sum<<endl;
        }
        else if(i==1){
            sum+=a[0];
        }
        else{
            sum+=a[i];
            cout<<"2:"<<sum<<endl;
        }
    }
    return sum;
}
int main(){
    /*ll n=0,k=0;
    cin>>n;
    cin>>k;
    vector<ll> a;
    summary(n,k,0,a);
    cout<<"done";
    cout<<"\n";
    cin>>n;
    cout<<factorial(n)<<endl;
    cout<<"done";
    cin>>n;
    cin>>k;
    vector<ll> a;
    outout(n,k,0,a);
    cin>>n;
    cin>>k;
    vector<ll> a;
    task28(n,k,0,0,a);
    cin>>n;
    cin>>k;
    vector<ll> a;
    task28(n,k,0,0,a);
    cin>>n;
    vector<ll> a(n);
    for(ll i=0;i<n;++i){
        a[i]=rand()%100;
    }
    for(ll i:a)cout<<i<<" ";
    cout<<endl;
    moveright(a);
    ll n, k;
    if (cin >> n >> k) {
        vector<ll> path;
        vector<bool> used(n + 1, false);
        task30(n, k, path, used);
    }
    cout<<"done";*/
    string s;
    cin>>s;
    cout<<sumrum(s);
    return 0;
}