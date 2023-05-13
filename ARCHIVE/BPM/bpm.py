import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify

import datetime
import requests
import re

class Bpm(MySpotify):

    def bpm(self, filename):
        NOTFOUND = []
        with open(f'{filename}.txt', 'r') as fp:
            lines = fp.readlines()
            fp.close()
        songs = [line.strip('\n').split(' - ') for line in lines]

        pl_id = self.find_pl_id(f'{filename}.BPM', create_missing=True)
        for i in songs:
            if len(i)==3:
                tr = self.search(i[1] + ' ' + i[2], type="track", market="FR", limit=1)['tracks']['items']
                if tr != []:
                    self.pl_add_tr(pl_id, tr[0]["id"])
                else:
                    NOTFOUND.append(i[1] + ' - ' + i[2])
        print('########### NOTFOUND ###########')
        for i in NOTFOUND: print(i)

    def precise_bpm(self):
        with open('allbpm.txt', 'r') as fp:
            lines = fp.readlines()
            fp.close()
        songs = [line.strip('\n').split(' - ') for line in lines]
        pl_ids = self.find_pl_id([f'{bpm}.BPM' for bpm in range(166,199)], create_missing = True)
        for i in songs:
            if len(i)==3:
                tr = self.search(i[1] + ' ' + i[2], type="track", market="FR", limit=1)['tracks']['items']
                if tr != []:
                    self.pl_add_tr(pl_ids[int(i[0][:3])-166], tr[0]["id"])     