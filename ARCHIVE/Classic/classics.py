#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 15:19:13 2021

@author: gabinfay
"""

import time
import spotipy
import os

start_time = time.time()

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


################### Delete test playlists while testing ###############

location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/"

full_path = location + "test.txt"

if os.path.exists(full_path):
    with open(full_path,'r') as ids:
        previous_ids = ids.readlines()
    for i in previous_ids:
        i = i.rstrip()
        spotify.current_user_unfollow_playlist(i)

###################################

playlist_total = spotify.user_playlists(USER_ID, limit = 1)["total"]

PLAYLISTS = []

j = 0
while 50 * j < playlist_total:
    playlists = spotify.user_playlists(USER_ID, limit = 50,
                                           offset = j * 50)
    for i in playlists["items"]:
        PLAYLISTS.append(i["name"])
    j += 1
    

#######

with open("classics.txt",'r') as file:
    albums = file.readlines()
    
for al in albums:

        
    start_time = time.time()    
    print(al)
    
    album = spotify.search(al, type="album")["albums"]["items"][0]
    name = album["name"]
    total = spotify.album(album["id"])
    tracks = spotify.album_tracks(album["id"])
    tracks = [i["id"] for i in tracks["items"]]
    ############### Perform the following only if it doesn't already exists
    
    if name not in PLAYLISTS:
        
        play_id = spotify.user_playlist_create(USER_ID, name)["id"]
        spotify.user_playlist_add_tracks(USER_ID, playlist_id = play_id,
                                                     tracks = tracks)
        with open(full_path, 'w+') as f:
            f.write("%s\n" % play_id)            
        
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
    
    
    
    
    
    
    
    
    
