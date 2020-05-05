'''
Created on 2020年4月29日

@author: zhangtangzhao
'''
# -*- coding: utf-8 -*-
import os
import win32crypt
import sqlite3
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SOUR_COOKIE_FILENAME = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Cookies'
DIST_COOKIE_FILENAME = '.\python-chrome-cookies'


def get_string( local_state ):
    with open( local_state, 'r', encoding='utf-8' ) as f:
        s = json.load( f )['os_crypt']['encrypted_key']
    return s

##  将本地cookie的key进行解密
def pull_the_key( base64_encrypted_key ):
    encrypted_key_with_header = base64.b64decode( base64_encrypted_key )
    encrypted_key = encrypted_key_with_header[5:]
    key = win32crypt.CryptUnprotectData( encrypted_key, None, None, None, 0 )[1]
    return key

# 将cookie的值进行解密
def decrypt_string( key, data ):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM( key )
    plainbytes = aesgcm.decrypt( nonce, cipherbytes, None )
    plaintext = plainbytes.decode( 'utf-8' )
    return plaintext

## 获取本地的cookie信息
def get_cookie_from_chrome( host: '.51cto.com' ):
    local_state = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    cookie_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"

    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host

    with sqlite3.connect( cookie_path ) as conn:
        cu = conn.cursor()
        res = cu.execute( sql ).fetchall()
        cu.close()
        cookies = {}
        key = pull_the_key( get_string( local_state ) )
        for host_key, name, encrypted_value in res:
            if encrypted_value[0:3] == b'v10':
                cookies[name] = decrypt_string( key, encrypted_value )
            else:
                cookies[name] = win32crypt.CryptUnprotectData( encrypted_value )[1].decode()

        # print(cookies)
        return cookies

## 将cookie对象封装成key=value;的字符串
def cookie_str():
    dict_cookie = get_cookie_from_chrome( '.51cto.com' )
    cs = dict_cookie.items()
    cookie = ''
    for name, value in cs:
        cookie += '{0}={1};'.format( name, value )
    return cookie

