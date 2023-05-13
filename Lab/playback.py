import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify
from Util.credentials import *

spo = MySpotify(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

# ====================================

# import time

# where_liked_songs_go_id = '7oaqVvZEsnibl6s5iK6Bdb'
# inspected_id = '4PmKsbJ5ZRahdQd509a4pR'
# inspected_tr_ids = spo.pl_tr_ids(inspected_id)

## need to provide the playlist URI to start or a list of ones
# spo.start_playback(context_uri=f'spotify:playlist:{inspected_id}')
# time.sleep(5)
# results = []
# k = 0
# while k < len(inspected_tr_ids):
#     track_length = spo.current_playback()['item']['duration_ms']
#     for i in [0.33, 0.66, 0.90]:
#         spo.seek_track(round(i*track_length))
#         time.sleep(5)
#         ## wait 5 seconds (how to ?) (or just 3 ?)
#     spo.pause_playback()
#     b = input('liked == enter without nothing, otw input something before typing enter !')
#     if len(b) == 0:
#         results.append(True)
#     else:
#         results.append(False)
#     spo.next_track()
#     spo.start_playback()
#     time.sleep(5)
#     k += 1

# to_add_ids = [i for i,j in zip(inspected_tr_ids,results) if j]
# spo.pl_add_tr(where_liked_songs_go_id, to_add_ids)

###########################

# OTHER POSSIBILITY ! Instead of having separate playlist, just pause the song for 5 seconds for you to like it
# looks ideal really

## very sped up here !

import time

inspected_id = '4PmKsbJ5ZRahdQd509a4pR'
spo.start_playback(context_uri=f'spotify:playlist:{inspected_id}')
time.sleep(5)
while True:
    track_length = spo.current_playback()['item']['duration_ms']
    for i in [0.33, 0.66, 0.90]:
        spo.seek_track(round(i*track_length))
        time.sleep(5)
    spo.next_track()
    time.sleep(5)