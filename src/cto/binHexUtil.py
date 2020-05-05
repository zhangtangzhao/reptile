'''
Created on 2020年4月28日

@author: zhangtangzhao
'''
# -*- coding: utf-8 -*-
import binascii
import hashlib



def base( n ):
    return str(binascii.b2a_hex( n.encode( 'utf-8' ) ), encoding='utf-8')


def md5(content):
    return hashlib.md5(content.encode(encoding='utf-8')).hexdigest()

#print( base( "807bf8ab6e8fe143" ) )