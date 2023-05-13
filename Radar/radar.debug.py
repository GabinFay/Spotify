import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime


from Util.credentials import *
from Radar.radar import Radar

radar = Radar(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

print(radar.me()['display_name'])

filenames = ['fr1', 'fr2', 'us1', 'us2', 'soft', 'discov']
filenames = [i+'.txt' for i in filenames]

for i in filenames:
    radar.complete_txt_ids('txt/'+i)
            
FILENAME = "soft.txt"
radar.radar(FILENAME, debug_print=True, debug_add_to_pl=False)

print('stopped running at : ', datetime.datetime.now().time())
