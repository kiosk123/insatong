import selenium
from gui.gui import InsatongGUI
from selenium.webdriver import ChromeOptions
import tkinter.messagebox as msgbox
import selenium.webdriver as webdriver

if __name__ == '__main__':
    try:
        wdriver = webdriver.Chrome(executable_path='driver/chromedriver.exe')
        InsatongGUI(wdriver)
    except OSError as e:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        msgbox.showerror("오류", "chromedriver.exe 파일 경로나 버전을 확인해주세요")
    