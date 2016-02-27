import json
import multiprocessing
import os
import socket
import tkinter as tk

HOSTMAP_FILE = os.path.dirname(__file__) + os.sep + "hostmap"


def get_hostmap():
    with open(HOSTMAP_FILE) as hostmap_fp:
        try:
            hostmap = json.load(hostmap_fp)
        except ValueError:
            hostmap = {}
        except json.decoder.JSONDecodeError:
            hostmap = {}
        return hostmap


def get_hostmap_strings():
    hostmap = get_hostmap()
    return ["%s -> %s" % (ip, host) for ip, host in hostmap.items()]


def update_hostmap():
    processes = []
    my_ip = str(socket.gethostbyname(socket.gethostname()))
    base_ip = my_ip[:my_ip.rfind('.')+1]
    for i in range(0, 255):
        ip = base_ip + str(i)
        processes.append(do_update_ip(ip))
    while len(processes):
        for process in processes:
            if not process.is_alive():
                process.join()
                processes.remove(process)


def update_ip(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        update_hostmap_file(ip, host)
    except socket.herror:
#        print("Adding", ip, "->", None)
        pass


def do_update_ip(ip):
    update_process = multiprocessing.Process(target=update_ip, args=(ip,))
    update_process.start()
    return update_process


def update_hostmap_file(ip, host):
    with open(HOSTMAP_FILE) as hostmap_fp:
        try:
            hostmap = json.load(hostmap_fp)
        except ValueError:
            hostmap = {}
        except json.decoder.JSONDecodeError:
            hostmap = {}
        if ip not in hostmap:
            print("Adding   ", ip, "->", host)
            hostmap[ip] = host
        elif hostmap[ip] != host:
            hostmap.pop(ip)
            print("Updating ", ip, "->", host)
            hostmap[ip] = host
#        else:
#            print("Unchanged", ip, "->", host)

    with open(HOSTMAP_FILE, "w") as hostmap_fp:
        json.dump(hostmap, hostmap_fp)


def do_update():
    update_process = multiprocessing.Process(target=update_hostmap)
    update_process.start()


class HostmapFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=500, height=480)
        self.text = tk.Listbox(self)
        width = 82
        self.update_text()
        self.text.config(width=width, height=50)
        self.text.place(x=0, y=0)

    def update_text(self):
        self.text.delete(0, tk.END)
        for line in get_hostmap_strings():
            self.text.insert(tk.END, line + os.linesep)


if not os.path.exists(HOSTMAP_FILE):
    open(HOSTMAP_FILE, 'w').close()

if __name__ == "__main__":
    root = tk.Tk()
    map = HostmapFrame(root)
    map.pack()
    root.mainloop()
