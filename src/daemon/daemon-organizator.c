#include <stdio.h>
#include <time.h>

int main ()
{
    time_t rawtime;
    struct tm * timeinfo;
    char buffer[26];

    time(&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer, 26, "%Y_%m_%dT%H_%M", timeinfo);/*:%S", timeinfo);*/
    printf("%s\n", buffer);
    return 0;
}
