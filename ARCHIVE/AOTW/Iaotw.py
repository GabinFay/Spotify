# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')


from Util.credentials import *
from AOTW.aotw import AOTW

aotw = AOTW(client_id=CLIENT_ID, 
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

aotw.aotw()