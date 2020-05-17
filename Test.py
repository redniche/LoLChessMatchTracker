import tkinter as tk
from tkinter import Tk, ttk
import tkinter.font

from ctypes import windll


class CounterWidget(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background='white')
        font = tk.font.Font(family="맑은 고딕", size=12)

        self.CheckMode = tk.IntVar()
        self.check_box = tk.Checkbutton(self, width='1', variable=self.CheckMode, command=self.flip_state, font=font,
                                background='white')
        self.check_box.pack(side="left", padx=0)

        self.txt_box = tk.Entry(self, font=font)
        self.txt_box.pack(side="left", padx=5, pady=0)

        self.spin_box = tk.Spinbox(self, from_=0, to=9999, font=font, width=5)
        self.spin_box.pack(side="left")

    def flip_state(self):
        self.test = self.CheckMode.get()
        if self.test == 1:  # checked
            self.txt_box['state'] = tk.DISABLED
        elif self.test == 0:  # unchecked
            self.txt_box['state'] = tk.NORMAL

# class App(ThemedTk):
#     def __init__(self):
#         super().__init__("equilux")
#
#         # ATTENTION!!
#         # The following could fail as i couldn't test with `ThemedTk`
#         # ATTENTION!!
#         style = ttk.Style(self)
#         style.configure("TLabel", background="white")


# class App(Tk):
#   def __init__(self, **args):
#     super().__init__(**args)
#     # init: 윈도우 기본 설정
#     self.title("대전 카운트")
#     self.overrideredirect(True)
#     self.iconbitmap("ddd.ico")
#     self.minsize(300, 200)
#     self.after(0, self._set_window)
#
#     # init: 요소 정의하기
#     s = ttk.Style()
#     s.configure('My.TFrame', background='grey')
#
#     titlebar = ttk.Frame(self, style="My.TFrame")
#     widget = ttk.Frame(self)
#     # icon = ttk.
#     title = ttk.Label(
#         titlebar, text=self.title(), style="titlebar.TLabel", background='grey')
#     close = ttk.Button(
#         titlebar, text='X', takefocus=False, command=self.on_exit, width=2)
#
#     # init: 요소 배치하기
#     titlebar.pack(side='top', fill='x', expand='no')
#     widget.pack(side='bottom', fill='both', expand='yes')
#     title.pack(side='left', fill='x', expand='yes', pady=3)
#     close.pack(side='right', padx=4, pady=2)
#
#     # 요소에 함수 바인딩하기
#     # <ButtonPress-1>: 마우스 왼쪽 버튼을 누름
#     # <ButtonRelease-1>: 마우스 왼쪽 버튼을 뗌
#     # <Double-Button-1>: 마우스 왼쪽 더블클릭
#     # <B1-Motion>: 마우스를 클릭한 상태로 움직임
#     title.bind("<ButtonPress-1>", self.start_move)
#     title.bind("<ButtonRelease-1>", self.stop_move)
#     title.bind("<Double-Button-1>", self.on_maximise)
#     title.bind("<B1-Motion>", self.on_move)
#
#   def on_maximise(self, event):
#     # 창의 제목을 더블클릭
#     # 최대화와 복원을 토글
#     if self.state() == 'normal':
#       self.state("zoomed")
#     else:
#       self.state("normal")
#
#   def start_move(self, event):
#     # 창의 제목을 클릭
#     # 위치 변수 등록
#     self.x = event.x
#     self.y = event.y
#
#   def stop_move(self, event):
#     # 마우스를 뗌
#     # 변수 초기화
#     self.x = None
#     self.y = None
#
#   def on_move(self, event):
#     # 마우스 드래그
#     # 윈도우를 이동
#     deltax = event.x - self.x
#     deltay = event.y - self.y
#     x = self.winfo_x() + deltax
#     y = self.winfo_y() + deltay
#     self.geometry("+%s+%s" % (x, y))
#
#   def on_exit(self):
#     # 종료 버튼 클릭
#     # GUI를 끝냄
#     self.destroy()
#
#   def _set_window(self):
#     GWL_EXSTYLE = -20
#     WS_EX_APPWINDOW = 0x00040000
#     WS_EX_TOOLWINDOW = 0x00000080
#     hwnd = windll.user32.GetParent(self.winfo_id())
#     style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
#     style = style & ~WS_EX_TOOLWINDOW
#     style = style | WS_EX_APPWINDOW
#     res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
#     self.wm_withdraw()
#     self.after(0, lambda: self.wm_deiconify())

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.custom1 = CounterWidget(self)
        self.custom1.pack(side="top")
        self.custom2 = CounterWidget(self)
        self.custom2.pack(side="top")
        self.custom3 = CounterWidget(self)
        self.custom3.pack(side="top")
        self.custom4 = CounterWidget(self)
        self.custom4.pack(side="top")
        self.custom5 = CounterWidget(self)
        self.custom5.pack(side="top")
        self.custom6 = CounterWidget(self)
        self.custom6.pack(side="top")
        self.custom7 = CounterWidget(self)
        self.custom7.pack(side="top")


