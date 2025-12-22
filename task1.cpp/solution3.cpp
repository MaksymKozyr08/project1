#include <iostream>
#include <cstdlib>

int N_sz;
int** mat;

int dfs(int r,int c){
    if(r<0||c<0||r>=N_sz||c>=N_sz||mat[r][c]==0)return 0;
    mat[r][c]=0;
    return 1+dfs(r+1,c)+dfs(r-1,c)+dfs(r,c+1)+dfs(r,c-1);
}

int main(){
    std::cout<<"Enter n: ";
    std::cin>>N_sz;
    mat=new int*[N_sz];
    for(int i=0;i<N_sz;i++){
        mat[i]=new int[N_sz];
        for(int j=0;j<N_sz;j++)mat[i][j]=std::rand()%2;
    }
    for(int i=0;i<N_sz;i++){
        for(int j=0;j<N_sz;j++)std::cout<<mat[i][j]<<" ";
        std::cout<<"\n";
    }
    int max_area=0;
    for(int i=0;i<N_sz;i++){
        for(int j=0;j<N_sz;j++){
            if(mat[i][j]==1){
                int area=dfs(i,j);
                if(area>max_area)max_area=area;
            }
        }
    }
    std::cout<<"Max area: "<<max_area<<"\n";
    for(int i=0;i<N_sz;i++)delete[] mat[i];
    delete[] mat;
    return 0;
}