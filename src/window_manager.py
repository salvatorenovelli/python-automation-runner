import re
import win32gui
import win32process
from collections import namedtuple
from win32gui import EnumWindows

import psutil
import win32con


class WindowManager:
    def __init__(self, pid=None, cmdline=None, class_name=None, window_text=None):
        self._handle = self.__find_window(pid, cmdline, class_name, window_text)
        if self._handle is None:
            raise Exception(
                "Unable to find window with attributes: pid: %s, command line: %s, class_name: %s, window text: %s"
                % (str(pid), cmdline, class_name, window_text))

    def __window_enum_callback(self, hwnd, filters):
        try:
            if self._handle is not None:
                return
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
                self._handle = hwnd
        except Exception as e:
            print(e)

    def __find_window(self, pid=None, cmdline=None, class_name=None, window_text=None):
        self._handle = None
        EnumWindows(self.__window_enum_callback,
                    namedtuple("Filters", "pid cmdline class_name window_text")(pid, cmdline, class_name, window_text))
        return self._handle

    def get_hwnd(self):
        return self._handle

    def set_foreground(self):
        if self._handle is not None:
            try:
                win32gui.SetForegroundWindow(self._handle)
            except Exception as e:
                if e.args[0] != 0:
                    raise e
