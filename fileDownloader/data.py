from . import tk
from . import os
from . import openpyxl
from . import worksheet
from . import uiBuilder
from . import filedialog
from . import simpledialog

saved_path = None
url_index = None
loaded_file_path = None
file_name_format = None
github_repository_name = None
skip_row_number = None

file_data = [
    ("學號", "姓名", "Github網址"),
    ("0001", "SAMPLE", "https://github.com/yopaper/CourseFileDownloader"),
    ("0002", "TEST", "https://github.com/yopaper/CourseFileDownloader"),
]
def set_file_path(path:str):
    loaded_file_path.set( "載入檔案:{0}".format(path) )
    #uiBuilder.loaded_file_entry.config( text="載入檔案:{0}".format(path) )
#------------------------------------------------
def display_file_data():
    for r in uiBuilder.table_var:
        for v in r:
            v.set("")
    for x in range( len( file_data ) ):
        if( x >= uiBuilder.table_size[0] ):
            break
        for y in range( len( file_data[x] ) ):
            if( y >= uiBuilder.table_size[1] ):
                break
            if( file_data[x][y]==None ):continue
            uiBuilder.table_var[x][y].set( file_data[x][y] )
#-------------------------------------------------
def select_saved_path():
    uiBuilder.msg("選擇儲存路徑")
    saved_path.set( filedialog.askdirectory() )
    uiBuilder.msg("儲存路徑設為:{0}".format(saved_path.get()))
#-------------------------------------------------
def select_excel():
    def load_excel()->tuple[openpyxl.Workbook, str]:
        excel_path = filedialog.askopenfile().name
        if( os.path.exists(excel_path) ):
            print("File Exists!")
            uiBuilder.msg( "載入檔案:{0}".format(excel_path) )
        return openpyxl.load_workbook( excel_path ), excel_path
    #...............................................
    def load_worksheet():
        def multi_sheet()->worksheet.Worksheet:
            i = 0
            for s in work_book.worksheets:
                sheet_msg += "({0}):{1}\n".format(i, s.title)
                i += 1
            sheet_msg = "總共有{0}個工作表\n{1}\n".format(worksheet_num, sheet_msg)
            +"請輸入要載入的工作表編號"
            index = simpledialog.askinteger("輸入", sheet_msg)
        #.............................................
        def single_sheet()->worksheet.Worksheet:
            uiBuilder.msg("此檔案只有一個工作表, 載入該工作表")
            return work_book.worksheets[0]
        #.............................................
        worksheet_num = len( work_book.worksheets )
        if( worksheet_num==1 ):
            return single_sheet()
        elif( worksheet_num>1 ):
            return multi_sheet()
        uiBuilder.msg("此檔案無任何工作表")
        return None
    #...............................................
    def load_data():
        file_data.clear()
        for r in loaded_sheet.rows:
            row_data = []
            for c in r:
                cell_data = c.value
                if( type(cell_data)==float and float.is_integer(cell_data) ):
                    cell_data = round( cell_data )
                row_data.append( cell_data )
            file_data.append( row_data )
    #...............................................
    try:
        uiBuilder.msg("-----------------------------")
        uiBuilder.msg("選擇Excel檔")
        work_book, excel_path = load_excel()
        loaded_sheet = load_worksheet()
        if( loaded_sheet==None ):return
        load_data()
        display_file_data()
        set_file_path( excel_path )
        uiBuilder.msg("右方為檔案預覽畫面")
        uiBuilder.msg("共有{0}筆資料".format( len(file_data) ))
        uiBuilder.msg("載入完成!")
    except Exception as e:
        uiBuilder.msg("載入失敗!")
        uiBuilder.msg(str(e))
        raise Exception( str(e) )
#-------------------------------------------------
def select_csv():
    def open_csv_file()->str:
        csv_path = filedialog.askopenfile().name
        return csv_path
    #..............................................
    def load_file():
        file_data.clear()
        with open( file=file_path, mode="r" )as file_reader:
            while(True):
                line_content = file_reader.readline()
                if( line_content==None or len( line_content ) <= 0 ):break
                print( line_content )
                row_data = line_content.split( "," )
                file_data.append( row_data )
    #..............................................
    try:
        uiBuilder.msg("-----------------------------")
        uiBuilder.msg("選擇 CSV 檔")
        file_path = open_csv_file()
        load_file()
        display_file_data()
        set_file_path( file_path )
    except Exception as e:
        uiBuilder.msg("載入失敗!")
        uiBuilder.msg(str(e))
        raise Exception( str(e) )
#-------------------------------------------------
def init():
    global saved_path, loaded_file_path, file_name_format
    global github_repository_name, url_index, skip_row_number
    saved_path = tk.StringVar( uiBuilder.window )
    saved_path.set("./SaveFiles/")
    loaded_file_path = tk.StringVar( uiBuilder.window )
    loaded_file_path.set("尚未載入檔案")
    file_name_format = tk.StringVar( uiBuilder.window )
    file_name_format.set("{0}_{1}")
    github_repository_name = tk.StringVar( uiBuilder.window )
    github_repository_name.set("用Github帳號下載需指定Repository")
    url_index = tk.IntVar( uiBuilder.window )
    url_index.set(2)
    skip_row_number = tk.IntVar( uiBuilder.window )
    skip_row_number.set(1)
#-------------------------------------------------