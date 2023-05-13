#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:23:55 2021

@author: gabinfay
"""

import time
import spotipy
import os
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

###################################

almi = ["0P5Gt3wVYAgzpjLhrwjtid", "5oidbMFLIBCFAm8VjCjLKE"]
dope = ["7lyfIivj8xoPhkV0uPI6Bo", "0LNesHR1Mmtpqaa47Aoibs", "15q8pIzcK1twrjwwh5InPF", "2LPj0dyy3Rp9iFRlWqf7hr"]
quint = ["3KbNlRMarrUI4LXOvY27Vx", "2FBwpQXLExhb338K3FGLZh", "4wwl4xb25HE0aZVuSa9UfB"]

full_almi = "2dmPbdbTEEN1qGH3mZhk6c"
full_dope = "7pJYASLYkBhotBYh8oXx5H"
full_quint = "44DV6QJEMLCNnT18nAOqBK"


def bulk(list_of_splits_ids, merge_id, market):
    for i in list_of_splits_ids:
        split_tracks = set(tracks_ids(i, market = market))
        merge_tracks = set(tracks_ids(merge_id, market = market))
        spotify.user_playlist_add_tracks(USER_ID, merge_id, 
                                         list(split_tracks.difference(merge_tracks)))
                                

bulk(almi, full_almi, market)
bulk(dope, full_dope, market)        
bulk(quint, full_quint, market)

                
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



