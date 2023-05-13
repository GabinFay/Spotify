# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

######### SPOTIFY AUTH ################

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import numpy as np
import requests
from copy import deepcopy

market = [ "AD", "AR", "AT", "AU", "BE", "BG", "BO", "BR", "CA", "CH", "CL", "CO", "CR", "CY",
      "CZ", "DE", "DK", "DO", "EC", "EE", "ES", "FI", "FR", "GB", "GR", "GT", "HK", "HN", "HU",
      "ID", "IE", "IS", "IT", "JP", "LI", "LT", "LU", "LV", "MC", "MT", "MX", "MY", "NI", "NL",
      "NO", "NZ", "PA", "PE", "PH", "PL", "PT", "PY", "SE", "SG", "SK", "SV", "TH", "TR", "TW",
      "US", "UY", "VN" ]
market1 = "FR"

client_id = "f52e951743c54dc4a106eafdde0ed938"
client_secret = "e5054eade9f0484b94269fd686bdaf7d"
USER_ID = "%23geesus"
redirect_uri = 'http://google.com/'

credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret)
# token = credentials.get_access_token()
# scope = 'user-follow-modify playlist-modify-private user-library-read'
scope = "playlist-modify-private playlist-modify-public user-read-private user-library-read"

# scope = "playlist-modify-private playlist-modify-public user-read-private \
#       ugc-image-upload user-read-recently-played user-top-read user-read-playback-position \
#             user-read-playback-state user-modify-playback-state user-read-currently-playing \
#       app-remote-control streaming playlist-read-private playlist-read-collaborative \
#       user-follow-modify user-follow-read user-library-modify \
#       user-library-read user-read-email"

token = util.prompt_for_user_token(USER_ID, scope = scope,
                                   client_id = client_id, client_secret = client_secret,
                                   redirect_uri = redirect_uri)
spotify = spotipy.Spotify(auth=token)


PLAYLISTS = []
for j in range(10):
    playlists = spotify.user_playlists(USER_ID, limit = 50,
                                           offset = j * 50)
for i in playlists["items"]:
    PLAYLISTS.append(i["name"])

######### FINDING FIRST AND LAST AND ADDING THEM TO FIXED PLAYLIST #######

for j in range(1):
    albums = spotify.current_user_saved_albums(limit=50, offset=j*50)
    for i in range(len(albums["items"])):
        first = albums["items"][i]["album"]["tracks"]["items"][0]["id"]
        last = albums["items"][i]["album"]["tracks"]["items"][-1]["id"]

        ### Determine playlist name based on albums["items"][i]["added_at"] info
        date = albums["items"][i]["added_at"][0:7]
        playlist_name = "F&L_" + date
        print(playlist_name)

        bool_try = True

        if playlist_name not in PLAYLISTS:
            spotify.user_playlist_create(USER_ID, playlist_name)
            PLAYLISTS.append(playlist_name)

        for j in range(5):
            if bool_try == True:
                playlists = spotify.user_playlists(USER_ID, limit = 50,
                                                   offset = j * 50)
                for i in playlists["items"]:
                    if i["name"] == playlist_name:
                        playlist_id = i["id"]
                        bool_try == False
                        
        already_in_ids = []
        bool_try = False
        for j in range(3):
            if bool_try == False:
                current_tracks = spotify.user_playlist_tracks(USER_ID,
                                        playlist_id = playlist_id,
                                        limit = 100, offset = j * 100,
                                        market = "from_token")

                if len(current_tracks["items"]) != 0:
                    for i in current_tracks["items"]:
                        already_in_ids.append(i["track"]["id"])
                else:
                    bool_try = True

        if first not in already_in_ids:
            spotify.user_playlist_add_tracks(USER_ID,
                                     playlist_id = playlist_id,
                                     tracks = [first])
        if last not in already_in_ids:
            spotify.user_playlist_add_tracks(USER_ID,
                                     playlist_id = playlist_id,
                                     tracks = [last])