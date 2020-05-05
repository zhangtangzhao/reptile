'''
Created on 2020年4月28日

@author: zhangtangzhao
'''
# -*- coding: utf-8 -*-
from cto import binHexUtil

def sign_key(lid):
    oriralSign = "eDu_51Cto_siyuanTlw"
    return binHexUtil.md5(lid + oriralSign)

#print(sign_key("1050_219907"))