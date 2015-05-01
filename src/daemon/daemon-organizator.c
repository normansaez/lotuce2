#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>

int main ()
{
    struct tm * timeinfo;
    struct stat s;
    time_t rawtime;
    char buffer[26];
    int errno;

    time(&rawtime);
    timeinfo = localtime(&rawtime);
//    strftime(buffer, 26, "%Y_%m_%dT%H_%M", timeinfo);/*:%S", timeinfo);*/
    strftime(buffer, 26, "Makefile", timeinfo);/*:%S", timeinfo);*/
    printf("%s\n", buffer);

    int err = stat(buffer, &s);
    if(-1 == err) {
        if(ENOENT == errno) {
            printf("does not exist\n");
        } else {
            perror("stat");
        }
    } else {
        if(S_ISDIR(s.st_mode)) {
            printf("it's a dir\n");
        } else {
            printf("exists but is no dir\n");
        }
    }

    return 0;
}
