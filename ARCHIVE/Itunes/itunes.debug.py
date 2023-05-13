# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime

import unidecode
import plistlib
from Util.MySpotify import MySpotify
from copy import deepcopy
from Util.credentials import *

# d = {'key': 'value'}
# print(d)  # {'key': 'value'}

# d['mynewkey'] = 'mynewvalue'

# print(d)  # {'key': 'value', 'mynewkey': 'mynewvalue'}
# 



    
def replace_name_by_its_spotify_name(tr_names):
    notfound = list(enumerate(tr_names))
    while notfound != []:
        tracks = [(i, sp.search(tr_name, type='track', limit=1)['tracks']) for i,tr_name in notfound]
        found = [(i,j['items'][0]['name']) for i,j in tracks if len(j['items']) != 0]
        # found_ids = [(i,j['items'][0]['id']) for i,j in enumerate(tracks) if len(j['items']) != 0]
        # found_artists = [(i,j['items'][0]['artists']['name']) if len(j['items'][0]['artists']['name']) = 0 else (i, j['items'][0]['artists']['name'][0]) for i,j in enumerate(tracks) if len(j['items']) != 0]
        # add key 'spotify ID' to the plist file !
        # and add key 'artist' too, and replace the artist by the artist found even if artist already exists
        # notfound = [(i,input(tr_names[i])) for i,j in enumerate(tracks) if len(j['items']) == 0]
        notfound = []
        for i,j in found : tr_names[i] = j
    return tr_names

sp = MySpotify(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)  


        
        # a = list(plist['Tracks'].values())
        # a.reverse()
        
        # tracks = [i for i in a if 'Podcast' not in i]
        
        # modified = deepcopy(tracks)
        # for i,j in enumerate(tracks):
        #     modified[i]['Name'] = j['Artist'] + ' ' + j['Name'] if 'Artist' in j else j['Name']
        #     modified[i]['Name'] = self.normalize_name_for_search(modified[i]['Name'])
    
        # counts = [i['Play Count'] if 'Play Count' in i else i['Track Count'] for i in modified]
        # tr_names = [i['Name'] for i in modified]
        # tr_names = self.replace_name_by_its_spotify_name(tr_names)
        # k = 0
        # for i,j in plist['Tracks'].items():
        #     if 'Podcast' not in j:
        #         plist_copy['Tracks'][i]['Name'] = tr_names[k]
        #         k += 1

        # pop_names = [x for _,x in sorted(zip(counts,tr_names))]
        # pop_names.reverse()
        # print('exit')
    

    


###### GET track INFOS, AND DATE FROM SOME URL  #####

# Tracks = np.genfromtxt("itunes.txt", delimiter = "none", dtype = str)
# s = np.shape(Tracks)[0] ## number of songs

# Final_Tracks = np.concatenate((np.reshape(Tracks,(s,1)), np.reshape(Tracks,(s,1))), axis = 1)

# # Artists = np.zeros((np.shape(Tracks)[0],1), dtype=str) 
# # Songs = np.zeros((np.shape(Tracks)[0],1), dtype=str) 

# Songs = deepcopy(Tracks)


# for i,j in enumerate(Tracks):
#     track = j.split()
#     song_cop = deepcopy(track)
#     for k,l in enumerate(track):
#         if l in ['feat', 'featuring', '-Feat', 'Feat.' 'ft.', 'feat.', \
#                   '&', '(', 'X', ')', 'explicit', '(Explicit)', 'EXPLICIT', 'Ft', 'Video', 'Official']:
#             song_cop.remove(l)
#         if l == '-':
#             song_cop.remove(l)
#         a = (l == 'ft.')
#         if a == True:
#             song_cop.remove(l)
#     Songs[i] = " ".join(song_cop)

# for i,j in enumerate(Tracks):
#         if i == 5:
#             track = j.split()
#             song_cop = deepcopy(track)
#             for k,l in enumerate(track):
#                 print(i)
#                 print(l)
#                 print("l == ft. : ", l == 'ft.')
#                 a = (l == 'ft.')
#                 print("a : ", a)
#                 if a == True:
#                     print(song_cop)
#                     song_cop.remove(l)
#                     print(song_cop)
#             print("EXIT : ", song_cop)
#             Songs[i] = " ".join(song_cop)
    

# playlist_id = "6JnIQy89nseOIvnvPHxd2D"
# already_in_ids = []

# Songs = np.genfromtxt("notfound.txt", delimiter = "none", dtype = str)


# NOTFOUND = []

# for i,track in enumerate(Songs):
#     print(track)
#     res1 = spotify.search(track, type="track", market="from_token", limit=1)
#     if len(res1["tracks"]["items"]) != 0:
#         track_id = res1["tracks"]["items"][0]["id"]
#         if track_id not in already_in_ids:
#             already_in_ids.append(track_id)
#             spotify.user_playlist_add_tracks(USER_ID,
#                                         playlist_id = playlist_id,
#                                         tracks = [track_id])
#             Final_Tracks[i,1] = res1["tracks"]["items"][0]["artists"][0]["name"] + " " + res1["tracks"]["items"][0]["name"]
        
                
#     else:
#         print(" NOT FOUND : " + track)
#         NOTFOUND.append(track)
#         Final_Tracks[i,1] = "#########"


# print(NOTFOUND)

# with open('notfound.txt', 'w') as f:
#     for item in NOTFOUND:
#         f.write("%s\n" % item)