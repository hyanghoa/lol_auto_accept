import os, sys
import cv2
import pyautogui
import numpy as np
import win32gui, win32con, win32ui, win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')


def capture_window(hwnd):
    # 윈도우 핸들을 사용하여 윈도우의 좌표 및 크기 가져오기
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    width = right - left
    height = bot - top

    # 윈도우의 디바이스 컨텍스트 생성
    hdc = win32gui.GetDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hdc)
    saveDC = mfcDC.CreateCompatibleDC()

    # 비트맵 객체 생성
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    # 비트맵 객체를 디바이스 컨텍스트에 선택하여 화면 내용 복사
    saveDC.SelectObject(saveBitMap)
    result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    # 화면 내용을 numpy 배열로 변환
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    # 메모리 해제
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)

    return img

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def find_accept_button(screenshot):
    # 매칭 수락 버튼 이미지
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
    
    template = cv2.imread(resource_path("accept_button.png"), cv2.IMREAD_GRAYSCALE)

    # 템플릿 이미지의 높이와 너비 가져오기
    template_height, template_width = template.shape[:2]

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # 최대값, 최소값, 위치 가져오기
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.9:
        # 일치하는 부분의 좌표 가져오기
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

        return (bottom_right[0] + top_left[0]) // 2 , (bottom_right[1] + top_left[1]) // 2

    else:
        return None

def click_accept_button(coordinate):
    pyautogui.click(coordinate[0]+350, coordinate[1]+150)

def main():
    # "게임 클라이언트"라는 제목을 가진 창의 핸들 얻기
    hwnd = win32gui.FindWindow(None, "League of Legends")
    
    # 창의 내용 캡처
    if hwnd:
        screenshot = capture_window(hwnd)
        coordinate = find_accept_button(screenshot)
        if coordinate is not None:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 최소화되어 있을 경우 창을 복원합니다.
            win32gui.SetForegroundWindow(hwnd)  # 창을 활성화합니다.
            click_accept_button(coordinate)
            return True

if __name__ == "__main__":
    main()