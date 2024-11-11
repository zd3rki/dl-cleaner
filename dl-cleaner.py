import string
import ctypes
import os.path
import time, sys
from pathlib import Path

from colorama import init
from colorama import Fore, Back, Style

exts = []
paths = []
dnlDir = ""

def main():
    ######INFO#######
    version = "1.0"
    #################
    init()
    ctypes.windll.kernel32.SetConsoleTitleW("DL-CLEANER by ZDERKI | build {}".format(version))

    os.system("cls")

    print(Fore.LIGHTCYAN_EX + "██████╗ ██╗      "+ Fore.LIGHTMAGENTA_EX+" ██████╗██╗     ███████╗ █████╗ ███╗   ██╗███████╗██████╗ ")
    print(Fore.LIGHTCYAN_EX + "██╔══██╗██║      "+ Fore.LIGHTMAGENTA_EX+"██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██╔════╝██╔══██╗")
    print(Fore.LIGHTCYAN_EX + "██║  ██║██║"+Fore.LIGHTBLUE_EX+"█████╗"+ Fore.LIGHTMAGENTA_EX+"██║     ██║     █████╗  ███████║██╔██╗ ██║█████╗  ██████╔╝")
    print(Fore.LIGHTCYAN_EX + "██║  ██║██║"+Fore.LIGHTBLUE_EX+"╚════╝"+ Fore.LIGHTMAGENTA_EX+"██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗")
    print(Fore.LIGHTCYAN_EX + "██████╔╝███████╗ "+ Fore.LIGHTMAGENTA_EX+"╚██████╗███████╗███████╗██║  ██║██║ ╚████║███████╗██║  ██║")
    print(Fore.LIGHTCYAN_EX + "╚═════╝ ╚══════╝ "+ Fore.LIGHTMAGENTA_EX +" ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  " + Fore.LIGHTGREEN_EX + "       by zderki_" + Fore.RESET)
    time.sleep(2)

    def isLineEmpty(line):
        return len(line.strip()) == 0

    def setup():
        global dnlDir
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                Lines = f.readlines()
                for line in Lines:
                    line = line.strip()

                    if "#" not in line and not isLineEmpty(line):     #splituje mp4 - C:\bla\bla a appenduje priponu do exts a cestu do paths
                        
                        if "\n" in line:
                            line = line[:-1] #odstrani \n na konci textaku (jenom pro jistotu... obcas to dela problemy)

                        if "!" not in line:
                            current = []
                            current = line.split(" - ")

                            exts.append(current[0])
                            paths.append(current[1])

                        else:
                            dnlDir = line[1:]
     
                f.close()

        else:
            print(Fore.LIGHTRED_EX + "CONFIG FILE NOT FOUND! CREATING ONE!")
            with open("config.txt", "a") as f:
                f.write("#Setup the Downloads folder this way:\n#!C:\\Users\\Jandy\\Downloads\\\n\n#Setup the files to be moved this way:\n#EXTENSION - PATH\n\n#for example:\n#mp4 - C:\\Users\\Jandy\\Desktop\\\n#docx - C:\\Users\\Jandy\\Documents\\\n#---------------------------------\n")
                f.close()

            print(Fore.LIGHTYELLOW_EX + "CONFIG CREATED... PLEASE FILL OUT AS REQUIRED!!!\nExiting in 5s")
            time.sleep(5)
            sys.exit()

        if not exts:
            print(Fore.LIGHTRED_EX +"ERROR: config.txt IS EMPTY!\nExitting in 5s")
            time.sleep(5)
            sys.exit()

        if not dnlDir:
            print(Fore.LIGHTRED_EX + "ERROR: Download directory in config.txt IS EMPTY!\nExitting in 5s")
            time.sleep(5)
            sys.exit()


    def uniquify(path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1
        return path


    def tridicka():
        for filename in os.listdir(Path(dnlDir)):
            if "." in filename:
                temp = filename.split(".")
                if temp[1] in exts:                   
                    index = exts.index(temp[1])
                    
                    try:
                        os.rename(os.path.join(dnlDir, filename), os.path.join(paths[index], filename))
                    except FileExistsError:
                        os.rename(os.path.join(dnlDir, filename), uniquify(os.path.join(paths[index], filename)))
                        print(Fore.LIGHTRED_EX + "WARN: File " + Fore.LIGHTYELLOW_EX + filename + Fore.LIGHTRED_EX + " had to be renamed!")

    setup()
    print(Fore.LIGHTGREEN_EX + "Config.txt seems fine...")
    print(Fore.RESET + "Using download folder: " + Fore.LIGHTYELLOW_EX + dnlDir)

    print(Fore.RESET + "Cleaning settings: " + Fore.LIGHTYELLOW_EX)
    for extention in exts:
        print(Fore.LIGHTYELLOW_EX + str(extention).upper() + "s" + Fore.LIGHTGREEN_EX + " to " + Fore.LIGHTYELLOW_EX + str(paths[exts.index(extention)]))

    print(Fore.LIGHTGREEN_EX + "Continue with these settings? y/n" + Fore.RESET)
    conf = input()
    if conf == "y":
        tridicka()

        print(Fore.LIGHTGREEN_EX + "DONE! All files were moved.\nExiting in 5s")
        time.sleep(5)
        sys.exit()

    else:
        print(Fore.LIGHTRED_EX + "Action CANCELLED! Exitting in 5s")
        time.sleep(5)
        sys.exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
