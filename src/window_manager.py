import re
import win32gui
import win32process
from collections import namedtuple
from win32gui import EnumWindows

import psutil


class WindowManager:
    def __init__(self, pid=None, cmdline=None, class_name=None, window_text=None):
        self._handles = None
        self.__find_windows(pid, cmdline, class_name, window_text)

    def get_handles(self):
        return self._handles

    def print(self):
        for hwnd in self._handles:
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            print("PID %s:" % win32process.GetWindowThreadProcessId(hwnd)[1])
            print("\t Is Visible: %d" % win32gui.IsWindowVisible(hwnd))
            print("\t Class Name: %s" % win32gui.GetClassName(hwnd))
            print("\tLocation: (%d, %d)" % (x, y))
            print("\t    Size: (%d, %d)" % (w, h))

    def __window_enum_callback(self, hwnd, filters):
        try:
            match = True
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]

            if filters.pid is not None:
                match &= pid == filters.pid
            if filters.cmdline is not None:
                cmdline = str(psutil.Process(pid).cmdline())
                match &= re.match(filters.cmdline, cmdline) is not None
            if filters.class_name is not None:
                class_name = win32gui.GetClassName(hwnd)
                match &= re.match(filters.class_name, class_name) is not None
            if filters.window_text is not None:
                window_text = win32gui.GetWindowText(hwnd)
                match &= re.match(filters.window_text, window_text) is not None
            if match:
                self._handles.append(hwnd)
        except Exception as e:
            print(e)

    def __find_windows(self, pid=None, cmdline=None, class_name=None, window_text=None):
        if self._handles is not None:
            raise AssertionError("This instance is already initialized, please create another one.")

        self._handles = list()
        EnumWindows(self.__window_enum_callback,
                    namedtuple("Filters", "pid cmdline class_name window_text")(pid, cmdline, class_name, window_text))


class Window:
    def __init__(self, pid=None, cmdline=None, class_name=None, window_text=None):
        self._handle = WindowManager().find_windows(pid, cmdline, class_name, window_text)
        if len(self._handle) != 1:
            raise Exception(
                "Found %d window/s with the current search criteria: pid: %s, command line: %s, class_name: %s, window text: %s"
                % (len(self._handle), str(pid), cmdline, class_name, window_text))

    def get_hwnd(self):
        return self._handle

    def set_foreground(self):
        if self._handle is not None:
            try:
                win32gui.SetForegroundWindow(self._handle)
            except Exception as e:
                if e.args[0] != 0:
                    raise e
