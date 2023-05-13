import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime


from Util.credentials import *
from Radar.complete import Complete

complete = Complete(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

print(complete.me()['display_name'])
print('started running at : ', datetime.datetime.now().time())

filename = 'complete.txt'
complete.complete_txt_ids('txt/'+filename)
complete.complete(filename)

print('stopped running at : ', datetime.datetime.now().time())
