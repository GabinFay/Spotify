# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime


from Util.credentials import *
from BPM.bpm import Bpm

bpm = Bpm(client_id=CLIENT_ID, 
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

print(bpm.me()['display_name'])
print('started running at : ', datetime.datetime.now().time())

# for i in ['175.185','160', '170','180','190']:
#     bpm.bpm(i)

bpm.precise_bpm()