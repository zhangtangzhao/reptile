# -*- coding: utf-8 -*-
import requests
import re
import os
import time
from lxml.html import etree
from cto import cmd as cmdUtil
from cto import signUtil
from cto import binHexUtil
from cto import jsutil
from cto import cookieUtil

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}

cookie = cookieUtil.cookie_str()
headers['cookie'] = cookie

## 根据文件的url下载ts文件并通过openssl界面
def download_file( url, download_path, decode_path, iv, key ):
    resp = requests.get( url ,headers=headers)
    filename = url.split( "/" )[-1]
    content = resp.content
    download_path = download_path + "/" + filename
    decode_path = decode_path + "/" + filename
    with open( download_path, 'wb' ) as f:
        f.write( content )
    # #解密
    cmdUtil.openssl_cmd( download_path, decode_path, iv, key )
    return filename


## 根据m3u8的地址返回并解析信息
def query_m3u8( url,name,chapter ):
#     m3u8 = open( file_path, 'r' )
#     print( m3u8 )
    content = requests.get(url,headers=headers).content
    header_url = 'https://edu.51cto.com'
    title = name.encode('utf-8').decode('utf-8')
    chapter = chapter.encode('utf-8').decode('utf-8')
#     lines = m3u8.readlines()
    key = ""
    iv = ""
    lines = str(content,encoding='utf-8').split("\n")
    for line in lines:
        if line.strip('\n').find('EXT-X-KEY') > -1:
            cs = line.split(',')
            ##m3u8中Key的url
            key_url = re.findall(r"URI=\"(.*)\"", cs[1])[0]
            ##提取lession_id
            lession_id = re.findall(r".*lesson_id=(.*)&id=.*", key_url)[0]
            headers["Referer"]='https://edu.51cto.com/center/course/lesson/index?type=wejob&id='+lession_id
            ##生成请求的sign
            sign_key = signUtil.sign_key(lession_id)
            url = header_url+key_url+"&sign="+sign_key
            resp_content = requests.get(url,headers=headers).content
            content = str(resp_content,encoding='utf-8')
            ##解密
            key = binHexUtil.base(jsutil.decode(content, lession_id))
            iv = re.findall(r"IV=0x(.*)", cs[2])[0]
#             title = query_title(lession_id)
        elif line.strip( '\n' ).find( ".ts" ) > -1:
            url = line.strip( '\n' )
            print( url )
            if os.path.isdir("E:/1/"+title+"/download") == False:
                os.makedirs("E:/1/"+title+"/download")
            if os.path.isdir("E:/1/"+title+"/decode") == False:
                os.makedirs("E:/1/"+title+"/decode")
            print("download start .....")
            decode_path = download_file( url, "E:/1/"+title+"/download", "E:/1/"+title+"/decode", iv, key )
            print("download end .....")
            content = "file '" + decode_path + "'\n"
            print("decode start...")
            write_file( "E:/1/"+title+"/decode/file.txt", content )
            print("decode end...")
    if os.path.isdir("E:/1/out/"+chapter) == False:
        os.makedirs("E:/1/out/"+chapter)
    print("ffmpeg start...")
    cmdUtil.ffmpeg_cmd("E:/1/"+title+"/decode/file.txt", "E:/1/out/"+chapter+"/"+title+".mp4")
    print("ffmpeg end...")        

## 将内容写入指定的文件
def write_file( file_path, content ):
    with open( file_path, "a" ) as file:
        file.write( content )

## 查询视频的文件名        
def query_title(lession_id):
    url = "https://edu.51cto.com/center/course/lesson/index?type=wejob&id="+lession_id
    html =  etree.HTML(requests.get(url,headers=headers).text)
    title = html.xpath('//title')[0].text.replace(" ","-")[:-8]
    return title

# query_m3u8("https://edu.51cto.com//center/player/play/m3u8?lesson_id=1059_220059&id=397344&dp=general&type=wejoboutcourse&lesson_type=course","4-4得到特征图表示","第4章卷积神经网络基本原理")
# query_title("https://edu.51cto.com/center/course/lesson/index?id=1449_279516&type=wejob")
# print(os.path.isdir("E:/1/111") )
