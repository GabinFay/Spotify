import spotipy
import os
import unidecode
import requests
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image, ImageDraw, ImageFont
import base64
import random

class Offline():
    def __init__(self):
        self.fish_emoji = '\ud83d\udc1f'.encode('utf-16', 'surrogatepass').decode('utf-16')

    def clean_playlist(self, playlist_id):
        self.playlist_replace_items(playlist_id, [])
        
    def complete_txt_ids(self, filename):
        with open(filename, 'r') as us:
            lines = us.readlines()
        
        full = []

        if all(len(line.split(' - ')) == 2 for line in lines):
            for line in lines:
                ar_name, ar_id = [x.rstrip() for x in line.split(' - ', 1)]
                full.append([ar_name, ar_id])
        
        else:
            for line in lines:
                if len(line.split(' - ')) == 2:
                    ar_name, ar_id = [x.rstrip() for x in line.split(' - ', 1)]
                    full.append([ar_name, ar_id])
                else:
                    test0 = False; j = 0
                    while test0 == False:
                        print("moi : ", line)
                        artist = self.search(line, type="artist")["artists"]["items"][j]
                        answer = input(artist["name"] + "\nEst ce le bon artiste ? (y)/(n) \n")
                        if answer == "y":
                            test0 = True
                        elif answer == "n":
                            j +=1
                    full.append([artist["name"], artist["id"]])
            self.write_2d_array_to_txt(full, filename)
        return self.artists([y for _,y in full])['artists']
    
    def get_nested_list_dim(self, seq):
        if not type(seq) == list:
            return []
        return [len(seq)] +self.get_nested_list_dim(seq[0])
    
    def write_2d_array_to_txt(self, array, filename):
        with open(filename, 'w+') as f:
            for x, y in array:
                f.write('{} - {}\n'.format(x, y))
    
    def write_1d_array_to_txt(self, array, filename):
        with open(filename, 'w+') as f:
            for x in array:
                f.write('{}\n'.format(x))

    flatten = lambda self, seq: [k for l in seq for k in l]

    has_dupli = lambda self, seq: len(seq) > len(set(seq))

    normalize_string = lambda self, foo: unidecode.unidecode(foo.lower())

    def clean_dupli(self, L):
        return list(dict.fromkeys(L))

    def get_surrogates(self, long_code):
        h = int(np.floor((long_code - 0x10000) / 0x400) + 0xD800)
        l = int((long_code - 0x10000) % 0x400 + 0xDC00)
        return ''.join(map(chr, [h,l]))
    
    def emoji_from_surrogates(self, surrogate_codes):
        return surrogate_codes.encode('utf-16',  'surrogatepass').decode('utf-16')