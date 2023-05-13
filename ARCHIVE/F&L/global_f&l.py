# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

######### SPOTIFY AUTH ################

import time
import spotipy
from collections import defaultdict

start_time = time.time()


def has_dupli(L):
    return len(L) > len(set(L))

def see_dupli(L):
    D = defaultdict(int)
    for k in L:
        D[k] += 1
    return [(i,k) for i, (k, v) in enumerate(D.items()) if v > 1]

    
def tracks_ids(playlist_id, market):
 ids = []
 total = spotify.playlist_items(playlist_id, limit=1)["total"]
 l = 0
 while l * 100 < total:
     for k in spotify.playlist_items(playlist_id, limit=100, offset=l*100, market=market)["items"]:
         ids.append(k["track"]["id"])
     l += 1
 return ids


def add_tracks(USER_ID, playlist_id, ids):
    ids = [ids[i:i + 100] for i in range(0, len(ids), 100)]
    if len(ids) != 0:
        for j in ids:
            spotify.user_playlist_add_tracks(USER_ID, playlist_id = playlist_id, tracks = j) 

market = [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY",
      "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU",
      "ID", "IE", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL",
      "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "SE", "SG", "SK", "SV", "TH", "TR", "TW",
      "US", "UY", "VN" ]

client_id = "12c0e5e7cfad4e9093642889c201ed0f"
client_secret = "ecaafcac08634f7390f3f9c1fb1934fa"
USER_ID = "%23geesus"
redirect_uri = 'http://google.com/'


scope = "playlist-modify-private playlist-modify-public user-read-private \
      ugc-image-upload user-read-recently-played user-top-read user-read-playback-position \
            user-read-playback-state user-modify-playback-state user-read-currently-playing \
      app-remote-control streaming playlist-read-private playlist-read-collaborative \
      user-follow-modify user-follow-read user-library-modify \
      user-library-read user-read-email"
      
token = spotipy.util.prompt_for_user_token(USER_ID, scope = scope,
                                   client_id = client_id, client_secret = client_secret,
                                   redirect_uri = redirect_uri)
spotify = spotipy.Spotify(auth=token)


######### FINDING FIRST AND LAST AND ADDING THEM TO FIXED PLAYLIST #######

playlist_id = "121NIlLx6CfftsvJMAJnsY"

j = 0 ; to_add = []
total = spotify.user_playlists(USER_ID, limit = 1)["total"]
while j*50 < total:
    albums = spotify.current_user_saved_albums(limit=50, offset=j*50)
    for i in albums["items"]:
        to_add.insert(0, i["album"]["tracks"]["items"][0]["id"])
        to_add.insert(1, i["album"]["tracks"]["items"][-1]["id"])
    j+=1
    
fl_tracks = set(tracks_ids(playlist_id, market))    
non_duplicates = list(set(to_add).difference(fl_tracks))

add_tracks(USER_ID, playlist_id, non_duplicates)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    