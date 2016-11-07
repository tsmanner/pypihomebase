import ctypes
import ctypes.util
import multiprocessing
import os
import subprocess
import webbrowser

SHELL_PROCESS = None
LastInputInfo = None
xss_available = False

if os.name == 'nt':
    class LastInputInfo(ctypes.Structure):
        _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]
else:
    class XScreenSaverInfo(ctypes.Structure):
        _fields_ = [
            ('window', ctypes.c_ulong),
            ('state', ctypes.c_int),
            ('kind', ctypes.c_int),
            ('til_or_since', ctypes.c_ulong),
            ('idle', ctypes.c_ulong),
            ('eventMask', ctypes.c_ulong)
        ]


    XScreenSaverInfo_p = ctypes.POINTER(XScreenSaverInfo)

    display_p = ctypes.c_void_p
    xid = ctypes.c_ulong
    c_int_p = ctypes.POINTER(ctypes.c_int)

    try:
        libX11path = ctypes.util.find_library('X11')
        if libX11path is None:
            raise OSError('libX11 could not be found.')
        libX11 = ctypes.cdll.LoadLibrary(libX11path)
        libX11.XOpenDisplay.restype = display_p
        libX11.XOpenDisplay.argtypes = ctypes.c_char_p,
        libX11.XDefaultRootWindow.restype = xid
        libX11.XDefaultRootWindow.argtypes = display_p,

        libXsspath = ctypes.util.find_library('Xss')
        if libXsspath is None:
            raise OSError('libXss could not be found.')
        libXss = ctypes.cdll.LoadLibrary(libXsspath)
        libXss.XScreenSaverQueryExtension.argtypes = display_p, c_int_p, c_int_p
        libXss.XScreenSaverAllocInfo.restype = XScreenSaverInfo_p
        libXss.XScreenSaverQueryInfo.argtypes = (display_p, xid, XScreenSaverInfo_p)

        dpy_p = libX11.XOpenDisplay(None)
        if dpy_p is None:
            raise OSError('Could not open X Display.')

        xss_info_p = libXss.XScreenSaverAllocInfo()
        if xss_info_p is None:
            raise OSError('XScreenSaverAllocInfo: Out of Memory.')

        rootwindow = libX11.XDefaultRootWindow(dpy_p)
        xss_available = True
    except OSError as err:
        # Logging?
        print(err, "Idle timeout not available.")


def idle():
    """
    Returns ms since last user input
    :return: int
    """
    # Windows
    if os.name == 'nt':
        last_input_info = LastInputInfo()
        last_input_info.cbSize = ctypes.sizeof(last_input_info)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))
        return float(ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime)
    else:
        """
        Return the idle time in milliseconds
        """
        if not xss_available:
            return 0
        # xss_info_p = libXss.XScreenSaverAllocInfo()
        if libXss.XScreenSaverQueryInfo(dpy_p, rootwindow, xss_info_p) == 0:
            return 0
        return xss_info_p.contents.idle


def git_update():
    """
    git_update: pulls from the git
    :return: bool indicating whether there was an update done
    """
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    git_process = subprocess.Popen(["git", "pull", "origin", "master"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    os.chdir(cwd)
    git_output_lines = git_process.communicate()[0].decode("UTF-8").split(os.linesep)
    for line in git_output_lines:
        line_split = line.split()
        if len(line_split) == 0:
            continue
        elif len(line_split) >= 3:
            if line_split[0].isdigit() and \
                            line_split[1].startswith("file") and \
                            line_split[2].startswith("changed"):
                return True
    return False


def open_shell():
    global SHELL_PROCESS
    if SHELL_PROCESS and SHELL_PROCESS.is_alive():
        if os.name == "nt":

            pass  # TODO how does this work in windows?
        else:
            elevate_str = "wmctrl -ia $(wmctrl -lp | awk -vpid={0} '$3==pid {print $1; exit}')"
            os.system(elevate_str.format(SHELL_PROCESS.pid))
    else:
        if SHELL_PROCESS:
            SHELL_PROCESS.join()
        SHELL_PROCESS = multiprocessing.Process(target=open_shell_target)
        SHELL_PROCESS.start()


def open_shell_target():
    global SHELL_PROCESS
    if os.name == "nt":
        # TODO how does this work in Windows?
        print("opening cmd.exe")
    else:
        print("opening lxterminal")
        SHELL_PROCESS = subprocess.Popen(["lxterminal"])
        SHELL_PROCESS.communicate()


def open_browser(event=None):
    webbrowser.open("http://www.google.com")


class BidirectionalDict:
    def __init__(self):
        self._list1 = []
        self._list2 = []

    def __setitem__(self, a, b):
        # If a and b are not in the map anywhere, just do the appends
        if a not in self._list1 and a not in self._list2 and b not in self._list1 and b not in self._list2:
            self._list1.append(a)
            self._list2.append(b)
        elif a in self._list1:
            if b in self._list1 or (b in self._list2 and self[a] != b):
                raise KeyError("Insert a->b mapping conflict! b in map with different key already!")
            # Update the mapping
            self._list2[self._list1.index(a)] = b
        elif a in self._list2:
            if b in self._list2 or (b in self._list1 and self[a] != b):
                raise KeyError("Insert a->b mapping conflict! b in map with different key already!")
            # Update the mapping
            self._list1[self._list2.index(a)] = b
        elif b in self._list1:
            if a in self._list1 or (a in self._list2 and self[b] != a):
                raise KeyError("Insert a->b mapping conflict! a in map with different key already!")
            # Update the mapping
            self._list2[self._list1.index(b)] = a
        elif b in self._list2:
            if a in self._list2 or (a in self._list1 and self[b] != a):
                raise KeyError("Insert a->b mapping conflict! a in map with different key already!")
            # Update the mapping
            self._list1[self._list2.index(b)] = a

    def items(self):
        return list(zip(self._list1, self._list2))

    def __contains__(self, item):
        if item in self._list1:
            return True
        return item in self._list2

    def __len__(self):
        if len(self._list1) != len(self._list2):
            raise AttributeError("Mismatched list lengths!")
        return len(self._list1)

    def __iter__(self):
        return zip(self._list1, self._list2)

    def __delitem__(self, key):
        if key in self._list1:
            del self._list2[self._list1.index(key)]
            del self._list1[self._list1.index(key)]
        elif key in self._list2:
            del self._list1[self._list2.index(key)]
            del self._list2[self._list2.index(key)]
        else:
            raise KeyError("Key " + str(key) + " not in map!")

    def __getitem__(self, item):
        if item in self._list1:
            return self._list2[self._list1.index(item)]
        elif item in self._list2:
            return self._list1[self._list2.index(item)]
        else:
            raise KeyError("Key " + str(item) + " not in map!")


if __name__ == '__main__':
    import time

    while True:
        print(idle())
        print(git_update())
        time.sleep(5)
