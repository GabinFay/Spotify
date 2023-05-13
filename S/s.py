#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:23:55 2021

@author: gabinfay
"""

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

import datetime



class S(MySpotify):
    
    def week_ritual(self,week_number=False, year=False, jan_to_dec = False):
        self.ssss(year=year)
        self.ssss_star(year=year)
        self.liked_songs_to_week(clean=True)
        self.global_star(week_number=week_number, year=year, jan_to_dec = jan_to_dec)
        self.global_week(week_number=week_number, year=year, jan_to_dec = jan_to_dec)
        
    def s_util(self, pl_ids, jan_to_dec = False):
        tr_ids=[]
        for i, pl_id in enumerate(pl_ids):
            if pl_id != False:
                temp_ids = self.pl_tr_ids(pl_id)
                tr_ids.extend(temp_ids)
        if not jan_to_dec:
            tr_ids.reverse()
        return tr_ids
    
    def ssss(self, year = False):
        week_number, month = self.get_week_number()
        if not year:
            pl_names = ['S'+str(i) for i in range(int(week_number) - 4, int(week_number))]
            ssss_pl_name = 'SSSS'
        else:
            pl_names = [f'S{i}.{year}' for i in range(int(week_number) - 4, int(week_number))]
            ssss_pl_name = f'SSSS.{year}'
        pl_ids = self.find_pl_id(pl_names)
        ssss_pl_id = self.find_pl_id(ssss_pl_name, create_missing=True)
        pl_ids.reverse()
        tr_ids = self.s_util(pl_ids)
        self.clean_playlist(ssss_pl_id)
        self.pl_add_tr(ssss_pl_id, tr_ids)

    def ssss_star(self, year=False):
        week_number, month = self.get_week_number()
        star= '\u2b50'
        if not year:
            pl_names = [star+' S'+str(i) +' ' + star for i in range(int(week_number) - 3, int(week_number)+1)]
            ssss_star_pl_name = star+ ' SSSS ' + star
        else:
            pl_names = [f'{star} S{i}.{year} {star}' for i in range(int(week_number) - 3, int(week_number)+1)]
            ssss_star_pl_name = f'{star} SSSS.{year} {star} '           
        pl_ids = self.find_pl_id(pl_names)
        ssss_star_pl_id = self.find_pl_id(ssss_star_pl_name, create_missing=True)
        pl_ids.reverse()
        tr_ids = self.s_util(pl_ids)
        self.clean_playlist(ssss_star_pl_id)
        self.pl_add_tr(ssss_star_pl_id, tr_ids)
    
    def global_star(self, week_number=False, year=False, jan_to_dec = False):
        if not week_number:
            week_number, _ = self.get_week_number()
        star= '\u2b50'
        if not year:
            pl_names = [f'{star} S{i} {star}' for i in range(1, int(week_number))]
            star_id = self.find_pl_id(f'{star} S {star}', create_missing=True)
        else:
            pl_names = [f'{star} S{i}.{year} {star}' for i in range(1, int(week_number))]
            star_id = self.find_pl_id(f'{star} S.{year} {star}', create_missing=True)
        pl_ids = self.find_pl_id(pl_names)
        tr_ids = self.s_util(pl_ids, jan_to_dec=jan_to_dec)
        self.clean_playlist(star_id)
        self.pl_add_tr(star_id, tr_ids)

    def global_week(self, year=False, week_number=False, jan_to_dec = False):
        if not week_number:
            week_number, _ = self.get_week_number()
        if not year:
            pl_names = [f'S{i}' for i in range(1, int(week_number))]
            s_id = self.find_pl_id('S', create_missing=True)
        else:
            pl_names = [f'S{i}.{year}' for i in range(1, int(week_number))]
            s_id = self.find_pl_id(f'S.{year}', create_missing=True)
        pl_ids = self.find_pl_id(pl_names)
        tr_ids = self.s_util(pl_ids, jan_to_dec = jan_to_dec)
        self.clean_playlist(s_id)
        self.pl_add_tr(s_id, tr_ids)

    def liked_songs_to_week(self, clean = False):
        liked_tr_ids, _ = self.get_liked_songs()
        liked_tr_ids.reverse()
        week_number, _ = self.get_week_number()
        s_pl_id = self.find_pl_id(f'S{week_number}.{self.get_year()}', create_missing=True)
        self.pl_add_tr(s_pl_id, liked_tr_ids)
        if clean:
            self.clean_liked_songs(liked_tr_ids)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



