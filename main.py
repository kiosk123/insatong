import selenium
from gui.gui import InsatongGUI
import tkinter.messagebox as msgbox
import webview

if __name__ == '__main__':
    try:
        # InsatongGUI(chrome_driver)
    except OSError as e:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        msgbox.showerror("오류", "설정 파일에 크롬 실행경로 설정을 확인해주세요")
    