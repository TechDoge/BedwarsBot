import os
from time import sleep

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def startWithDelay(delay):
    clear()
    print("Starting In 3.")
    sleep(delay/3)
    clear()
    print("Starting In 2..")
    sleep(delay/3)
    clear()
    print("Starting In 1...")
    sleep(delay/3)