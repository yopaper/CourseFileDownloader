from . import data
from . import uiBuilder
from . import os
from . import requests
from . import Timer
from math import sqrt
#-------------------------------------------
GITHUB_TAIL_URL = "/archive/refs/heads/main.zip"

# 下載指定網路檔案, 並儲存為檔案
def download_web_file( file_path:str, url:str ):
    uiBuilder.msg("開始下載此檔案:{0}".format(url))
    response = requests.get( url )
    file_writer = open( file_path, "wb" )
    file_writer.write( response.content )
    file_writer.close()
    uiBuilder.msg("儲存於:{0}".format(file_path))
#-------------------------------------------------------
# 開始下載的開始步驟
def start_download():
    uiBuilder.msg("-----------------------------")
    uiBuilder.msg("開始下載檔案!")
    uiBuilder.msg("完成前請勿進行其他操作!")
    check_save_path()
#-------------------------------------------------------
def download_github_by_url():
    def download_thread(index:int, none_counter:int, none_limit:int):
        try:
            current_row = data.file_data[index]
            filename = combine_file_name( name_format, col_index, current_row, ".zip")
            github_url = current_row[ url_index ]
            if( filename != None and github_url != None ):
                if( GITHUB_TAIL_URL not in github_url ):
                    github_url += GITHUB_TAIL_URL
                download_web_file( filename, github_url )
                none_counter = 0
            else:
                none_counter += 1
                uiBuilder.msg( "空列資料:{0}/{1}".format(none_counter, none_limit) )

        except Exception as e:
            uiBuilder.msg( "單一檔案下載失敗!" )
        
        if( index < data_number-1 and none_counter<none_limit):
            t = Timer(0.001, download_thread, (index+1,none_counter, none_limit))
            t.start()
        else:
            uiBuilder.msg("下載完成!")
    #.................................................
    try:
        start_download()
        name_format, col_index = get_github_filename_format_index()
        data_number = len( data.file_data )
        url_index = data.url_index.get()

        t = Timer( 0.5, download_thread, (data.skip_row_number.get(), 0, get_none_data_limiting()) )
        t.start()
    except Exception as e:
        uiBuilder.msg( str(e) )
        uiBuilder.msg("下載失敗! 下載終止!")
#-------------------------------------------
def download_github_by_account():
    def download_thread(index:int, none_counter:int, none_limit:int):
        row_data = data.file_data[index]
        try:
            filename = combine_file_name( name_format, col_index, row_data, ".zip" )
            acount_name = row_data[ data.url_index.get() ]
            if( filename!=None and acount_name!=None ):
                github_url = url_format.format( acount_name, repository_name )
                download_web_file( filename, github_url )
                none_counter = 0
            else:
                none_counter += 1
                uiBuilder.msg( "空列資料:{0}/{1}".format(none_counter, none_limit) )
            
        except Exception as e:
            uiBuilder.msg( "單一檔案下載失敗!" )

        if( index < data_number - 1 and none_counter<none_limit ):
            t = Timer( 0.001, download_thread, (index+1, none_counter, none_limit) )
            t.start()
        else:
            uiBuilder.msg("下載完成!")
    #.................................................
    try:
        start_download()
        url_format = "https://github.com/{0}/{1}/archive/refs/heads/main.zip"
        name_format, col_index = get_github_filename_format_index()
        data_number = len( data.file_data )
        repository_name = data.github_repository_name.get()
        
        t = Timer( 0.5, download_thread, (data.skip_row_number.get(), 0, get_none_data_limiting()) )
        t.start()
    except Exception as e:
        uiBuilder.msg( str(e) )
        uiBuilder.msg("下載失敗! 下載終止!")
#-------------------------------------------
def check_save_path():
    save_path = data.saved_path.get()
    if( not os.path.exists(save_path) ):
        uiBuilder.msg("儲存路徑不存在, 已為您建立")
        os.makedirs( save_path )
#-------------------------------------------
def combine_file_name(
        name_format:str, index_set:list,
        row_data:list, tail_filename:str="" )->str:
    col_content = []
    for i in index_set:
        col = row_data[i]
        if( col == None or col == "" ):return None
        col_content.append( col )
    return name_format.format( *col_content ) + tail_filename
#-------------------------------------------
def get_github_filename_format_index()->(str, list[int]):
    name_format, col_index = split_filename_format()
    name_format = os.path.join( data.saved_path.get(), name_format )
    return name_format, col_index
#-------------------------------------------
def split_filename_format()->(str, list[int]):
    format_error = Exception("檔案名稱格式錯誤!")
    filename = data.file_name_format.get()
    col_index = []; splitname = []
    current_index = ""; current_split = ""
    front_trigger = False
    for i in range( len(filename) ):
        current_char = filename[i]
        if( current_char == '{' ):
            if( front_trigger == False ):
                front_trigger = True
                current_split += current_char
                splitname.append( current_split )
                current_split = ""
            else: # 異常
                uiBuilder.msg("在出現 \'}\' 前出現第二個 \'{\'")
                raise format_error
        elif( current_char == '}' ):
            if( front_trigger==True ):
                front_trigger = False
                current_split += current_char
                if( not current_index.isdigit() ):
                    uiBuilder.msg("{ }內的必須是大於等於0的整數")
                    raise format_error
                col_index.append(int(current_index))
                current_index = ""
            else: # 異常
                uiBuilder.msg("在出現 \'{\' 前出現 \'}\'")
                raise format_error
        else:
            if( front_trigger ):
                current_index += current_char
            else:
                current_split += current_char
    # End For
    splitname.append( current_split )
    format_name = splitname[0]
    for i in range( 1, len(splitname) ):
        format_name += str(i-1)
        format_name += splitname[i]
    return (format_name, col_index)
#-------------------------------------------
def get_none_data_limiting()->int:
    return round( sqrt( len( data.file_data )+1 )+2 )
#-------------------------------------------