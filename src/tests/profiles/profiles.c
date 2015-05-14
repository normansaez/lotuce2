#include <stdlib.h>
#include <stdio.h>

int main(){
    int pxly = 3;
    int pxlx = 5;
    // DATA
    int data[pxlx*pxly];
    int pfx[pxly];
    int pfy[pxlx];

    for (int i=0;i<pxly*pxlx;i++)
        data[i] = i;


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
                pfx[j] = px;
                col = 0;
                px = 0;
            }
            index += 1;
        }
        printf("  %d<y\n",py);
        pfy[i] = py;
    }
    printf("---\n");
    for (int i=0;i<pxlx;i++)
        printf("pfy: %d\n",pfy[i]);
    printf("---\n");
    for (int j=0;j<pxly;j++)
        printf("pfx: %d\n",pfx[j]);

    return 0;
}
