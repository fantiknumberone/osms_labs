#include <stdio.h>

void genGold(int X[5], int Y[5], int g[31]) {
    int Xt[5], Yt[5];
    for(int i=0;i<5;i++) Xt[i]=X[i], Yt[i]=Y[i];
    
    for(int i=0;i<31;i++){
        g[i]=Xt[4]^Yt[4];
        int newX=Xt[4]^Xt[3];
        int newY=Yt[4]^Yt[1];
        
        for(int j=4;j>0;j--) Xt[j]=Xt[j-1], Yt[j]=Yt[j-1];
        Xt[0]=newX; Yt[0]=newY;
    }
}

int main() {
    int X1[5]={0,1,1,0,1}, Y1[5]={1,0,1,0,0};
    int X2[5]={0,1,1,1,0}, Y2[5]={0,1,1,1,1};
    int g1[31], g2[31];
    
    genGold(X1,Y1,g1);
    genGold(X2,Y2,g2);
    
    int sum=0;
    for(int i=0;i<31;i++) sum += (g1[i]==g2[i])?1:-1;
    
    printf("Взаимная корреляция: %d/31 = %.4f\n", sum, (double)sum/31);
    return 0;
}