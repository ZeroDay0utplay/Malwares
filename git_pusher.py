import os


os.system("git add .")
os.system("git commit -m " + '"' + input("Enter the commit MSG : ") + '"')
os.system("git push")