# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')


from Util.credentials import *
from S.s import S

s = S(client_id=CLIENT_ID, 
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

year = s.get_year()
s.week_ritual(year = year, jan_to_dec = False)