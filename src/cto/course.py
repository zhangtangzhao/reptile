# -*- coding: utf-8 -*-
'''
Created on 2020年4月29日

@author: zhangtangzhao
'''

import requests
import json
import time
import os
from cto import signUtil
from cto import cookieUtil
from cto import download

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
}

cookie = cookieUtil.cookie_str()
headers['cookie'] = cookie

##java架构 train_id:309
def course_list(train_id,page=1,size=100):
    url = "https://edu.51cto.com/center/wejob/user/train-course-ajax?train_id="+train_id+"&page="+page+"&size="+size
    
    content = str( requests.get( url, headers=headers ).content, encoding='utf-8' )
    courses = json.loads( content ).get( 'data' ).get( 'data' )
    return courses

## 获取课程章节列表
def video_list( train_course_id,page,size ):
    url = "https://edu.51cto.com/center/wejob/user/course-info-ajax?page="+page+"&size="+size+"&train_course_id=" + train_course_id

    content = str( requests.get( url, headers=headers ).content, encoding='utf-8' )
    videos = json.loads( content ).get( 'data' ).get('data')
    return videos


#  根据lession_id 获取m3u8文件的请求url
#  lession_id = train_course_id + lesson_id
def lession_m3u8( lession_id ):
    sign = signUtil.sign_key( lession_id )
    url = "https://edu.51cto.com/center/player/play/get-lesson-info?type=wejoboutcourse&lesson_id=" + lession_id + "&sign=" + sign
    content = str( requests.get( url, headers=headers ).content, encoding='utf-8' )
    m3u8_url = json.loads( content ).get( 'dispatch' )[0]['url']
    return m3u8_url

#print(lession_m3u8("1050_219907"))
train_course_id = "1055"
try:
    for i in range(1,9):
        datas = video_list(train_course_id,str(i),"20")
        for d in datas:
            data_list = d.get("list")
            chapter_sort = d.get("chapter_sort")
            chapter_name = d.get("chapter_name")
            chapter = "第"+chapter_sort+"章"+chapter_name
            if isinstance(data_list,dict):
                for key in data_list.keys():
                    
                    value = data_list.get(key)
                    exam_type = value.get("exam_type")
                    if exam_type == 1:
                        continue
                    lesson_name = value.get("lesson_name").replace(" ","-")
                    lesson_name = lesson_name.replace("**","")
                    show_number = value.get("show_number")
                    print(show_number+lesson_name)
                    lesson_id = value.get("lesson_id")
                    if os.path.isdir("E:/1/"+show_number+lesson_name) == False:
                        time.sleep(10)
                        m3u8_url = lession_m3u8(train_course_id+"_"+str(lesson_id))
                        download.query_m3u8(m3u8_url,show_number+lesson_name,chapter)
            elif isinstance(data_list,list):
                for data in data_list:
                    exam_type = data.get("exam_type")
                    if exam_type == 1:
                        continue
                    lesson_name = data.get("lesson_name").replace(" ","-")
                    lesson_name = lesson_name.replace("**","")
                    show_number = data.get("show_number")
                    print(show_number+lesson_name)
                    lesson_id = data.get("lesson_id")
                    if os.path.isdir("E:/1/"+show_number+lesson_name) == False:
                        time.sleep(10)
                        m3u8_url = lession_m3u8(train_course_id+"_"+str(lesson_id))
                        download.query_m3u8(m3u8_url,show_number+lesson_name,chapter)
            else:
                print("--------::"+data_list)
except Exception as e:
    print(e)    


