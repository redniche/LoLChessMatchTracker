import tkinter as tk
# from tkinter import Tk, ttk
import tkinter.font
import time
# from ctypes import windll
import sys, os, win32gui, win32con
from PIL import Image
from typing import List
import threading
import pytesseract
import PIL.ImageOps
import numpy as np
import cv2
from mss import mss

from capture_module import capture_specific_by_title, HandleNotFoundError
from image_module import image_np_search_correct, is_image_exist, image_multi_search, image_match_area_search, \
    confidence_by_image_search


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def EnumWindowsHandler(hwnd, extra):
    wintext = win32gui.GetWindowText(hwnd)
    print("%08X: %s" % (hwnd, wintext))

#TODO 윈도우 이름, 핸들러 알아내는 함수
# win32gui.EnumWindows(EnumWindowsHandler, None)


#상수로 쓸 클래스
class Constant:
    NAME_WIDTH = 110
    NAME_HEIGHT = 22
    OTHER_PEOPLE_COUNT = 7
    # GAME_WINDOW_NAME = r'League of Legends (TM) Client'
    GAME_WINDOW_NAME = r'#공부 - Discord'
    # GAME_WINDOW_NAME = r'Super Animal Royale'
    NAME_DIMENSIONS = (1670, 185, 1850, 770)
    ROUND_DIMENSIONS = (834, 29, 1084, 44)
    FIGHT_START_DIMENSIONS = (940, 130, 980, 170)
    FIGHT_METER_DIMENSIONS = (1600, 270, 1620, 620)
    # FIGHT_METER_DIMENSIONS = (1600, 270, 1900, 370)
    FIGHT_METER_NAME_DIMENSIONS = (1618, 278, 1748, 297)


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

        self.spin_meet_count = tk.Spinbox(self, from_=0, to=9999, font=font, width=5)
        self.spin_meet_count.pack(side="left")

        self.spin_met_count = tk.Spinbox(self, from_=0, to=9999, font=font, width=5)
        self.spin_met_count.pack(side="left")

        self.check_flag = 0

    def flip_state(self):
        self.check_flag = self.CheckMode.get()
        if self.check_flag == 1:  # checked
            self.txt_box['state'] = tk.DISABLED
        elif self.check_flag == 0:  # unchecked
            self.txt_box['state'] = tk.NORMAL

#TODO 앱 디자인 커스텀

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


class Player:
    def __init__(self, name="", hp=None, meeting=0, last_met=0, x=None, y=None):
        self.name = name
        self.hp = hp
        self.meeting = 0
        self.last_met = 0
        self.x = x
        self.y = y
        self.death_flag = False
        self.crop_image: PIL.Image = None
        self.crop_image_grey_np: np.ndarray = None

    def builder(self, name="", hp=None, meeting=0, last_met=0, x=None, y=None):
        self.name = name
        self.hp = hp
        self.meeting = meeting
        self.last_met = last_met
        self.x = x
        self.y = y


