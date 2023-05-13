# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

######### SPOTIFY AUTH ################

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify
from pyyoutube import Api
import requests
import re
import datetime
import json
# Get authorization url
# >>> api.get_authorization_url()
# ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=scope&state=PyYouTube&access_type=offline&prompt=select_account', 'PyYouTube')
# # user to do
# # copy the response url
# >>> api.generate_access_token(authorization_response="link for response")
# AccessToken(access_token='token', expires_in=3599, token_type='Bearer')

import datetime
date = datetime.date.today().strftime("%d/%m/%Y")



class Youfive(MySpotify):
    def __init__(self):
        self.api_key = 'AIzaSyD33HoW7ej2GSvWs8MRuTxPjpMufSuJmlo'
        self.api = Api(access_token=self.api_key)

    def youfive(self):
        month = datetime.datetime.now().strftime("%B").lower()
        year = datetime.date.today().strftime("%d/%m/%Y")[-4:]
        playlists_by_mine = self.api.get_playlists(mine=True)
        pl_name = self.get_ofive_pl_name(month)
        tr_names = self.pl_tr_names(pl_name)
        pl_id = 'PLIlNYYp2ojeK05Q54YidAzLxp18_8T6fi'
        for tr_name in tr_names:
            r = self.api.search_by_keywords(q=tr_name, search_type=['video'], count =1, limit=1).items[0]
            vid_id = json.loads(r.to_json())['id']['videoId']
            self.add_video_to_playlist(vid_id, pl_id)
            
    
    def get_ofive_pl_name(self, month, year):
        return self.fish_emoji + ' ' + month + ' ' + year[2:] + ' ' + self.fish_emoji
    
    def add_video_to_playlist(self,videoID,playlistID):
        add_video_request=self.api.playlistItem().insert(
          part="snippet",
          body={
                'snippet': {
                  'playlistId': playlistID, 
                  'resourceId': {
                          'kind': 'youtube#video',
                      'videoId': videoID
                    }
                #'position': 0
                }
        }
         ).execute()

youfive = Youfive()
youfive.youfive()