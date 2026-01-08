#include <stdio.h>

int main() {
    int X[5] = {0,1,1,0,1};   // 13
    int Y[5] = {1,0,1,0,0};   // 20
    int g[31];

    for(int i = 0; i < 31; i++) {
        g[i] = X[4] ^ Y[4];  // выход = X4 xor Y4
        
        int newX = X[4] ^ X[3];  // X4 xor X5
        int newY = Y[4] ^ Y[1];  // Y2 xor Y5 
        
        for(int j = 4; j > 0; j--) {
            X[j] = X[j-1];
            Y[j] = Y[j-1];
        }
        X[0] = newX;
        Y[0] = newY;
    }

    
    for(int s = 0; s < 31; s++) {
        int matches = 0;
        int mismatches = 0;
        printf("%2d | ", s);

        for(int i = 0; i < 31; i++) {
            int b = g[(i + s) % 31];
            printf("%d ", b);
            if(g[i] == b) {
                matches++;
            } else {
                mismatches++;
            }
        }

        //  Rx(τ) = (число совпадений - число несовпадений) / N
        int diff = matches - mismatches;
        printf("| %d/31 (%.4f)\n", diff, (double)diff / 31);
    }
    
    return 0;
}