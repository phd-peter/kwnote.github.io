import win32gui
import win32con

# 블루스택 창 핸들 얻기
def get_window_handle(title):
    def win_enum_handler(hwnd, result_list):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            result_list.append(hwnd)

    hwnd_list = []
    win32gui.EnumWindows(win_enum_handler, hwnd_list)
    return hwnd_list[0] if hwnd_list else None

# 블루스택 창 복원
APP_TITLE = "BlueStacks App Player"
hwnd = get_window_handle(APP_TITLE)

if hwnd:
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 복원
    print(f"Restored window: {APP_TITLE}")
else:
    print(f"Window '{APP_TITLE}' not found.")
