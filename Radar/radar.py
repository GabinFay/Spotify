import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')

import time
import datetime
import requests
from complete import Complete
from io import BytesIO
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image, ImageDraw, ImageFont
import base64
import random
import spotipy
from collections import Counter
from pathlib import Path


class Radar(Complete):
    
    def radar(self, filename, debug_print = False, debug_add_to_pl = False):
        week_number, month = self.get_week_number()
        artists = self.complete_txt_ids('txt/'+filename)
        print('')
        pl_names = [artist['name'] + " Complete " + self.return_emoji_unicode(filename[:-4]) for artist in artists]
        # self.change_complete_names(pl_names)
        pl_ids = self.find_pl_id(pl_names, create_missing=True)
        blood_drop = self.emoji_from_long_code(0x1FA78)
        radar_id = self.find_pl_id(blood_drop + ' ' + month + ' ' + blood_drop, create_missing=True)
        radar_S_id = self.find_pl_id(blood_drop + ' S' + week_number + ' ' + blood_drop, create_missing=True)
        self.cover_grid(artists, radar_S_id, average = False, pixelize=True)
        # self.change_radar_description(radar_id, artists)
        # print(radar_name)
        for artist, pl_id in zip(artists, pl_ids):
            new_ids, new_names, alr_in_names = self.one_complete(artist, pl_id)
            new_ids.reverse() ; new_names.reverse()
            if not debug_add_to_pl:
                if alr_in_names != [] and new_ids != []:
                    new_ids = self.add_albums_to_lib_but_not_radar(new_ids)
                    alr_in_radar_names = self.pl_tr_names(radar_id)
                    to_add_id = [i for i,j in zip(new_ids, new_names) if j not in alr_in_radar_names]
                    self.pl_add_tr(radar_id, to_add_id)
                    self.pl_add_tr(radar_S_id, to_add_id)
        return pl_ids
    
    def sort_completes_by_pop(self, filename):
        week_number, month = self.get_week_number()
        artists = self.complete_txt_ids('txt/'+filename)
        pl_names = [artist['name'] + " Complete " + self.return_emoji_unicode(filename[:-4]) for artist in artists]
        pl_ids = self.find_pl_id(pl_names, create_missing=True)
        for pl_id in pl_ids:
            if pl_id != None:
                self.order_by_popularity(pl_id)
    
    def add_albums_to_lib_but_not_radar(self, new_ids):
        trs=self.tracks(new_ids)
        albums_download_id = self.find_pl_id('albums downloads', create_missing=True)
        new_albums_ids = [i['album']['id'] for i in trs['tracks'] if i != None]
        occurences = Counter(new_albums_ids)
        long_album_ids = [k for k,c in occurences.items() if c >= 3]
        if long_album_ids != []:
            albums = self.albums(long_album_ids)['albums']
            tracks_ids = [j['id'] for i in albums for j in i['tracks']['items']]
            alr_in_album_pl = self.pl_tr_ids(albums_download_id)
            to_add_ids = [i for i in tracks_ids if i not in alr_in_album_pl]
            self.pl_add_tr(albums_download_id, to_add_ids)
            try:
                self.current_user_saved_albums_add(long_album_ids)
            except:
                for i in long_album_ids:
                    self.current_user_saved_albums_add(i)
        return [i['id'] for i in trs['tracks'] if i!=None and i['album']['id'] not in long_album_ids]

    def spot_new_artists(self, lead_artists, week_num = False):
        lead_artists = list(filter(None, lead_artists))
        week_number, month = self.get_week_number()
        if week_num != False:
            week_number = week_num
        lead_ids = [i['id'] for i in lead_artists]
        # discov_name = 'txt/discov/featured S'+ week_number+'.txt'
        try:
            alr_in_featured_artists = self.read_txt_to_array('featured_artists.txt')
        except FileNotFoundError:
            # Path(discov_name).touch()
            alr_in_featured_artists = []
        blood_drop = self.emoji_from_long_code(0x1FA78)
        radar_id = self.find_pl_id(blood_drop + ' S' + week_number + ' ' + blood_drop, create_missing=True)
        # hetz_id = self.find_pl_id('radar S25')
        pl_tr = self.pl_tr(radar_id)
        # pl_tr = self.pl_tr(hetz_id)
        artists = []
        for i in pl_tr:
            if i['track'] != None:
                for j in i['track']['artists']:
                    if j['id'] not in lead_ids and j['id'] not in artists and j['id'] not in alr_in_featured_artists:
                        artists.append(j['id'])
        # artists = [j for i in pl_tr for j in i['track']['artists'] if j not in tracked_artists]
        # artists = self.clean_dupli(artists)
        to_add_artists = [i for i in artists if i not in alr_in_featured_artists]
        alr_in_featured_artists.extend([i for i in to_add_artists])
        self.write_1d_array_to_txt(to_add_artists,'featured_artists.txt', mode = 'a')
        globe_emoji = self.emoji_from_surrogates('\ud83c\udf0d')
        print('')
        self.discov('', discov_name = globe_emoji + ' S' + week_number + ' ' + globe_emoji, ids = to_add_artists, tr_num = 5)

    def change_radar_description(self, radar_id, artists):
        ar_names = [artist['name'] for artist in artists]
        random.shuffle(ar_names)
        description = ''
        i = 0
        while len(description) < 107 and i < len(ar_names):
            nam = ar_names[i]
            if len(nam) < 8:
                description += nam +', '
            i += 1
        description += '...'
        self.playlist_change_details(radar_id, description=description) 

    def change_complete_names(self, complete_names):
        for i in complete_names:
            test = False
            foo = i.split(' Complete')[0] + ' Complete'
            k = 0
            while k < len(self.pl_names) and test==False:
                if self.pl_names[k].split(foo)[0] != self.pl_names[k]:
                    pl_id = self.pl_ids[k]
                    pl_name = self.pl_names[k]
                    if pl_id != [] and pl_name != i:
                        self.playlist_change_details(pl_id, name=i)
                        self.pl_names[k] = i
                    test = True
                k += 1
                

    def get_radar_name_and_id(self, filename):
        date = datetime.datetime.now()
        week_number, month = self.get_week_number()
        radar_name = "radar " + '\u00b7 ' + self.return_emoji_unicode(filename[:-4]) + ' \u00b7 ' + month
        radar_S_name = "radar " + '\u00b7 ' + self.return_emoji_unicode(filename[:-4]) + ' \u00b7 ' + 'S' + week_number
        radar_id = self.find_pl_id(radar_name, create_missing = True)
        radar_S_id = self.find_pl_id(radar_S_name, create_missing = True)
        return (radar_id, radar_name, radar_S_id, radar_S_name)

    def return_emoji_unicode(self, filename):
            fr = self.emoji_from_surrogates('\uD83C\uDDEB\uD83C\uddf7')
            us = self.emoji_from_surrogates('\ud83c\uddfa\ud83c\uddf8')
            switcher = {
                'fr': fr,
                'us': us,
                'soft': '\u2600',
                'discov': '',
                'test': 'TEST'}
            return switcher.get(filename, [])