window = tk.Tk()
window.title("대전 카운팅")
app = Application(master=window)
window.geometry("300x220+600+100")
window.configure(background='white')
window.resizable(False, False)
window.attributes("-topmost", True)

import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

window.iconbitmap(resource_path('ddd.ico'))

from PIL import Image
from PIL import ImageGrab
import win32gui



def EnumWindowsHandler(hwnd, extra):
    wintext = win32gui.GetWindowText(hwnd)
    print("%08X: %s" % (hwnd, wintext))

# win32gui.EnumWindows(EnumWindowsHandler, None)

hwnd = win32gui.FindWindow(None, r'League of Legends 2020.05.02 - 07.59.51.07.DVR.mp4')
print(hwnd)
# win32gui.SetForegroundWindow(hwnd)
dimensions = win32gui.GetWindowRect(hwnd)


# left,top,x2,y2 = dimensions
# width = x2 - left + 1
# height = y2 - top + 1

#LolChess name coordinates
# 1670 185
# 1820 770

# print('키에엥ㄱ')
dimensions_list = list(dimensions)
import operator

dimensions_list[0] += 1670
dimensions_list[1] += 185
dimensions_list[2] -= 70
dimensions_list[3] -= 310

# image = ImageGrab.grab(dimensions)
# image.show()

print(dimensions)

import custom_greb

image2 = custom_greb.grab_screen(dimensions_list)
print(type(image2))
image2.show()

import pytesseract
import PIL.ImageOps
import numpy as np
import cv2



image3 = custom_greb.grab_screen(dimensions)
print(image3.height)
print(image3.width)

default_crop = [1716, 203, 1816, 226]

crop_image_np = image3.crop(default_crop)
# name_image_list = []
# for idx in range(8):
#     open_cv_image = np.array(PIL.ImageOps.invert(crop_image.convert('L')))
#     # ret, dst = cv2.threshold(open_cv_image, 130, 255, cv2.THRESH_BINARY)
#     dst = cv2.adaptiveThreshold(open_cv_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 30)
#     # height, width = dst.shape[:2]
#     # img_temp = cv2.resize(dst, (int(0.97 * width), int(0.97 * height)), interpolation=cv2.INTER_CUBIC)
#     # img_result = cv2.resize(dst, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)
#
#     name_image_list.append(PIL.Image.fromarray(dst))
#     default_crop[1] += 72
#     default_crop[3] += 72
#
#     # name_image_list[idx].show()
#     print(pytesseract.image_to_string(name_image_list[idx], lang='kor+eng',
#                                       config='--psm 6 -c preserve_interword_spaces=1'))
#

# print(type(name_image_list[0]))
# name_image_list[0].show()

# image3.show()
# cropped = image3.crop(default_crop)
# print(cropped.height)


# im_haystack = Image.open()
im_needle = Image.open(resource_path('me.png'))
im_needle.show()

# print(image2.mode)
# image2 = image2.convert("RGBA")
# print(image2.mode)
# image2.show()

# import find_image

# print(np.array(image2))
# print("//////////")
# print(np.array(im_needle))

# find_image.image_find(image2, im_needle)

second_match = Image.open(resource_path('other.png'))

# find_image.image_find(image2, second_match)

# print(find_matches(image2, im_needle))


# im = np.array(image2)
# tmp = np.array(second_match)

# result = cv2.matchTemplate(im, tmp, cv2.TM_SQDIFF)

from PIL import ImageDraw


