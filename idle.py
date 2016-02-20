import ctypes
import ctypes.util
import os

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

global xss_available
xss_available = False

try:
    libX11path = ctypes.util.find_library('X11')
    if libX11path == None:
        raise OSError('libX11 could not be found.')
    libX11 = ctypes.cdll.LoadLibrary(libX11path)
    libX11.XOpenDisplay.restype = display_p
    libX11.XOpenDisplay.argtypes = ctypes.c_char_p,
    libX11.XDefaultRootWindow.restype = xid
    libX11.XDefaultRootWindow.argtypes = display_p,

    libXsspath = ctypes.util.find_library('Xss')
    if libXsspath == None:
        raise OSError('libXss could not be found.')
    libXss = ctypes.cdll.LoadLibrary(libXsspath)
    libXss.XScreenSaverQueryExtension.argtypes = display_p, c_int_p, c_int_p
    libXss.XScreenSaverAllocInfo.restype = XScreenSaverInfo_p
    libXss.XScreenSaverQueryInfo.argtypes = (display_p, xid, XScreenSaverInfo_p)

    dpy_p = libX11.XOpenDisplay(None)
    if dpy_p == None:
        raise OSError('Could not open X Display.')

    xss_info_p = libXss.XScreenSaverAllocInfo()
    if xss_info_p == None:
        raise OSError('XScreenSaverAllocInfo: Out of Memory.')

    rootwindow = libX11.XDefaultRootWindow(dpy_p)
    xss_available = True
except OSError as err:
    # Logging?
    xss_available = False
    raise(err)


class LastInputInfo(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]


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
        xss_info_p = libXss.XScreenSaverAllocInfo()
        if libXss.XScreenSaverQueryInfo(dpy_p, rootwindow, xss_info_p) == 0:
            return None
        return xss_info_p.contents.idle

# test

if __name__ == '__main__':
    import time
    while True:
        print(idle())
        time.sleep(2)
