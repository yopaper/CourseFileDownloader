import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

import requests
from threading import Timer
import openpyxl
import openpyxl.worksheet.worksheet as worksheet
import os

from fileDownloader import uiBuilder
from fileDownloader import data
from fileDownloader import downloader

data.init()
uiBuilder.init()
data.display_file_data()
uiBuilder.msg("https://github.com/yopaper/CourseFileDownloader")
uiBuilder.msg("使用教學在以下網站")
uiBuilder.msg("========================")
uiBuilder.msg("111598023 梁佑駿")
uiBuilder.msg("臺北科技大學 電腦圖學實驗室")
uiBuilder.msg("開發者:")
uiBuilder.msg("歡迎使用學生作品下載程式")
uiBuilder.msg("========================")

downloader.check_save_path()

tk.mainloop()