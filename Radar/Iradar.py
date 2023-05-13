import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime
import traceback


from Util.credentials import *
from Radar.radar import Radar

radar = Radar(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

print(radar.me()['display_name'])
print('started running at : ', datetime.datetime.now().time())

filenames = [i+'.txt' for i in ['us', 'fr', 'soft', 'discov']]

# filenames = ['soft.txt']
h
full_art = []

for i in filenames:
    full_art.extend(radar.complete_txt_ids('txt/'+i))
    
for filename in filenames:
    k = 0
    success = False
    while not success and k < 10:
        try:
            radar.radar(filename, debug_print=False, debug_add_to_pl=False)
            radar.sort_completes_by_pop(filename)
            success = True
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            k += 1


# radar.spot_new_artists(full_art)
# radar.spot_new_artists(full_art, week_num = '28')

print('stopped running at : ', datetime.datetime.now().time())