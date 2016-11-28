import re
import win32gui
import win32process
from collections import namedtuple
from win32gui import EnumWindows

import psutil


class WindowManager:
    def __init__(self):
        self._running = False
        self._handle = None

    def _window_enum_callback(self, hwnd, filters):
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

    def find_window(self, pid=None, cmdline=None, class_name=None, window_text=None):
        self._handle = None
        EnumWindows(self._window_enum_callback,
                    namedtuple("Filters", "pid cmdline class_name window_text")(pid, cmdline, class_name, window_text))
        return self._handle
