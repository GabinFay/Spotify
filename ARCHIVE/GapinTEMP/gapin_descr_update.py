import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify
from Util.credentials import *

spo = MySpotify(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

description = "Updated Completes available here : https://open.spotify.com/user/312eq5p7cvh6m2ub4x33uglbsf7i"

for pl_id in spo.pl_ids:
    spo.playlist_change_details(pl_id, description=description)