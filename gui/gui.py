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

def _worker_thread1(wdriver, search_txt):
    page = 1
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

def _worker_thread2(wdriver, search_date, search_txt):
    page = 1
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
        root.geometry("480x200+{}+{}".format(posX, posY))
        root.resizable(False, False)

        date_frame = LabelFrame(root, text="검색 시작일", padx=20, pady=10)
        date_frame.place(x=50, y=30)

        self.__cal = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="y-mm-dd")
        self.__cal.pack(padx=10, pady=10)

        serach_frame = LabelFrame(root, text="회사명", padx=10, pady=20)
        serach_frame.place(x=250, y=30)

        self.__search_txt = Entry(serach_frame, width=20)
        self.__search_txt.pack()

        button_frame = Frame(root, width=100, height=50)
        button_frame.place(x=160, y=130)

        # define buttons
        active_btn = Button(button_frame,text="실행", width=10, height=3, command=self.__active_btn_event)
        active_btn.bind("<Return>", self.__active_btn_event)
        active_btn.grid(row=0, column=0, padx=30)
        root.mainloop();
    
    def __active_btn_event(self, *args):
        sys_date = str(date.today())
        search_date = str(self.__cal.get_date())
        search_txt = self.__search_txt.get().strip()

        if len(search_txt) == 0:
            msgbox.showwarning("확인", "회사명을 입력해주세요")
            return

        if search_date == sys_date:
            job = Thread(target=_worker_thread1, args=(self.__webdriver, search_txt))
            job.start()
        else:
            job = Thread(target=_worker_thread2,  args=(self.__webdriver, search_date, search_txt))
            job.start()