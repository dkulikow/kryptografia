
import requests as rq
import re
import string as st
import time

from Crypto.Cipher import ARC4
from itertools import product

def get_info_from_website():
    request = rq.get("http://zagorski.im.pwr.wroc.pl/courses/kbk2015/l1.php?id=208800")
    data = request.text
    key_regex = re.compile("\(zad 2\).*<b>(.*)</b>[^01]*([01 ]*)")
    info = key_regex.findall(data)
    return info[0][0], info[0][1]

def parse_bistring(bitstring):
    bitstrings_list = bitstring.split(" ")
    bitstrings_list = filter(None, bitstrings_list)
    bitstrings_list = [int(string, 2) for string in bitstrings_list]
    return bitstrings_list

def decode_and_confirm(cryptogram, key):
    decryptor = ARC4.new(key)
    message = decryptor.decrypt(cryptogram)
    try:
        message.encode()
        print message
        return message
    except:
        return ""

symbols = "2a713456890bcdef"
#symbols = "de4213567890abcf"
key2, cryptogram = get_info_from_website()
cryptogram = parse_bistring(cryptogram)
bytestring = str(bytearray(cryptogram))

i = 0
for key1 in product(symbols, repeat=8):
    key = "".join(key1) + key2
    decode_and_confirm(bytestring, key.encode())
    i += 1
    if i % 1000000 == 1:
	   print(key)
	    
