import hashlib
import base64
from Crypto.Cipher import AES
from lxml import objectify
import json


access = "***REMOVED***".encode()
password = "***REMOVED***".encode()
secret = b'X\xf1\x8dp\xf6g\xc9\xc7\x9e\xf7\xdeC[\xf0\xf9\xb1U;\xbbna\x81b\x12\xab\x80\xe5\xb0\xd3Q\xfb\xb1'


def get_md5(data):
    m = hashlib.md5()
    m.update(data)

    return m.digest()


def decode(data):
    decoded = base64.b64decode(data)

    #print(1)
    abyte1 = get_md5(access + secret)
    abyte2 = get_md5(secret + password)

    #print(2)
    key = abyte1 + abyte2

    #print(3)
    a = AES.new(key)
    a = AES.new(key, AES.MODE_ECB)
    res = a.decrypt(decoded)

    #print(4)
    #print(type(res))
    #print(res)
    return res
