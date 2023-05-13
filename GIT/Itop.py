import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime
import traceback


from Util.credentials import *
from GIT.top import Top

top = Top(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

print('top.py')
print(top.me()['display_name'])
print('started running at : ', datetime.datetime.now().time())

top.top()

print('stopped running at : ', datetime.datetime.now().time())
