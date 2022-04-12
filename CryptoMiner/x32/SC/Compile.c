#include <stdlib.h>



int main() {
	system("gcc zdo.c -o zdo.exe");
	system("gcc del.c -o del.exe");
	system("gcc Win32.c -o Win32.exe");
	system("g++ sys32.cpp -static-libgcc -static-libstdc++ -o Sys32.exe");
	system("move Win32.exe .\\WIN32\\");
	system("mkdir System");
	system("move Sys32.exe .\\System\\");
	return 0;
}