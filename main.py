from gui.gui import InsatongGUI
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from win32api import GetSystemMetrics

import selenium
import tkinter.messagebox as msgbox
import selenium.webdriver as webdriver


if __name__ == '__main__':
    try:
        size_opt = "--window-size={},{}".format(GetSystemMetrics(0), GetSystemMetrics(1))
        opts = Options()
        opts.add_argument(size_opt)
        wdriver = webdriver.Chrome(options=opts, executable_path='driver/chromedriver.exe')
        InsatongGUI(wdriver)
    except OSError as e:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        msgbox.showerror("오류", "chromedriver.exe 파일 경로나 버전을 확인해주세요")
    