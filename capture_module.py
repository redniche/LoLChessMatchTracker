from ctypes import windll
# , c_int, c_uint, c_char_p, c_buffer
# from struct import calcsize, pack
from PIL import Image
import win32gui
import win32con
import win32ui
from mss import mss

# gdi32 = windll.gdi32
#
# # Win32 functions
# CreateDC = gdi32.CreateDCA
# CreateCompatibleDC = gdi32.CreateCompatibleDC
# GetDeviceCaps = gdi32.GetDeviceCaps
# CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
# BitBlt = gdi32.BitBlt
# SelectObject = gdi32.SelectObject
# GetDIBits = gdi32.GetDIBits
# DeleteDC = gdi32.DeleteDC
# DeleteObject = gdi32.DeleteObject
#
# # Win32 constants
# NULL = 0
# HORZRES = 8
# VERTRES = 10
# SRCCOPY = 13369376
# HGDI_ERROR = 4294967295
# ERROR_INVALID_PARAMETER = 87
#
# def grab_screen(bbox=None):
#     """
#     Grabs a screenshot. This is a replacement for PIL's ImageGrag.grab() method
#     that supports multiple monitors. (SEE: https://github.com/python-pillow/Pillow/issues/1547)
#
#     Returns a PIL Image, so PIL library must be installed.
#
#     Usage:
#         im = grab_screen() # grabs a screenshot of the primary monitor
#         im = grab_screen([-1600, 0, -1, 1199]) # grabs a 1600 x 1200 screenshot to the left of the primary monitor
#         im.save('screencap.jpg')
#     """
#     def cleanup():
#         if bitmap:
#             DeleteObject(bitmap)
#         DeleteDC(screen_copy)
#         DeleteDC(screen)
#
#     try:
#         screen = CreateDC(c_char_p(b'DISPLAY'), NULL, NULL, NULL)
#         screen_copy = CreateCompatibleDC(screen)
#
#         if bbox:
#             left,top,x2,y2 = bbox
#             width = x2 - left
#             height = y2 - top
#         else:
#             left = 0
#             top = 0
#             width = GetDeviceCaps(screen, HORZRES)
#             height = GetDeviceCaps(screen, VERTRES)
#
#         bitmap = CreateCompatibleBitmap(screen, width, height)
#         if bitmap == NULL:
#             print('grab_screen: Error calling CreateCompatibleBitmap. Returned NULL')
#             return
#
#         hobj = SelectObject(screen_copy, bitmap)
#         if hobj == NULL or hobj == HGDI_ERROR:
#             print('grab_screen: Error calling SelectObject. Returned {0}.'.format(hobj))
#             return
#
#         if BitBlt(screen_copy, 0, 0, width, height, screen, left, top, SRCCOPY) == NULL:
#             print('grab_screen: Error calling BitBlt. Returned NULL.')
#             return
#
#         bitmap_header = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 24)
#         bitmap_buffer = c_buffer(bitmap_header)
#         bitmap_bits = c_buffer(ord(' ') * (height * ((width * 3 + 3) & -4)))
#         got_bits = GetDIBits(screen_copy, bitmap, 0, height, bitmap_bits, bitmap_buffer, 0)
#         if got_bits == NULL or got_bits == ERROR_INVALID_PARAMETER:
#             print('grab_screen: Error calling GetDIBits. Returned {0}.'.format(got_bits))
#             return
#
#         image = Image.frombuffer('RGB', (width, height), bitmap_bits, 'raw', 'BGR', (width * 3 + 3) & -4, -1)
#         return image
#     finally:
#         pass
#         cleanup()

#이미지를 못찾을 경우 에러 클래스

class HandleNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg



class ImageNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


#창이 어디있든간에 이미지 캡쳐
def capture_specific_screen(hwnd, width: int = None, height: int = None):
    # # Get window bounds
    # # dimensions = win32gui.GetWindowRect(hwnd)
    # try:
    #     left, top, right, bot = win32gui.GetClientRect(hwnd)
    # except Exception:
    #     raise HandleNotFoundError("게임이 실행중이 아닙니다!!")
    # w = right - left
    # h = bot - top
    #
    # if width is not None:
    #     w = width
    # if height is not None:
    #     h = height
    #
    # hwndDC = win32gui.GetWindowDC(hwnd)
    # mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # saveDC = mfcDC.CreateCompatibleDC()
    #
    # saveBitMap = win32ui.CreateBitmap()
    # saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    #
    # saveDC.SelectObject(saveBitMap)
    #
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    # # print(result)
    #
    # bmp_info = saveBitMap.GetInfo()
    # bmp_str = saveBitMap.GetBitmapBits(True)
    # im = Image.frombuffer(
    #     'RGB',
    #     (bmp_info['bmWidth'], bmp_info['bmHeight']),
    #     bmp_str, 'raw', 'BGRX', 0, 1)
    #
    # win32gui.DeleteObject(saveBitMap.GetHandle())
    # saveDC.DeleteDC()
    # mfcDC.DeleteDC()
    # win32gui.ReleaseDC(hwnd, hwndDC)
    #
    # if result == 1:
    #     return im
    # else:
    #     raise ImageNotFoundError("이미지를 찾을 수 없음")

    im = 0
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        im = Image.frombuffer(
            'RGB', sct_img.size,
            sct_img.bgra, 'raw', 'BGRX')
        # im.show()
    return im


#창의 전체 이미지를 반환하는 함수
def capture_specific_by_title(window_name: str, width: int = None, height: int = None):
    hwnd = win32gui.FindWindow(None, window_name)
    # print(hwnd)
    # win32gui.SetForegroundWindow(hwnd)
    return capture_specific_screen(hwnd, width, height)

# def capture_screenshot():
#     # Capture entire screen
#     # while True:
#         with mss() as sct:
#             monitor = sct.monitors[1]
#             sct_img = sct.grab(monitor)
#             # Convert to PIL/Pillow Image
#             img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
#             print(img)
#         # time.sleep(0.5)
# img = capture_screenshot()
# img.show()