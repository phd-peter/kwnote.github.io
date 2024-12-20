import time
import pyautogui
import mss
import pygetwindow as gw
import mss.tools

# -3 파일 : 5개를 찍어서 모아서 저장하기

# 설정 값
CAPTURE_INTERVAL = 1.2  # 클릭 후 대기 시간 (2초)
SAVE_DIRECTORY = "screenshots/"
APP_TITLE = "BlueStacks App Player"  # 블루스택 창 제목

# 클릭 좌표
FIRST_CLICK_COORD = (3370, 280)  # 처음 4번 클릭할 좌표
SECOND_CLICK_COORD = (2663, 280)  # 마지막 5번째 클릭할 좌표

def get_window_rect(title):
    """블루스택 창의 위치와 크기(Rect)를 반환."""
    import win32gui
    def win_enum_handler(hwnd, result_list):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            result_list.append(hwnd)

    hwnd_list = []
    win32gui.EnumWindows(win_enum_handler, hwnd_list)
    if hwnd_list:
        hwnd = hwnd_list[0]
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    else:
        raise Exception(f"No window with title '{APP_TITLE}' found.")

def capture_bluestacks(title, count):
    """블루스택 창의 현재 화면을 캡처."""
    with mss.mss() as sct:
        rect = get_window_rect(title)
        monitor = {"top": rect[1], "left": rect[0], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
        screenshot = sct.grab(monitor)
        
        # 파일 저장
        filename = f"{SAVE_DIRECTORY}bluestacks_set_{count}.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
        print(f"Screenshot saved: {filename}")

def click_and_capture(title):
    """5번 클릭하고 캡처를 반복하여 하나의 셋트를 만듦."""
    
    # 처음 4번 같은 좌표 클릭
    for i in range(1, 5):  # 캡처 후 클릭하기 1, 2, 3, 4번 클릭
        time.sleep(CAPTURE_INTERVAL)
        capture_bluestacks(title, i) 
        pyautogui.click(x=FIRST_CLICK_COORD[0], y=FIRST_CLICK_COORD[1])
        print(f"Clicked on {FIRST_CLICK_COORD} (Click {i})")
        time.sleep(CAPTURE_INTERVAL)

    # 마지막 5번째 클릭 다른 좌표
    for i in range(1, 10):  # 5번 클릭
        time.sleep(CAPTURE_INTERVAL)
        pyautogui.click(x=SECOND_CLICK_COORD[0], y=SECOND_CLICK_COORD[1])
        print(f"Clicked on {SECOND_CLICK_COORD} (Click 5)")
        time.sleep(CAPTURE_INTERVAL/10)

if __name__ == "__main__":
    import os
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

    while True:
        try:
            print("Starting a new set...")
            click_and_capture(APP_TITLE)  # 한 셋트(5번 클릭과 캡처) 수행
            break  # 한 셋트 후 종료 (필요시 반복 가능)
        except Exception as e:
            print(f"Error occurred: {e}")
            break
