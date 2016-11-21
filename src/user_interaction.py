import win32api
import win32con
import win32gui
import win32process


def get_cursor_pos():
    return win32gui.GetCursorPos()


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def get_pixel_colour(x, y):
    i_desktop_window_id = win32gui.GetDesktopWindow()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, x, y)
    return int(long_colour)


def get_cur_window_executable():
    try:
        hwnd = win32gui.GetForegroundWindow()
        thread, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
        return win32process.GetModuleFileNameEx(process_handle, 0)
    except RuntimeError as err:
        print("WindowsProcess", str(err))


def get_cur_window_text():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())
