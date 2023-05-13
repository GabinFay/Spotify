# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:00:29 2020

@author: gabin
"""

######### SPOTIFY AUTH ################

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from OFIVE.ofive import Ofive

import requests
import re
import datetime


class AOTW(Ofive):

    def aotw(self):
        to_include = 'records'
        not_to_include = ['movies', 'interview']
        Href = self.get_href(100, to_include, not_to_include)
        tr_dates = [i.split('/')[3:-2] for i in Href]
        # tr_names = [' '.join(re.split('/|-', i)[6:-1]) for i in Href]
        website = [i[6:-1] for i in Href]
        req = [requests.get(url) for url in website]
        Alb_ids = []
        for r in req:
            Alb_ids.append([word[42:64] for line in r.text.splitlines() for word in line.split() if word[:29]=='src="https://open.spotify.com'])
        week_numbers = [datetime.date(int(date[0]), int(date[1]), int(date[2])).isocalendar()[1] for date in tr_dates]
        pl_names = [self.fish_emoji + ' S' + str(week_number) for week_number in week_numbers]
        for alb_ids,pl_name in zip(Alb_ids, pl_names):
            alb = self.albums(alb_ids)['albums']
            img = self.grid(alb)
            pl_id = self.pl_ofive_week_normale(pl_name + ' ' + self.fish_emoji, alb_ids)
            self.upload_cover(pl_id, img)
            pl_id = self.pl_ofive_week_feats(pl_name + ' feat ' + self.fish_emoji, alb_ids)
            self.upload_cover(pl_id, img)
            pl_id = self.pl_ofive_week_pop(pl_name + ' pop ' + self.fish_emoji, alb_ids)
            # pl_id = self.pl_ofive_week_pop(pl_name + '\u2b50' + self.fish_emoji, alb_ids)
            self.upload_cover(pl_id, img)

    def pl_ofive_week_normale(self, pl_name, alb_ids):    
        pl_id = self.find_pl_id(pl_name, create_missing=True)
        alr_in_names = self.pl_tr_names(pl_id)
        if alr_in_names == []:
            tr_ids = [j['id'] for i in alb_ids for j in self.album_tracks(i, limit=50, offset=0, market=None)["items"]]
            self.pl_add_tr(pl_id, tr_ids)
        return pl_id

    def pl_ofive_week_feats(self, pl_name, alb_ids):
        pl_id = self.find_pl_id(pl_name, create_missing=True)
        alr_in_names = self.pl_tr_names(pl_id)
        if alr_in_names == []:
            tr_ids = [j['id'] for i in alb_ids for j in self.album_tracks(i, limit=50, offset=0, market=None)["items"] if len(j['artists']) != 1]
            self.pl_add_tr(pl_id, tr_ids)
        return pl_id
    
    def pl_ofive_week_pop(self, pl_name, alb_ids):
        pl_id = self.find_pl_id(pl_name, create_missing=True)
        self.clean_playlist(pl_id)
        for i in alb_ids:
            tr_ids = [j['id'] for j in self.album_tracks(i, limit=50, offset=0, market=None)["items"]]
            tr_names = [j['name'] for j in self.album_tracks(i, limit=50, offset=0, market=None)["items"]]
            tr = self.tracks(tr_ids)
            popularity = [j['popularity'] for j in tr['tracks']]
            pop_ids = [x for _,x in sorted(zip(popularity,tr_ids))]
            pop_names = [x for _,x in sorted(zip(popularity, tr_names))]
            pop_ids.reverse()
            self.pl_add_tr(pl_id, pop_ids[:3])
        return pl_id