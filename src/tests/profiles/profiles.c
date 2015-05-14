#include <stdlib.h>
#include <stdio.h>

int main(){
    int pxly = 3;
    int pxlx = 5;
    // DATA
    int data[pxlx*pxly];
    for (int i=0;i<pxly*pxlx;i++){
//        printf("%d\n", i);
        data[i] = i;
    }

    int index = 0;
    int col = 0;
    int px = 0;
    int py = 0;

    for (int i=0;i<pxlx;i++){
        py = 0;
        for (int j=0;j<pxly;j++){
            py = py + data[pxlx*j+i];
            px = px + data[index];
            col += 1;
            if (col >= pxlx){
                printf("x>%d\n",px);
                col = 0;
                px = 0;
            }
            index += 1;
        printf("  %d<y\n",py);
        }
    }
    return 0;
}
