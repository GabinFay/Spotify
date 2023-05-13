import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify
from Util.credentials import *

spo = MySpotify(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

delimiter_id = '3Iaeuda9ZUNT8GHo7ukZTI'

album_name = "It's almost dry"
album = spo.search(album_name, type="album")["albums"]["items"][0]
album_name = album['name']
pl_id = spo.user_playlist_create(spo.user_id, f'🎊 {album_name} 🎊')['id']
tracks = spo.album_tracks(album["id"])["items"]

# ADD THE WHOLE ALBUM ON TOP #
tr_ids = [i['id'] for i in tracks]
spo.pl_add_tr(pl_id, tr_ids)
spo.pl_add_tr(pl_id, delimiter_id)
# featurings
tr_ids = [tr['id'] for tr in tracks if len(tr['artists']) != 1]
spo.pl_add_tr(pl_id, tr_ids)
spo.pl_add_tr(pl_id, delimiter_id)
# post featurings
feats_indices = [i for i,tr in enumerate(tracks) if len(tr['artists']) != 1]
try:
    tr_ids = [tracks[i+1]['id'] for i in feats_indices]
except:
    tr_ids = [tracks[i+1]['id'] for i in feats_indices[:-1]]    
spo.pl_add_tr(pl_id, tr_ids)
spo.pl_add_tr(pl_id, delimiter_id)
# most 5 pops
all_tr_ids = [i['id'] for i in tracks]
all_tr = spo.tracks(all_tr_ids)['tracks']
sorted_ids = [tr['id'] for tr in sorted(all_tr, key=lambda item: item['popularity'], reverse=True)][:5]
spo.pl_add_tr(pl_id, sorted_ids)
spo.pl_add_tr(pl_id, delimiter_id)
# first 3 songs & last
tr_ids = [i['id'] for i in tracks][:3]
spo.pl_add_tr(pl_id, tr_ids)
tr_ids = [i['id'] for i in tracks][-1]
spo.pl_add_tr(pl_id, tr_ids)

    