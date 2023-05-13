# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

import sys
import os
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime


from Util.credentials import *
from Util.MySpotify import MySpotify

spo = MySpotify(client_id=CLIENT_ID, 
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)


def spobak(spo, filename):
    NOTFOUND = []
    with open(f'{filename}.txt', 'r') as fp:
        lines = fp.readlines()
        fp.close()
    songs = [line.strip('\n') for line in lines]
    print('')
    pl_id = spo.find_pl_id(filename, create_all=True)
    for i in songs:
        tr = spo.search(i[0], type="track", market="FR", limit=1)['tracks']['items']
        if tr != []:
                spo.pl_add_tr(pl_id, tr[0]["id"])
        else:
            NOTFOUND.append(i)
    print('########### NOTFOUND ###########')
    for i in NOTFOUND: print(i)

print(spo.me()['display_name'])
print('started running at : ', datetime.datetime.now().time())

filenames = [i[:-4] for i in os.listdir() if i[-4:] == '.txt']

for i in filenames:
    if i != 'template':
        spobak(spo, i)

