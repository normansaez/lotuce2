#include <stdio.h>
#include <unistd.h>

int main(){
    int counter = 0;
    int myvar = 1;
    while(true){
        printf("%d -> %d\n", counter, myvar);
        usleep(1e6);//micro secs
        counter += 1;
    }
    return 0;
}
