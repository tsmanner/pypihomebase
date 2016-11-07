import common
import json
import multiprocessing
import os
import socket
import tkinter as tk

HOSTMAP_FILE = os.path.dirname(__file__) + os.sep + "hostmap"


def get_hostmap():
    with open(HOSTMAP_FILE) as hostmap_fp:
        hostmap = common.BidirectionalDict()
        try:
            [hostmap.__setitem__(item[0], item[1]) for item in json.load(hostmap_fp)]
        except json.decoder.JSONDecodeError:
            pass
        return hostmap


def get_hostmap_strings():
    hostmap = get_hostmap()
    return ["%s -> %s" % (ip.ljust(15), host) for ip, host in hostmap]


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
        pass


def do_update_ip(ip):
    update_process = multiprocessing.Process(target=update_ip, args=(ip,))
    update_process.start()
    return update_process


def update_hostmap_file(ip, host):
    with open(HOSTMAP_FILE) as hostmap_fp:
        hostmap = get_hostmap()
        if host not in hostmap:
            hostmap[ip] = host
            print("Adding", host + ": " + ip)
        else:
            if hostmap[host] != ip:
                print("Updating " + host + ": " + hostmap[host] + "->" + ip)
                del hostmap[host]
                hostmap[ip] = host
    with open(HOSTMAP_FILE, "w") as hostmap_fp:
        json.dump(hostmap.items(), hostmap_fp)


def do_update():
    update_process = multiprocessing.Process(target=update_hostmap)
    update_process.start()


class HostmapFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=500, height=480)
        self.hostmap_strings = []
        self.text = tk.Listbox(self, font="courier 9")
        width = 82
        self.text.config(width=width, height=50)
        self.text.place(x=0, y=0)
        self.update_text()

    def update_text(self):
        hostmap_strings = get_hostmap_strings()
        hostmap_strings.sort()
        if self.hostmap_strings != hostmap_strings:
            self.hostmap_strings = hostmap_strings
            self.text.delete(0, tk.END)
            for line in self.hostmap_strings:
                self.text.insert(tk.END, line + os.linesep)
        self.after(500, self.update_text)


if not os.path.exists(HOSTMAP_FILE):
    open(HOSTMAP_FILE, 'w').close()

if __name__ == "__main__":
    do_update()
    root = tk.Tk()
    hmap = HostmapFrame(root)
    hmap.pack()
    root.mainloop()
