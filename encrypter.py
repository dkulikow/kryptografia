#!/usr/bin/env python3

import requests as rq
import curses.ascii as ca
import string

def get_cryptograms():
    r = rq.get("http://zagorski.im.pwr.wroc.pl/courses/kbk2015/l1.php?id=208802")
    data = r.text
    data_list = data.split("<br />")
    all_cryptograms = []

    for c in data_list: 
        if len(c) > 0 and (c[0] == "0" or c[0] == "1"):
            splitted = c.split(" ")
            letters = [l for l in splitted if len(l) > 0]
            all_cryptograms.append(letters)
            
    to_decrypt = all_cryptograms[-2] 
    cryptograms = all_cryptograms[:-2]
    cryptograms = cryptograms[:6] + cryptograms[7:]
    return to_decrypt, cryptograms

special = [' ', '!', '"', ",", "-", ".", ":", "?", "'", "5"]
letters = string.ascii_lowercase.replace("v", "")
letters += string.ascii_uppercase.replace("Q","")
letters = letters.replace("V", "")
letters = letters.replace("q", "")
class Encrypter():

    def __init__(self, info):
        self.to_decrypt = info[0]
        self.message_length = len(self.to_decrypt)
        self.cryptograms = info[1][:][:self.message_length-1]
        self.nr_of_cryptograms = len(self.cryptograms)
        self.xored_list = []
        self.possible_letters = [[] for i in range(self.message_length-1)]

    def xor_cryptograms(self):
        self.xored_list = []
        for i in range(self.nr_of_cryptograms):
            xored = [chr(int(self.cryptograms[i][j],2) ^ int(self.to_decrypt[j], 2)) for j in range(self.message_length)]
            self.xored_list.append(xored)

    def char_possibility(self, char, position):
        num = 0
        for xored in self.xored_list:
            xor_with_char = ord(xored[position]) ^ ord(char)
            #print(chr(xor_with_char), end="")
            if char == 'm' and position == 3:
                print (chr(xor_with_char))
            if (chr(xor_with_char) not in letters and chr(xor_with_char) not in special):
            #not (ca.isalpha(xor_with_char) or ca.isdigit(xor_with_char) or self.is_special(xor_with_char))
                #print("\nFAILED AT: ", ord(xored[position]), ord(char))

                num += 1
        #print("\n")
        return num <= 0

    def print_chars(self):
        for message in self.xored_list:
            for letter in message:
                print ("%4c" % letter, end="")
            print ("\n")

    def print_numbers(self):
        for message in self.xored_list:
            for letter in message:
                print ("%4d" % ord(letter), end="")
            print ("\n")

    def print_chars_with_xor(self, char):
        for message in self.xored_list:
            for letter in message:
                if ord(letter) < 32:
                    print ("%4c" % chr(ord(letter) ^ ord(char)) , end="")
                else:
                    print ("%4d" % (ord(letter) ^ ord(char)), end="")
            print ("\n")

    def encrypt(self):
        for position in range(self.message_length):
            for letter in letters:
                if(self.char_possibility(letter, position)):
                    self.possible_letters[position].append(letter)
            if(self.char_possibility(" ", position)):
                    self.possible_letters[position].append(" ")
            for letter in string.digits:
                if(self.char_possibility(letter, position)):
                    self.possible_letters[position].append(letter)                



e = Encrypter((get_cryptograms()))  
e.xor_cryptograms()
e.encrypt()
e.print_chars_with_xor('D')
for pos in e.possible_letters:
    print(pos)

