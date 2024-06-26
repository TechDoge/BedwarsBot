import win32api, win32con

class Actions:

    def __init__(self):
        pass

    # Clicks / Key Presses
    def left_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def right_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    def move_mouse(self, x, y):
        win32api.SetCursorPos((x, y))

    def press_key(self, key):
        key = ord(key.upper())
        win32api.keybd_event(key, 0, 0, 0)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    def hold_key(self, key):
        key = ord(key.upper())
        win32api.keybd_event(key, 0, 0, 0)
    
    def rel_key(self, key):
        key = ord(key.upper())
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)