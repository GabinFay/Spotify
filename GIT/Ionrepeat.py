import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime
import traceback


from Util.credentials import *
from GIT.onrepeat import OnRepeat

onrepeat = OnRepeat(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

print('top.py')
print(onrepeat.me()['display_name'])
print('started running at : ', datetime.datetime.now().time())

onrepeat.onrepeat()

print('stopped running at : ', datetime.datetime.now().time())