#메인 어플리케이션
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.counter_widget_list: List[CounterWidget] = []
        self.players = [Player() for _ in range(Constant.OTHER_PEOPLE_COUNT)]
        self.dimensions = None

        #TODO 공유자원이 될 가능성이 있음.
        self.meet_flag: bool = False

        self.create_widgets()

        self.start_thread = threading.Thread(target=self.start_process)
        self.start_thread.daemon = True
        self.start_thread.start()

        # self.after(10000, self.recognize_name)

        #  TODO 스레드 함수 만들기
        # t1 = threading.Thread(target=, args=('http://google.com',))
        # t1.daemon = True
        # t1.start()

    def create_widgets(self):
        for idx in range(Constant.OTHER_PEOPLE_COUNT):
            self.counter_widget_list.append(CounterWidget(self))
            self.counter_widget_list[idx].pack(side="top")

    #프로그램 시작시 작동
    def start_process(self):
        try:
            self.recognize_name()
            self.update_form()
            for p in self.players:
                print(p.name)

            # self.players[0].crop_image.show()
            # self.players[2].crop_image.show()
            # self.players[5].crop_image.show()
            # self.players[6].crop_image.show()
            # Image.fromarray(self.players[6].crop_image_grey_np).show()

            # self.after(0, self.always_process)+
            always_process = threading.Thread(target=self.always_process)
            always_process.daemon = True
            always_process.start()
        except Exception as ex:
            if type(ex) is HandleNotFoundError:
                #TODO 게임 실행 아닌 상태 바꿔야함.
                print("게임이 실행중이 아닙니다.")
            print("이름을 못찾았음")

    #계속 작동
    def always_process(self):

        #TODO 최종 마무리 지을 때 최적화 할 것
        round_check_process = threading.Thread(target=self.round_check_process)
        round_check_process.daemon = True
        round_check_process.start()

        round_check_process = threading.Thread(target=self.meeting_check_process)
        round_check_process.daemon = True
        round_check_process.start()


        # meeting_check_process = threading.Thread(target=self.meeting_check_process)
        # meeting_check_process.daemon = True
        # meeting_check_process.start()

    def round_check_process(self):
        # pass
        # while not exit_flag.wait(timeout=0.45):
        while True:
            try:
                if self.is_end_round():
                    self.update_player_by_form()
                    self.update_player_pos()
                    self.sort_update_by_y()
                    print("라운드엔드작동완료")
                time.sleep(0.45)
            except Exception as ex:
                if type(ex) is HandleNotFoundError:
                    print("게임이 실행중이 아닙니다.")
                break

        # if self.is_round_end():
        #     print("라운드엔드작동중")
        # self.recognize_round_end()
        # self.after(1000, self.always_process)

    def meeting_check_process(self):
        while True:
            try:
                if self.is_start_fight():
                    self.meet_flag = True
                    print("스타트파이트작동중")
                    time.sleep(4.5)

                    self.meet_and_met_counting()
                    self.update_form()
                    time.sleep(20)
                time.sleep(0.8)
            except Exception as ex:
                if type(ex) is HandleNotFoundError:
                    print("게임이 실행중이 아닙니다.")
                break

    #플레이어 변경사항을 윈도우 폼에 적용
    def update_form(self):
        # Entry 텍스트 변경
        for idx, player in enumerate(self.players):
            print(player.name, player.x, player.y)
            self.counter_widget_list[idx].txt_box.delete(0, "end")
            print("update_form: ", player.name)
            print("update_form(type): ", type(player.name))
            # Image.fromarray(player.crop_image).show()
            print(type(player.crop_image))
            self.counter_widget_list[idx].txt_box.insert(0, player.name)
            self.counter_widget_list[idx].spin_meet_count.delete(0, "end")
            self.counter_widget_list[idx].spin_meet_count.insert(0, player.meeting)
            self.counter_widget_list[idx].spin_met_count.delete(0, "end")
            self.counter_widget_list[idx].spin_met_count.insert(0, player.last_met)

    #폼 변경사항을 플레이어에 적용
    def update_player_by_form(self):
        for idx, widgets in enumerate(self.counter_widget_list):
            self.players[idx].name = widgets.txt_box.get()
            self.players[idx].meeting = int(widgets.spin_meet_count.get())
            self.players[idx].last_met = int(widgets.spin_met_count.get())

    #y축 위치기반 정렬
    def sort_update_by_y(self):
        self.players.sort(key=lambda x: x.y)
        self.update_form()

    #확률기반 정렬
    #TODO 확률기반 정렬 제작

    #이 함수는 Player 객체를 전반적으로 갱신합니다.
    def recognize_name(self):
        error_count = 0
        # TODO 특정 창 전체 이미지 캡쳐
        while True:
            try:
                #전체 화면 불러오기
                score_name_image = capture_specific_by_title(Constant.GAME_WINDOW_NAME)
                print(np.array(score_name_image))
                # score_name_image.show()

                print(score_name_image.height, score_name_image.width)
                # 원래는 image2였다.

                #오른쪽 이름부분 잘라내기
                score_name_image = score_name_image.crop(Constant.NAME_DIMENSIONS)
                # print(type(score_name_image))
                # image2.show()

                # 내 위치 찾기
                # TODO 이거 개발
                # 아직은 의미 없음
                # im_needle = Image.open(resource_path('me.png'))
                #
                # im_needle.show()

                # print(image2.mode)
                # image2 = image2.convert("RGBA")
                # print(image2.mode)
                # image2.show()

                # import find_image

                # print(np.array(image2))
                # print("//////////")
                # print(np.array(im_needle))

                # find_image.image_find(image2, im_needle)

                #체력 옆의 작은 이미지 리소스로 열기
                second_match = Image.open(resource_path('other.png'))

                #위치 리스트 반환
                name_pos_list = image_multi_search(score_name_image, second_match, Constant.OTHER_PEOPLE_COUNT)

                # open_cv_image = np.array(score_name_image)
                # lower = np.array((110, 110, 110), dtype="uint8")
                # upper = np.array((255, 255, 255), dtype="uint8")
                # after_image = cv2.inRange(open_cv_image, lower, upper)
                # Image.fromarray(after_image).show()

                # open cv에서 쓸 수 있게 Image를 numpy형식으로 변환, 반전사용
                open_cv_image = np.array(PIL.ImageOps.invert(score_name_image.convert('L')))
                #흑백 이미지 보여주기
                # PIL.Image.fromarray(open_cv_image).show()
                #전처리하기. 적응형이진화
                after_image = cv2.adaptiveThreshold(open_cv_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 28) #기본 13 28

                # print(open_cv_image[0])

                #단순이진화
                # ret, after_image = cv2.threshold(open_cv_image, 80, 255, cv2.THRESH_BINARY)
                # Image.fromarray(after_image).show()

                # #전처리한 이미지 보여주기
                # img_temp = PIL.Image.fromarray(after_image)
                # img_temp.show()

                # 관심영역 폭 90 높이 36
                # 1차 서칭 포인트에서 X: -35 y: -7
                # 좌측상단은 x -125 y -7
                # 우측하단은 x -36 y +30

                # left_rect_image = Image.open(resource_path("left_rectangle.png"))
                # empty_rect_image = Image.open(resource_path("empty_rectangle.png"))
                empty_rect_image = np.zeros((20, 10), dtype=np.uint8)
                empty_rect_image.fill(255)  # or img[:] = 255

                # sum_time = 0
                for idx, [x, y] in enumerate(name_pos_list):
                    self.players[idx].x = x
                    self.players[idx].y = y


                    #잘라낼 관심영역 x1,y1:x2,y2 좌표
                    x1 = x - 110
                    x2 = x - 5
                    y1 = y
                    y2 = y + 22

                    # numpy의 이미지 자르기
                    crop_image_np = after_image[y1:y2, x1:x2]
                    #x증가량 , y증가량
                    x_delta = 0
                    y_delta = 0
                    rightx = 1

                    while rightx != -1:
                        # print("image_np_search_correct", idx, ": ", crop_image_np.shape,  np.array(empty_rect_image).shape)
                        rightx, topy = image_np_search_correct(crop_image_np, np.array(empty_rect_image))
                        if rightx != -1:
                            crop_image_np = crop_image_np[topy:, rightx:]
                            x_delta += rightx-1
                            y_delta += topy

                    #잘라낸 이미지 player에 등록
                    self.players[idx].crop_image = score_name_image.crop((x1+x_delta, y1+y_delta, x2, y2))
                    print("recognize_name: ", crop_image_np.shape)

                    if y2-y+y_delta > 20:
                        self.players[idx].crop_image_grey_np = crop_image_np
                        self.players[idx].name = pytesseract.image_to_string(crop_image_np, lang='kor+eng',
                                                                             config='--psm 7 -c preserve_interword_spaces=1')
                        # self.players[idx].crop_image.show()

                    #TODO 잘라낸 이미지 찾아내서 좌표 얻는 법
                    #f_image = np.array(self.players[idx].crop_image)
                    #xtop, ytop = image_np_serch_correct(np.array(score_name_image), f_image)
                    #
                    # draw = ImageDraw.Draw(score_name_image)
                    # draw.line(((xtop, ytop), (xtop, ytop + 5)), fill="red", width=1)
                    # draw.line(((xtop + 5, ytop), (xtop + 5, ytop + 5)), fill="red", width=1)
                    # draw.line(((xtop, ytop + 5), (xtop + 5, ytop + 5)), fill="red", width=1)
                    # draw.line(((xtop, ytop), (xtop + 5, ytop)), fill="red", width=1)
                    # del draw

                    # draw = ImageDraw.Draw(img_temp)
                    # draw.line(((x1 + x_delta, y1 + y_delta), (x1 + x_delta, y1 + y_delta + 5)), fill="red", width=1)
                    # draw.line(((x1 + x_delta + 5, y1 + y_delta), (x1 + x_delta + 5, y1 + y_delta + 5)), fill="red", width=1)
                    # draw.line(((x1 + x_delta, y1 + y_delta + 5), (x1 + x_delta + 5, y1 + y_delta + 5)), fill="red", width=1)
                    # draw.line(((x1 + x_delta, y1 + y_delta), (x1 + x_delta + 5, y1 + y_delta)), fill="red", width=1)
                    # del draw

                    # 개별 이미지 출력
                    # PIL.Image.fromarray(crop_image_np).show()

                    # cv2.imshow(str(crop_image), crop_image)

                    # PIL.Image.fromarray(thresh).show()
                    # PIL.Image.fromarray(mask).show()

                    # open_cv_image = np.array(PIL.ImageOps.invert(crop_image.convert('L')))
                    # ret, dst = cv2.threshold(open_cv_image, 130, 255, cv2.THRESH_BINARY)
                    # dst = cv2.adaptiveThreshold(crop_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 9)
                    # height, width = dst.shape[:2]
                    # img_temp = cv2.resize(dst, (int(0.97 * width), int(0.97 * height)), interpolation=cv2.INTER_CUBIC)
                    # img_result = cv2.resize(dst, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)


                    # name_image_list.append(crop_image_np)
                    #
                    # name_image_list[idx].show()


                    # b = time.time()
                    # sum_time += b-a
                    # print(b-a)
                # print(sum_time)
                # img_temp.show()
                # score_name_image.show()
                break
            except Exception as ex:
                if type(ex) is HandleNotFoundError:
                    raise HandleNotFoundError("게임이 실행중이 아닙니다.")
                # TODO 에러 15번 이상 발견시 작동할 에러메세지 관련 동작 필요할지도
                print("에러 발생>>>", ex)
                error_count += 1
                if error_count > 15:
                    raise Exception("이름이 제대로 인식안됨")
                time.sleep(0.45)
                continue

    #닉네임들의 위치 찾아서 Player객체의 좌표값 업데이트
    def update_player_pos(self):
        # 전체 화면 불러오기
        error_count = 0
        while True:
            if error_count > 15:
                break
            try:
                score_name_image = capture_specific_by_title(Constant.GAME_WINDOW_NAME)

                # 오른쪽 이름부분 잘라내기
                score_name_image = score_name_image.crop(Constant.NAME_DIMENSIONS)

                find_pos_list = []
                for idx in range(Constant.OTHER_PEOPLE_COUNT):
                    f_image = np.array(self.players[idx].crop_image)
                    find_pos_list.append(image_np_search_correct(np.array(score_name_image), f_image))
                    if find_pos_list[idx][0] == -1:
                        raise Exception
                for idx in range(Constant.OTHER_PEOPLE_COUNT):
                    self.players[idx].x, self.players[idx].y = find_pos_list[idx][0], find_pos_list[idx][1]
                break
            except Exception as ex:
                print(ex)
                error_count += 1
                time.sleep(1)
                continue

    #라운드가 종료 되었는지 알아내기
    def is_end_round(self):
        try:
            round_image = capture_specific_by_title(Constant.GAME_WINDOW_NAME, height=44)
        except Exception as ex:
            print(ex)
            return False
        current_round_image = round_image.crop(Constant.ROUND_DIMENSIONS)

        target = np.array(current_round_image)
        # open cv는 내부적으로 bgr을 쓰므로 정확히 맞추기 위해 이를 사용해야함.
        target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
        find = cv2.imread(resource_path("round_picker.png"), cv2.IMREAD_COLOR)

        if type(self.dimensions) is tuple:
            target[self.dimensions[1]:self.dimensions[3], self.dimensions[0]:self.dimensions[2]] = 0  #[0, 0, 0]
            # Image.fromarray(target).show()
        dimensions = image_match_area_search(target, find)
        print("dimensions: ", dimensions)

        if type(dimensions) is tuple:
            if self.dimensions is None:
                self.dimensions = dimensions
                return False
            print("is_round_end: True 반환")
            #TODO 공유자원이니 유의하셈
            self.dimensions = dimensions
            # target[self.dimensions[1]:self.dimensions[3], self.dimensions[0]:self.dimensions[2]] = 0
            return True
        # Image.fromarray(target).show()
        print("is_round_end: False 반환")
        return False

    #전투 시작 알아내기
    @staticmethod
    def is_start_fight():
        try:
            fight_start_image = capture_specific_by_title(Constant.GAME_WINDOW_NAME, width=980, height=170)
        except Exception as ex:
            print(ex)
            return False
        current_round_image = fight_start_image.crop(Constant.FIGHT_START_DIMENSIONS)

        target = np.array(current_round_image)
        # open cv는 내부적으로 bgr을 쓰므로 정확히 맞추기 위해 이를 사용해야함.
        target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
        find = cv2.imread(resource_path("fight_start.png"), cv2.IMREAD_COLOR)

        # if type(self.dimensions) is tuple:
        #     target[self.dimensions[1]:self.dimensions[3], self.dimensions[0]:self.dimensions[2]] = 0

        xy = image_np_search_correct(target, find)

        if xy[0] != -1:
            print("is_start_fight: True 반환")
            return True
        # Image.fromarray(target).show()

        print("is_start_fight: False 반환")
        return False

    def meet_and_met_counting(self):
        while self.meet_flag:
            # fight_end_image: Image
            try:
                fight_end_image = capture_specific_by_title(Constant.GAME_WINDOW_NAME, width=1755, height=590)
            except Exception as ex:
                print(ex)
                return False

            deal_meter_image = fight_end_image.crop(Constant.FIGHT_METER_DIMENSIONS)

            target = np.array(deal_meter_image)
            # open cv는 내부적으로 bgr을 쓰므로 정확히 맞추기 위해 이를 사용해야함.
            target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
            find = cv2.imread(resource_path("deal_meter_check2.png"), cv2.IMREAD_COLOR)

            # Image.fromarray(target).show()
            # Image.fromarray(find).show()

            # if type(self.dimensions) is tuple:
            #     target[self.dimensions[1]:self.dimensions[3], self.dimensions[0]:self.dimensions[2]] = 0

            if is_image_exist(target, find):
                print("meet_and_met_counting: 딜미터기 찾음")
                self.meet_flag = False

                deal_name_image = fight_end_image.crop(Constant.FIGHT_METER_NAME_DIMENSIONS)

                # 흑백 이미지 보여주기
                # PIL.Image.fromarray(open_cv_image).show()
                # 전처리하기. 적응형이진화

                # target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
                target = np.array(PIL.ImageOps.invert(deal_name_image.convert('L')))

                # target = cv2.adaptiveThreshold(target, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                #                                13, 28)  # 기본 13 28
                ret, target = cv2.threshold(target, 170, 255, cv2.THRESH_BINARY)

                empty_rect_image = np.zeros((17, 10), dtype=np.uint8)
                empty_rect_image.fill(255)  # or img[:] = 255

                right_tx, right_ty = image_np_search_correct(target, empty_rect_image)
                print("딜미터기 부분:", right_tx, right_ty)
                right_tx -= 15

                target = target[:, :right_tx]

                max_conf = 0
                max_conf_player_idx = -1
                self.update_player_by_form()
                for idx, player in enumerate(self.players):
                    player.last_met += 1
                    # Image.fromarray(self.players[idx].crop_image_grey_np).show()
                    if not -10 < player.crop_image_grey_np.shape[1] - target.shape[1] < 10:
                        print("폭이 서로 10 이상 차이남")
                        continue
                    temp = confidence_by_image_search(player.crop_image_grey_np, target, player.name, "과 현재 화면")
                    if max_conf < temp:
                        max_conf = temp
                        max_conf_player_idx = idx
                self.players[max_conf_player_idx].meeting += 1
                self.players[max_conf_player_idx].last_met = 0
            time.sleep(0.3)
            # Image.fromarray(target).show()

    class ProcessCore(threading.Thread):
        def __init__(self, q):
            threading.Thread.__init__(self)
            pass

        def run(self):
            pass


window = tk.Tk()
window.title("대전 카운팅")
app = Application(master=window)
window.geometry("400x220+600+100")
window.configure(background='white')
window.resizable(False, False)
window.lift()
window.attributes("-topmost", True)
window.iconbitmap(resource_path('ddd.ico'))

# def func():
#     while True:
#         win32gui.SetWindowPos(window.winfo_id(), win32con.HWND_TOPMOST, 0, 0, 0, 0,
#                               win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
# # print()
# round_check_process = threading.Thread(target=func)
# round_check_process.daemon = True
# round_check_process.start()





# left,top,x2,y2 = dimensions
# width = x2 - left + 1
# height = y2 - top + 1

#LolChess name coordinates
# 1670 185
# 1820 770

# # print('키에엥ㄱ')
# dimensions_list = list(dimensions)
# import operator
#
# dimensions_list[0] += 1670
# dimensions_list[1] += 185
# dimensions_list[2] -= 70
# dimensions_list[3] -= 310
# 지원 해상도 1920 * 1080


# image = ImageGrab.grab(dimensions)
# image.show()

# print(dimensions)



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

