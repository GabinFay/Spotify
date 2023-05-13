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

filename = 'completeforpeople.txt'
complete.complete_txt_ids(filename)
complete.complete(filename, plus_txt=False, update_descr = True)

print('stopped running at : ', datetime.datetime.now().time())