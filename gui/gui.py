from tkinter import *
from tkcalendar import DateEntry
from threading import Thread
from datetime import date
from win32api import GetSystemMetrics
from selenium.common.exceptions import WebDriverException 

import tkinter.messagebox as msgbox

_WEB_URL = "https://www.saramin.co.kr/zf_user/jobs/recent-contents/recruiter-interviews?page={}"
_DATE_XPATH = '//*[@id="jobboard_basic"]/tbody//tr/td[1]'
_COMPANY_XPATH = '//*[@id="jobboard_basic"]/tbody//tr/td[4]/a[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{}")]'

def _highlight_compay_text(wdriver, company):
    xpath = _COMPANY_XPATH.format(company.lower())
    elements = wdriver.find_elements_by_xpath(xpath)
    for element in elements:
        parent = element._parent
        style = "background: yellow; color: blue; font-weight: bold;"
        parent.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)

def _worker_thread1(target, wdriver, page_num, search_txt):
    page = page_num
    while target.do_action:

        try:
            wdriver.get(_WEB_URL.format(page))
        except WebDriverException:
            msgbox.showerror("오류", "웹 브라우저를 제어 할 수 없습니다.\n 프로그램을 다시 실행 시켜주세요")
            target.window_quit()
            break

        dates = wdriver.find_elements_by_xpath(_DATE_XPATH)
        
        dates = [ d.text for d in dates]
        dates = list(filter(lambda x: x != 'TODAY', dates))

        # 검색할 회사 찾았으면 하이라이트 하고 멈춤
        companys = wdriver.find_elements_by_xpath(_COMPANY_XPATH.format(search_txt.lower()))
        if len(companys) > 0:
            _highlight_compay_text(wdriver, search_txt)
            msgbox.showinfo("성공", "{}의 인사통을 찾았습니다.".format(search_txt))
            break

        # 아니면 여기서 브레이크
        if len(dates) > 0:
            msgbox.showerror("오류", "{}의 인사통을 찾을 수 없습니다".format(search_txt))
            break
        page = page + 1

def _worker_thread2(target, wdriver, page_num, search_date, search_txt):
    page = page_num
    search_date = int(search_date.replace("-",""))
    while target.do_action:

        try:
            wdriver.get(_WEB_URL.format(page))
        except WebDriverException:
            msgbox.showerror("오류", "웹 브라우저를 제어 할 수 없습니다.\n 프로그램을 다시 실행 시켜주세요")
            target.window_quit()
            break

        dates = wdriver.find_elements_by_xpath(_DATE_XPATH)
        dates = [int(d.text.split('\n')[0].replace("-","")) for d in dates if d.text != 'TODAY']
        dates = list(filter(lambda x: x < search_date, dates))

        # 검색할 회사 찾았으면 하이라이트 하고 멈춤
        companys = wdriver.find_elements_by_xpath(_COMPANY_XPATH.format(search_txt.lower()))
        if len(companys) > 0:
            _highlight_compay_text(wdriver, search_txt)
            msgbox.showinfo("성공", "{}의 인사통을 찾았습니다.".format(search_txt))
            break

        # 아니면 여기서 브레이크
        if len(dates) > 0:
            msgbox.showerror("오류", "{}의 인사통을 찾을 수 없습니다".format(search_txt))
            break
        page = page + 1

class InsatongGUI:

    def __init__(self, webdriver):
        # data variable 
        self.__page_num = 1
        self.__webdriver = webdriver
        self.__do_action = False

        # initial request for url
        request_url = _WEB_URL.format(self.__page_num)
        self.__webdriver.get(request_url)

        self.__root = Tk()
        posX, posY = int(GetSystemMetrics(0) / 3), int(GetSystemMetrics(1) / 3)

        self.__root.title("최근 인사통 Helper")
        self.__root.geometry("270x350+{}+{}".format(posX, posY))
        self.__root.resizable(True, True)

        date_frame = LabelFrame(self.__root, text="검색 시작일", padx=20, pady=10)
        date_frame.place(x=50, y=30)

        self.__cal = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="y-mm-dd")
        self.__cal.pack(padx=10, pady=10)

        serach_frame = LabelFrame(self.__root, text="회사명", padx=10, pady=20)
        serach_frame.place(x=50, y=110)

        self.__search_txt = Entry(serach_frame, width=20)
        self.__search_txt.pack()

        page_frame = LabelFrame(self.__root, text="검색 시작 페이지", padx=10, pady=20)
        page_frame.place(x=50, y=190)

        self.__page_txt = Entry(page_frame, width=20)
        self.__page_txt.bind("<Return>", self.__page_move_event)
        self.__page_txt.pack()
        self.__page_txt.insert(0, str(self.__page_num))

        button_frame = Frame(self.__root, width=100, height=50)
        button_frame.place(x=50, y=270)

        # define buttons
        active_btn = Button(button_frame,text="실행", width=9, height=3, padx=5 ,command=self.__active_btn_event)
        active_btn.bind("<Return>", self.__active_btn_event)
        active_btn.grid(row=0, column=0)

        stop_btn = Button(button_frame,text="중지", width=9, height=3, padx=5 ,command=self.__action_stop_event)
        stop_btn.bind("<Return>", self.__action_stop_event)
        stop_btn.grid(row=0, column=1, padx=5)

        self.__root.mainloop();

    def window_quit(self):
        self.__root.destroy()

    @property
    def do_action(self):
        return self.__do_action

    @do_action.setter
    def do_action(self, isdo):
        self.__do_action = isdo
    
    def __active_btn_event(self, *args):
        sys_date = str(date.today())
        search_date = str(self.__cal.get_date())
        search_txt = self.__search_txt.get().strip()
        self.do_action = True

        if len(search_txt) == 0:
            msgbox.showwarning("확인", "회사명을 입력해주세요")
            return

        input_page = self.__page_txt.get().strip()
        try:
            self.__page_num = int(input_page)
        except ValueError:
            msgbox.showerror("오류", "숫자가 아닌 값이 입력되었습니다")
            self.__page_txt.delete(0, END)
            self.__page_txt.insert(0, str(self.__page_num))
            return
            
        if search_date == sys_date:
            job = Thread(target=_worker_thread1, args=(self, self.__webdriver, self.__page_num, search_txt))
            job.start()
        else:
            job = Thread(target=_worker_thread2,  args=(self, self.__webdriver, self.__page_num, search_date, search_txt))
            job.start()
    
    def __page_move_event(self, *args):
        input_page = self.__page_txt.get().strip()
        try:
            self.__page_num = int(input_page)
        except ValueError:
            msgbox.showerror("오류", "숫자가 아닌 값이 입력되었습니다")
            self.__page_txt.delete(0, END)
            self.__page_txt.insert(0, str(self.__page_num))
            return
        
        request_url = _WEB_URL.format(self.__page_num)

        try:
            self.__webdriver.get(request_url)
        except WebDriverException:
            msgbox.showerror("오류", "웹 브라우저를 제어 할 수 없습니다.\n 프로그램을 다시 실행 시켜주세요")
            self.window_quit()

    def __action_stop_event(self, *args):
        self.do_action = False
        msgbox.showwarning("확인", "탐색이 중지 되었습니다.")
