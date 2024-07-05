from . import tk
from . import data
from . import downloader

DOWN_PART_BASE_ROW = 4

window = tk.Tk()
msg_list = tk.Listbox(window, width=45, height=35, font=("", 10))
open_excel_button = tk.Button( window,
    text="載入Excel"
)
open_scv_button = tk.Button( window,
    text="載入SCV"
)
start_download_github_buton= tk.Button(window,
                                text="用Github網址下載", bg="#CCFFCC")
start_download_github_account_button = tk.Button(window,
                                                 text="用Github帳號名稱下載", bg="#DDFFDD")
start_download_target_file_button = tk.Button(window,
                                              text = "直接下載目標檔案")
start_download_youtube_button = tk.Button(window,
                                          text="下載Youtube影片(未完成)", bg="#FFDDDD")
select_save_path_buton = tk.Button(window,
                                   text="選擇儲存路徑")
# Entry ..........................................................
save_path_entry = tk.Entry(window, width=30)
loaded_file_entry = tk.Entry(window, width=40, state="readonly")
file_name_entry = tk.Entry(window, width=35)
repository_name_entry = tk.Entry(window, width=35)

# Spinbox ........................................................
url_index_spinbox = tk.Spinbox( window, from_=0, increment=1, to=4294967296, width=33 )
skip_row_number_spinbox = tk.Spinbox( window, from_=0, increment=1, to=4294967296, width=10 )

# 預覽表格 ..........................................................
table_size = (30, 10)
table_var = [[tk.StringVar(window) for x in range(table_size[1])]
             for y in range(table_size[0])]
table_entry = [[tk.Entry(window, textvariable=table_var[x][y], width=14, font=("", 10), state="readonly")
                for y in range(table_size[1])] for x in range(table_size[0])]
table_index_label = [ tk.Label(window, text="({0})".format(x)) for x in range(table_size[1]) ]
#---------------------------------------------------------
def init():
    window.title("Files Downloader")
    
    msg_list.grid(column=0, row=DOWN_PART_BASE_ROW, columnspan=3, rowspan=table_size[0])

    open_excel_button.grid(column=0, row=1)
    open_excel_button.config(command=data.select_excel)
    open_scv_button.grid(column=1, row=1)
    open_scv_button.config( command=data.select_csv )
    select_save_path_buton.grid(column=2, row=1)
    select_save_path_buton.config( command=data.select_saved_path )
    start_download_github_buton.grid(column=3, row=1, columnspan=2)
    start_download_github_buton.config( command=downloader.download_github_by_url )
    start_download_github_account_button.grid(column=3, row=2, columnspan=2)
    start_download_github_account_button.config( command=downloader.download_github_by_account )
    start_download_target_file_button.grid( column=3, row=0, columnspan=2 )
    start_download_target_file_button.config( command=downloader.download_file_from_url )
    #start_download_youtube_button.grid(column=3, row=0, columnspan=2)

    tk.Label(window, text="儲存路徑").grid(column=0, row=0)
    tk.Label(window, text="Github Repository名稱", relief="solid", bd=1, width=24, anchor="e").grid(column=5,row=2, columnspan=2)
    tk.Label(window, text="檔案命名格式", relief="solid", bd=1, width=24, anchor="e").grid(column=5, row=0, columnspan=2)
    tk.Label(window, text="URL(或帳號)欄位編號", relief="solid", bd=1, width=24, anchor="e").grid(column=5, row=1, columnspan=2)
    tk.Label(window, text="跳過列數量", relief="solid", bd=1, width=12, anchor="e").grid(column=10,row=0, columnspan=1)

    repository_name_entry.grid(column=6, row=2, columnspan=5)
    repository_name_entry.config( textvariable=data.github_repository_name )
    file_name_entry.grid(column=7, row=0, columnspan=3)
    file_name_entry.config( textvariable=data.file_name_format )
    save_path_entry.grid(column=1, row=0, columnspan=2)
    save_path_entry.config( textvariable=data.saved_path )
    loaded_file_entry.grid(column=0, row=2, columnspan=3)
    loaded_file_entry.config( textvariable=data.loaded_file_path )
    
    url_index_spinbox.grid( column=7, row=1, columnspan=3 )
    url_index_spinbox.config( textvariable=data.url_index )
    skip_row_number_spinbox.grid( column=11, row=0, columnspan=1 )
    skip_row_number_spinbox.config( textvariable=data.skip_row_number )

    for i in range(table_size[1]):
        table_index_label[i].grid(column=i+3, row=DOWN_PART_BASE_ROW-1)
    for x in range( table_size[0] ):
        for y in range( table_size[1] ):
            table_entry[x][y].grid(column=y+3, row=x+DOWN_PART_BASE_ROW)
    window.resizable( False, False )
#---------------------------------------------------------
def msg(msg_content:str):
    msg_list.insert(0, msg_content)
#---------------------------------------------------------