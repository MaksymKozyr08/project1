#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <cstdint>

using namespace std;

typedef long long ll;
typedef long double ld;

struct bits_12_19{
    uint32_t m:19;
    uint32_t e:12;
    uint32_t s:1;
};

union CFloat{
    uint32_t raw;
    bits_12_19 b;
};

vector<CFloat> st;

CFloat to_cstm(ld v){
    CFloat r;
    r.raw=0;
    if(isnan(v)){
        r.b.e=4095;
        r.b.m=1;
        return r;
    }
    if(isinf(v)){
        r.b.e=4095;
        r.b.s=(v<0)?1:0;
        return r;
    }
    if(v==0.0){
        r.b.s=signbit(v)?1:0;
        return r;
    }
    
    r.b.s=(v<0)?1:0;
    v=fabsl(v);
    
    int exp_i;
    ld mant=frexpl(v, &exp_i);
    
    mant*=2.0;
    exp_i-=1;
    
    ll nx=exp_i+2047;
    
    if(nx<=0){
        r.b.e=0;
        r.b.m=(uint32_t)(mant*pow(2, 18+nx));
    }else if(nx>=4095){
        r.b.e=4095;
        r.b.m=0;
    }else{
        r.b.e=nx;
        r.b.m=(uint32_t)((mant-1.0)*524288);
    }
    return r;
}

ld to_dbl(CFloat v){
    if(v.b.e==4095){
        if(v.b.m!=0)return NAN;
        return(v.b.s==1)?-INFINITY:INFINITY;
    }
    if(v.b.e==0&&v.b.m==0){
        return(v.b.s==1)?-0.0:0.0;
    }
    
    ld res;
    if(v.b.e==0){
        res=(ld)v.b.m/524288.0;
        res=ldexpl(res, -2046);
    }else{
        res=1.0+(ld)v.b.m/524288.0;
        res=ldexpl(res, (int)v.b.e-2047);
    }
    
    if(v.b.s)res=-res;
    return res;
}

void p_b(uint64_t v,ll c){
    for(ll i=c-1;i>=0;--i)cout<<((v>>i)&1);
}

void show(){
    if(st.empty()){
        cout<<"Stack is empty\n\n";
        return;
    }
    for(ll i=st.size()-1;i>=0;--i){
        cout<<"["<<st.size()-1-i<<"] | ";
        p_b(st[i].b.s,1);cout<<" | ";
        p_b(st[i].b.e,12);cout<<" | ";
        p_b(st[i].b.m,19);
        ld val=to_dbl(st[i]);
        if(isnan(val))cout<<" | NaN\n";
        else if(isinf(val))cout<<" | Infinity\n";
        else cout<<" | Double: "<<setprecision(15)<<(double)val<<"\n";
    }
    for(ll j=st.size();j<=7;++j){
        cout<<"["<<j<<"] | - | ------------ | ------------------- | Empty\n";
    }
    cout<<"\n";
}

void std_f(){
    ld a[]={1e-300L,1e300L,-1e300L,1.0L,INFINITY,-INFINITY,NAN};
    for(ll i=0;i<7;++i){
        CFloat f=to_cstm(a[i]);
        p_b(f.b.s,1);cout<<" ";
        p_b(f.b.e,12);cout<<" ";
        p_b(f.b.m,19);
        cout<<" -> "<<(double)to_dbl(f)<<"\n";
    }
    cout<<"\n";
}

void push_f(ld v){
    if(st.size()<8)st.push_back(to_cstm(v));
    else cout<<"Stack Overflow!\n";
}

ld pop_f(){
    if(!st.empty()){
        ld r=to_dbl(st.back());
        st.pop_back();
        return r;
    }
    cout<<"Stack is empty!\n";
    return 0.0;
}

int main(){
    std_f();
    ifstream f("Commands.txt");
    if(!f.is_open()){
        cout<<"Can`t open file!\n";
        return 0;
    }
    string s;
    ld v;
    while(f>>s){
        if(s=="LOAD"){
            f>>v;
            push_f(v);
            cout<<"Load "<<(double)v<<"\n";
        }else if(s=="ADD"){
            if(st.size()>1){
                ld b=pop_f();
                ld a=pop_f();
                push_f(a+b);
            }
            cout<<"Add\n";
        }else if(s=="SUB"){
            if(st.size()>1){
                ld b=pop_f();
                ld a=pop_f();
                push_f(a-b);
            }
            cout<<"Sub\n";
        }else if(s=="MULT"){
            if(st.size()>1){
                ld b=pop_f();
                ld a=pop_f();
                push_f(a*b);
            }
            cout<<"Mult\n";
        }else if(s=="DIV"){
            if(st.size()>1){
                ld b=pop_f();
                ld a=pop_f();
                if(b!=0){
                    push_f(a/b);
                }else if(a==0&&b==0){
                    cout<<"Division zero by zero\n";
                    push_f(NAN);
                }else{
                    cout<<"Division by zero!\n";
                    push_f((a>0)?INFINITY:-INFINITY);
                }
            }
            cout<<"Div\n";
        }else if(s=="STORE"){
            ld r=pop_f();
            cout<<"Get from store: "<<(double)r<<"\n";
        }
        show();
    }
    f.close();
    return 0;
}