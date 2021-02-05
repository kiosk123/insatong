from tkinter import *
from tkcalendar import DateEntry
from threading import Thread
from datetime import date
from win32api import GetSystemMetrics

import tkinter.messagebox as msgbox

_WEB_URL = "https://www.saramin.co.kr/zf_user/jobs/recent-contents/recruiter-interviews?page={}"
_DATE_XPATH = '//*[@id="jobboard_basic"]/tbody//tr/td[1]'
_COMPANY_XPATH = '//*[@id="jobboard_basic"]/tbody//tr/td[4]/a[contains(text(),"{}")]'

def _highlight_compay_text(wdriver, company):
    xpath = _COMPANY_XPATH.format(company)
    elements = wdriver.find_elements_by_xpath(xpath)
    for element in elements:
        parent = element._parent
        style = "background: yellow; color: blue; font-weight: bold;"
        parent.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)

def _worker_thread1(wdriver, page_num, search_txt):
    page = page_num
    while True:
        wdriver.get(_WEB_URL.format(page))
        dates = wdriver.find_elements_by_xpath(_DATE_XPATH)
        
        dates = [ d.text for d in dates]
        dates = list(filter(lambda x: x != 'TODAY', dates))

        # 검색할 회사 찾았으면 하이라이트 하고 멈춤
        companys = wdriver.find_elements_by_xpath(_COMPANY_XPATH.format(search_txt))
        if len(companys) > 0:
            _highlight_compay_text(wdriver, search_txt)
            msgbox.showinfo("성공", "{}의 인사통을 찾았습니다.".format(search_txt))
            break

        # 아니면 여기서 브레이크
        if len(dates) > 0:
            msgbox.showerror("오류", "{}의 인사통을 찾을 수 없습니다".format(search_txt))
            break
        page = page + 1

def _worker_thread2(wdriver, page_num, search_date, search_txt):
    page = page_num
    search_date = int(search_date.replace("-",""))
    while True:
        wdriver.get(_WEB_URL.format(page))
        dates = wdriver.find_elements_by_xpath(_DATE_XPATH)
        dates = [int(d.text.split('\n')[0].replace("-","")) for d in dates if d.text != 'TODAY']
        dates = list(filter(lambda x: x < search_date, dates))

        # 검색할 회사 찾았으면 하이라이트 하고 멈춤
        companys = wdriver.find_elements_by_xpath(_COMPANY_XPATH.format(search_txt))
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

        # initial request for url
        request_url = _WEB_URL.format(self.__page_num)
        self.__webdriver.get(request_url)

        root = Tk()
        posX, posY = int(GetSystemMetrics(0) / 3), int(GetSystemMetrics(1) / 3)

        root.title("최근 인사통 Helper")
        root.geometry("270x350+{}+{}".format(posX, posY))
        root.resizable(True, True)

        date_frame = LabelFrame(root, text="검색 시작일", padx=20, pady=10)
        date_frame.place(x=50, y=30)

        self.__cal = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="y-mm-dd")
        self.__cal.pack(padx=10, pady=10)

        serach_frame = LabelFrame(root, text="회사명", padx=10, pady=20)
        serach_frame.place(x=50, y=110)

        self.__search_txt = Entry(serach_frame, width=20)
        self.__search_txt.pack()

        page_frame = LabelFrame(root, text="검색 시작 페이지", padx=10, pady=20)
        page_frame.place(x=50, y=190)

        self.__page_txt = Entry(page_frame, width=20)
        self.__page_txt.bind("<Return>", self.__page_move_event)
        self.__page_txt.pack()
        self.__page_txt.insert(0, str(self.__page_num))

        button_frame = Frame(root, width=100, height=50)
        button_frame.place(x=50, y=270)

        # define buttons
        active_btn = Button(button_frame,text="실행", width=22, height=3, padx=3 ,command=self.__active_btn_event)
        active_btn.bind("<Return>", self.__active_btn_event)
        active_btn.pack()

        root.mainloop();
    
    def __active_btn_event(self, *args):
        sys_date = str(date.today())
        search_date = str(self.__cal.get_date())
        search_txt = self.__search_txt.get().strip()

        if len(search_txt) == 0:
            msgbox.showwarning("확인", "회사명을 입력해주세요")
            return

        if search_date == sys_date:
            job = Thread(target=_worker_thread1, args=(self.__webdriver, self.__page_num, search_txt))
            job.start()
        else:
            job = Thread(target=_worker_thread2,  args=(self.__webdriver, self.__page_num, search_date, search_txt))
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
        self.__webdriver.get(request_url)
