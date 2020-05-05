# -*- coding: utf-8 -*-
import os


def openssl_cmd( filePath, outfilePath, iv, key ):
    cmd = 'openssl aes-128-ecb -d -in '
    cmd = cmd + filePath
    cmd = cmd + ' -out '
    cmd = cmd + outfilePath
    cmd = cmd + ' -nosalt -iv '
    cmd = cmd + iv
    cmd = cmd + ' -K '
    cmd = cmd + key
    res = os.popen( cmd )
    output_str = res.read()
    print( output_str )

def ffmpeg_cmd(filePath,outFilePath):
    cmd = 'ffmpeg -f concat -i '
    cmd = cmd + filePath
    cmd = cmd + ' -c copy '
    cmd = cmd + outFilePath
    res = os.popen( cmd )
    output_str = res.read()
    print( output_str )
    
#ffmpeg_cmd("E:/1/decode/file.txt", "E:/1/1.mp4")