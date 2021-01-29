from tkinter import *
import tkinter.messagebox as msgbox

from win32api import GetSystemMetrics

WEB_URL = "https://www.saramin.co.kr/zf_user/jobs/recent-contents/recruiter-interviews?page={}&max_entry={}"
class InsatongGUI:
    
    
    def __init__(self, webdriver):
        # data variable 
        self.page_num = 1
        self.data_cnt = 50
        self.webdriver = webdriver

        # initial request for url
        request_url = WEB_URL.format(self.page_num, self.data_cnt)
        self.webdriver.get(request_url)

        root = Tk()
        posX, posY = int(GetSystemMetrics(0) / 3), int(GetSystemMetrics(1) / 3)

        root.title("최근 인사통 Helper")
        root.geometry("300x200+{}+{}".format(posX, posY))
        root.resizable(False, False)

        page_frame = LabelFrame(root, text="페이지", padx=20, pady=10)
        page_frame.place(x=50, y=30)

        self.page_txt = Entry(page_frame, width=5)
        self.page_txt.insert(END, str(self.page_num)) # set pagenum into page_txt
        self.page_txt.bind("<Return>", self.page_txt_event) # enter key bind into page_txt
        self.page_txt.pack()

        data_cnt_frame = LabelFrame(root, text="출력 데이터 수", padx=10, pady=10)
        data_cnt_frame.place(x=150, y=30)

        self.data_cnt_txt = Entry(data_cnt_frame, width=5)
        self.data_cnt_txt.insert(END, str(self.data_cnt)) # set data count into data_cnt_txt
        self.data_cnt_txt.bind("<Return>", self.page_cnt_event) # enter key bind into data_cnt_txt
        self.data_cnt_txt.pack()

        button_frame = Frame(root, width=100, height=50)
        button_frame.place(x=50, y=100)

        # define buttons
        prev_btn = Button(button_frame,text="이전", width=10, height=3, command=self.prev_btn_event)
        prev_btn.bind("<Return>", self.prev_btn_event)
        prev_btn.grid(row=0, column=0, padx=10)

        next_btn = Button(button_frame, text="다음", width=10, height=3, command=self.next_btn_event)
        next_btn.bind("<Return>", self.next_btn_event)
        next_btn.grid(row=0, column=1)
        root.mainloop();
    
    def page_txt_event(self, *args):
        '''
        페이지 번호 입력 위젯 처리
        '''
        try:
            page_num = int(self.page_txt.get())
            self.page_num = page_num
            self.data_cnt_txt.delete(0, END)
            self.data_cnt_txt.insert(END, str(self.data_cnt))

            request_url = WEB_URL.format(self.page_num, self.data_cnt)
            self.webdriver.get(request_url)
            
        except ValueError:
            msgbox.showerror("오류", "숫자가 아닌 값이 입력되었습니다.")
            self.page_txt.delete(0, END)
            self.page_txt.insert(END, str(self.page_num))

    def page_cnt_event(self, *args):
        '''
        출력 데이터 수 입력 위젯 처리
        '''
        try:
            data_cnt = int(self.data_cnt_txt.get())
            self.data_cnt = data_cnt
            self.page_txt.delete(0, END)
            self.page_txt.insert(END, str(self.page_num))

            request_url = WEB_URL.format(self.page_num, self.data_cnt)
            self.webdriver.get(request_url)
        except ValueError:
            msgbox.showerror("오류", "숫자가 아닌 값이 입력되었습니다.")
            self.data_cnt_txt.delete(0, END)
            self.data_cnt_txt.insert(END, str(self.data_cnt))

    def prev_btn_event(self, *args):
        '''
        이전 페이지 버튼 이벤트 처리
        '''
        self.page_num = self.page_num - 1
        if self.page_num <= 1:
            self.page_num = 1

        request_url = WEB_URL.format(self.page_num, self.data_cnt)
        self.webdriver.get(request_url)

    def next_btn_event(self, *args):
        '''
        다음 페이지 버튼 이벤트 처리
        '''
        self.page_num = self.page_num + 1

        request_url = WEB_URL.format(self.page_num, self.data_cnt)
        self.webdriver.get(request_url)


if __name__ == "__main__":
    InsatongGUI()
