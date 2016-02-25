import json
import multiprocessing
import os
import socket

HOSTMAP_FILE = os.path.dirname(__file__) + os.sep + "hostmap"


def get_hostmap():
    with open(HOSTMAP_FILE) as hostmap_fp:
        try:
            hostmap = json.load(hostmap_fp)
        except json.decoder.JSONDecodeError:
            hostmap = {}
        print(hostmap)


def update_hostmap():
    my_ip = str(socket.gethostbyname(socket.gethostname()))
    base_ip = my_ip[:my_ip.rfind('.')+1]
    for i in range(0, 255):
        ip = base_ip + str(i)
        try:
            host = socket.gethostbyaddr(ip)[0]
            print("Adding", ip, "->", host)
            update_hostmap_file(ip, host)
        except socket.herror:
            print("Adding", ip, "->", None)
            pass


def update_hostmap_file(ip, host):
    with open(HOSTMAP_FILE) as hostmap_fp:
        try:
            hostmap = json.load(hostmap_fp)
        except json.decoder.JSONDecodeError:
            hostmap = {}
        hostmap[ip] = host
    with open(HOSTMAP_FILE, "w") as hostmap_fp:
        json.dump(hostmap, hostmap_fp)


def do_update():
    update_process = multiprocessing.Process(target=update_hostmap)
    update_process.start()


if not os.path.exists(HOSTMAP_FILE):
    open(HOSTMAP_FILE, 'w').close()
