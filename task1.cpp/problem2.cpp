#include <cstdio>
#include <cstdlib>

struct Polar{double r,phi;};

void create(int N){
    FILE* f=fopen("polar.bin","wb");
    if(!f)return;
    for(int i=0;i<N;i++){
        Polar p;
        p.r=(rand()%20)+1;
        p.phi=(rand()%360);
        fwrite(&p,sizeof(Polar),1,f);
    }
    fclose(f);
}

void process(){
    FILE* f=fopen("polar.bin","rb");
    if(!f)return;
    Polar p;
    double minr=1e9,maxr=-1e9;
    while(fread(&p,sizeof(Polar),1,f)){
        if(p.r<minr)minr=p.r;
        if(p.r>maxr)maxr=p.r;
    }
    printf("Ring: r[%.1f, %.1f]\n",minr,maxr);
    fclose(f);
}

int main(){
    int N;
    scanf("%d",&N);
    create(N);
    process();
    return 0;
}