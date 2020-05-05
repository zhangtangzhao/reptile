'''
Created on 2020年4月24日

@author: zhangtangzhao
'''
# -*- coding: utf-8 -*-
import js2py

def decode(code,less_id):
    content = open( "decode.js", 'r', encoding='utf-8' ).read()
    js = js2py.eval_js( content )
    res = js( code, less_id )
#     print( res )
    return res

# print(decode("BiQQtlHbnjjRQlND7PxDpQQl9Lxj6QRl7byJASNxQ7xPe5QdPXy5JQQpk5W3OLVd7HyHkS0PkOxHAMCHi5VMvOiO0OxDOoh7mQwUDPCB0SPPeMxjgPWUNO0HUaYHEPhqIHYdHN0dVLxPQXwpdPNOJNjdkIyHQozqPPOUDP0UkIPDeXw1IbyHJOWaAa0PQPjdO5CPDPOPuMx7fQh7PHWlKNhqmPy7ebxxmPYJHSPO07xDVoijPPWUoPjHQPyxPbxD75YJDSvxr7xPeXZlRPNivPjHrQQxVohUNHi02PzlQL07eMw1iLyHJQQWJ7VHANiU75CcJSOPza0HpMZldPWlQNhB0IjP6oh7mXy50", "1449_279516"))