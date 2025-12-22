#include <cstdio>

int main(){
    FILE* in=fopen("input.txt","r");
    if(!in)return 1;
    int N;
    fscanf(in,"%d",&N);
    int* arr=new int[N];
    for(int i=0;i<N;i++)fscanf(in,"%d",&arr[i]);
    fclose(in);
    int pos=0;
    for(int i=0;i<N;i++){
        if(arr[i]!=0)arr[pos++]=arr[i];
    }
    while(pos<N)arr[pos++]=0;
    for(int i=0;i<N;i++)printf("%d ",arr[i]);
    delete[] arr;
    return 0;
}