#최적 이미지를 무조건 좌측 상단 위치를 튜플로 반환. 반환이 안되는 경우가 없음.
def image_search(source_image: Image, find_image: Image):
    im = np.array(source_image)
    tmp = np.array(find_image)
    print(im.shape)
    print(tmp.shape)

    result = cv2.matchTemplate(im, tmp, cv2.TM_SQDIFF)
    (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
    return minloc

#np.ndarray타입에서 임계값을 넘은 최적 이미지를 찾아서 !!!우측!!! 상단 위치를 튜플로 반환, 못찾을 경우 -1 반환.
def image_np_serch_correct(target_image : np.ndarray, image_to_find : np.ndarray):
    image_size = target_image.shape[:2]
    template_size = image_to_find.shape[:2]

    # print ('image_size (y,x)', image_size)
    # print ('template_size (y,x)', template_size)

    result = cv2.matchTemplate(target_image, image_to_find, cv2.TM_SQDIFF)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #
    # print ('min_val', min_val)
    # print ('max_val', max_val)
    # print ('min_loc', min_loc, 'X')
    # print ('max_loc', max_loc)

    rightx = min_loc[0] + template_size[1]
    topy = min_loc[1]


    confidence = (9999999999 - min_val) / 100000000
    # print ('primary confidence', '%.2f %%' % confidence)

    altconfidence = 100 - ((min_val / max_val)*100)
    # print ('alternate confidence', '%.2f %%' % altconfidence)

    if (altconfidence > 99) or ((confidence > 97) and (altconfidence > 93)) or ((confidence > 95.7) and (altconfidence > 96.3)):
        # print ('The image of size', template_size, '(y,x) was found at', min_loc)
        pass

    else:
        print ('///image_serch_correct: 해당 이미지 못찾음///')
        return -1, -1

    return rightx, topy

#모든 이미지 찾은 위치 좌측상단 위치를 리스트로 반환하는 함수
def image_multiple_search(source_image: Image, find_image: Image, find_count: int):
    im = np.array(source_image)
    tmp = np.array(find_image)

    result = cv2.matchTemplate(im, tmp, cv2.TM_SQDIFF)

    result2 = np.reshape(result, result.shape[0] * result.shape[1])
    sort = np.argsort(result2)

    find_list = []
    for idx in range(find_count):
        y1, x1 = np.unravel_index(sort[idx], result.shape)  # best match
        find_list.append([x1, y1])
        # print(x1, y1)
        # topx = x1 - 110
        # topy = y1
        #
        #
        # draw = ImageDraw.Draw(image2)
        # draw.line(((topx, topy), (x1, topy)), fill="red", width=1)
        # draw.line(((topx, topy), (topx, topy + 22)), fill="red", width=1)
        # draw.line(((topx, y1 + 22), (x1, y1 + 22)), fill="red", width=1)
        # draw.line(((x1, y1), (x1, y1 + 22)), fill="red", width=1)
        # del draw

    # sorted(find_list, key=lambda k: [k[1], k[0]])
    # y축 좌표를 통한 간접정렬
    find_list = np.array(find_list)
    ind = np.lexsort((find_list[:, 1], find_list[:, 0]))
    find_list = find_list[ind]

    print(find_list)
    # print(sort)
    # image2.show()

    return find_list


#상수로 쓸 클래스
class Constant:
    name_width = 110
    name_height = 22


name_pos_list = image_multiple_search(image2, second_match, 7)

print(name_pos_list)


# print("//전처리 전 결과//\n" + pytesseract.image_to_string(image2, lang='kor+eng',
#                                   config='--psm 6 -c preserve_interword_spaces=1'))
#
#

#open cv에서 쓸 수 있게 Image를 numpy형식으로 변환, 반전사용
open_cv_image2 = np.array(PIL.ImageOps.invert(image2.convert('L')))
# PIL.Image.fromarray(open_cv_image2).show()
#
# ret, th = cv2.threshold(open_cv_image2, 200, 255, cv2.THRESH_BINARY)
# PIL.Image.fromarray(th).show()
# out = cv2.bitwise_not(th)
# contours, hierarchy = cv2.findContours(out, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# for cnt in contours:
# cv2.drawContours(open_cv_image2, contours, 0, (255, 0, 0), 2)

PIL.Image.fromarray(open_cv_image2).show()

after_image = cv2.adaptiveThreshold(open_cv_image2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 30)


#!!!!!!!!!!!!!
img_temp = PIL.Image.fromarray(after_image)

img_temp.show()
#
# print("//전처리 후 결과//\n" + pytesseract.image_to_string(dst, lang='kor+eng',
#                                   config='--psm 6 -c preserve_interword_spaces=1'))
# print('/////')

#관심영역 폭 90 높이 36
#1차 서칭 포인트에서 X: -35 y: -7
#좌측상단은 x -125 y -7
#우측하단은 x -36 y +30
name_image_list = []
# left_rect_image = Image.open(resource_path("left_rectangle.png"))
# empty_rect_image = Image.open(resource_path("empty_rectangle.png"))
empty_rect_image = cv2.imread(resource_path("empty_rectangle.png"), cv2.IMREAD_GRAYSCALE)
for idx, [x, y] in enumerate(name_pos_list):
    # print(x, y)
    # x1 = x - 125
    # x2 = x - 36
    #
    # y1 = y - 7
    # y2 = y + 30

    x1 = x - 110
    x2 = x - 5

    y1 = y
    y2 = y + 22
    # crop_image = image2.crop((x1, y1, x2, y2))
    # print(crop_image)
    # print("결과//////////////////////////////////")
    # topx, topy = image_search(crop_image, left_rect_image)
    # print("결과//////////////////////////////////")
    #
    # draw = ImageDraw.Draw(crop_image)
    # draw.line(((topx, topy), (topx+1, topy)), fill="red", width=1)
    # draw.line(((topx, topy), (topx, topy + 1)), fill="red", width=1)
    # draw.line(((topx, topy + 1), (topx, topy + 1)), fill="red", width=1)
    # draw.line(((topx, topy + 1), (topx, topy)), fill="red", width=1)
    # del draw
    # crop_image.show()

    # draw = ImageDraw.Draw(img_temp)
    # draw.line(((x1, y1), (x2, y1)), fill="red", width=1)
    # draw.line(((x1, y1), (x1, y2)), fill="red", width=1)
    # draw.line(((x1, y2), (x2, y2)), fill="red", width=1)
    # draw.line(((x2, y1), (x2, y2)), fill="red", width=1)
    # del draw

    #numpy에서 이미지 자르기
    crop_image_np = after_image[y1:y2, x1:x2]

    x_delta = 0
    y_delta = 0
    rightx = 1
    while rightx != -1:
        rightx, topy = image_np_serch_correct(crop_image_np, np.array(empty_rect_image))
        if rightx != -1:
            crop_image_np = crop_image_np[topy:, rightx:]
            x_delta += rightx
            y_delta += topy

    draw = ImageDraw.Draw(img_temp)
    draw.line(((x1+x_delta, y1+y_delta), (x1+x_delta, y1+y_delta+5)), fill="red", width=1)
    draw.line(((x1+x_delta+5, y1+y_delta), (x1+x_delta+5, y1+y_delta+5)), fill="red", width=1)
    draw.line(((x1+x_delta, y1+y_delta+5), (x1+x_delta+5, y1+y_delta+5)), fill="red", width=1)
    draw.line(((x1+x_delta, y1+y_delta), (x1+x_delta+5, y1+y_delta)), fill="red", width=1)
    del draw

    PIL.Image.fromarray(crop_image_np).show()

    # cv2.imshow(str(crop_image), crop_image)

    # PIL.Image.fromarray(thresh).show()
    # PIL.Image.fromarray(mask).show()

    # open_cv_image = np.array(PIL.ImageOps.invert(crop_image.convert('L')))
    # ret, dst = cv2.threshold(open_cv_image, 130, 255, cv2.THRESH_BINARY)
    # dst = cv2.adaptiveThreshold(crop_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 9)
    # height, width = dst.shape[:2]
    # img_temp = cv2.resize(dst, (int(0.97 * width), int(0.97 * height)), interpolation=cv2.INTER_CUBIC)
    # img_result = cv2.resize(dst, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)
    #1820 -1785
    #362-369
    #399-369

    name_image_list.append(crop_image_np)
    #
    # name_image_list[idx].show()
    print(pytesseract.image_to_string(crop_image_np, lang='kor+eng',
                                      config='--psm 7 -c preserve_interword_spaces=1'))

image2.show()
img_temp.show()
#
# for image in name_image_list:
#     PIL.Image.fromarray(image).show()


# #the get the best match fast use this:
# (min_x, max_y, minloc, maxloc) = cv2.minMaxLoc(result)
# (x,y) = minloc
#
# #get all the matches:
# result2 = np.reshape(result, result.shape[0]*result.shape[1])
# sort = np.argsort(result2)

# (y1, x1) = np.unravel_index(sort[0], result.shape) # best match
# (y2, x2) = np.unravel_index(sort[7], result.shape) # second best match
# print(x1, y1)
# print(x2, y2)



# for idx in range(7):
#     (y1, x1) = np.unravel_index(sort[idx], result.shape)  # best match
#     print(x1, y1)
#     topx = x1 - 110
#     topy = y1
#     draw = ImageDraw.Draw(image2)
#     draw.line(((topx, topy), (x1, topy)), fill="red", width=1)
#     draw.line(((topx, topy), (topx, topy + 22)),   fill="red", width=1)
#     draw.line(((topx, y1 + 22), (x1, y1 + 22)),   fill="red", width=1)
#     draw.line(((x1, y1), (x1, y1+22)), fill="red", width=1)
#     del draw
#
# print(sort)
# image2.show()

app.mainloop()

