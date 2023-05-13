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
from Util.Offline import Offline
from copy import deepcopy

class Itunes(MySpotify):

    def most_recents_25_play_count(self):
        filename='lib.2018.perfect.xml'
        # self.complete_plist_file(filename)
        with open(filename, 'rb') as fp:
            plist = plistlib.load(fp)
        tracks = [] ; date_added = []
        for k,v in plist['Tracks'].items():
            tracks.append(v)
        sorted_tracks = sorted(tracks, key=lambda k: k['Date Added'])

        play_counts = [] ; ids = [] ; names = []
        for k,v in plist['Tracks'].items():
            if 'Podcast' not in v and '(notfound)' not in v['Name']:
                play_count = v['Play Count'] if 'Play Count' in v else v['Track Count']
                if play_count >= 25:
                    play_counts.append(play_count)
                    ids.append(v['Spotify ID'])
                    names.append(v['Name'])
        pl_name = 'Oldest 25 most listened'
        pl_id = self.find_pl_id(pl_name, create_missing = True)
        alr_in_names = self.pl_tr_names(pl_id)
        if alr_in_names == []:
            self.pl_add_tr(pl_id, ids)
        ids.reverse()
        pl_name = 'Newest 25 most listened'
        pl_id = self.find_pl_id(pl_name, create_missing = True)
        alr_in_names = self.pl_tr_names(pl_id)
        if alr_in_names == []:
            self.pl_add_tr(pl_id, ids)
        print('exit')
            
    def year_most_listened(self):
        filename='lib.2018.perfect.xml'
        # self.complete_plist_file(filename)
        with open(filename, 'rb') as fp:
            plist = plistlib.load(fp)
        playlists = plist['Playlists']
        for i in playlists:
            if 'Playlist Items' in i and 'Podcasts' not in i:
                if i['Name'] in [str(i) for i in range(2012,2018)]:
                    pl_tr_relative_ids = [j['Track ID'] for j in i['Playlist Items']]
                    # full_tracks = dict.fromkeys(pl_tr_relative_ids)
                    full_tracks = {key: None for key in pl_tr_relative_ids}
                    for k,v in plist['Tracks'].items():
                        if 'Podcast' not in v and v['Track ID'] in pl_tr_relative_ids:
                            full_tracks[v['Track ID']] = v
                    for k in deepcopy(full_tracks):
                        if full_tracks[k] == None: full_tracks.pop(k)
                    pl_id = self.find_pl_id(i['Name'] + ' ML', create_missing=True)
                    tr_ids = [v['Spotify ID'] for k,v in full_tracks.items() if 'notfound' not in v['Name']]
                    play_counts = [v['Play Count'] if 'Play Count' in v else v['Track Count'] for k,v in full_tracks.items() if 'notfound' not in v['Name']]
                    pop_ids = [x for _,x in sorted(zip(play_counts,tr_ids))]
                    pop_ids.reverse()
                    self.pl_add_tr(pl_id, pop_ids)

    def mirror_to_spotify(self):
        filename='lib.2018.perfect.xml'
        # self.complete_plist_file(filename)
        with open(filename, 'rb') as fp:
            plist = plistlib.load(fp)
        playlists = plist['Playlists']
        for i in playlists:
            if 'Playlist Items' in i and 'Podcasts' not in i:
                print(i['Name'])
                pl_tr_relative_ids = [j['Track ID'] for j in i['Playlist Items']]
                # full_tracks = dict.fromkeys(pl_tr_relative_ids)
                full_tracks = {key: None for key in pl_tr_relative_ids}
                for k,v in plist['Tracks'].items():
                    if 'Podcast' not in v and v['Track ID'] in pl_tr_relative_ids:
                        full_tracks[v['Track ID']] = v
                for k in deepcopy(full_tracks):
                    if full_tracks[k] == None: full_tracks.pop(k)
                pl_id = self.find_pl_id(i['Name'], create_missing=True)
                tr_ids = [v['Spotify ID'] for k,v in full_tracks.items() if 'notfound' not in v['Name']]
                self.pl_add_tr(pl_id, tr_ids)

    def itunes_most_listened(self, plist, cut=None):
        play_counts = [] ; ids = []
        for k,v in plist['Tracks'].items():
            if 'Podcast' not in v and '(notfound)' not in v['Name']:
                play_counts.append(v['Play Count'] if 'Play Count' in v else v['Track Count'])
                ids.append(v['Spotify ID'])
        pop_ids = [x for _,x in sorted(zip(play_counts,ids))]
        pop_ids.reverse()
        if cut != None:
            pop_ids = pop_ids[:cut]
        pl_name = 'Itunes Most Listened' if cut==None else 'Itunes ' + str(cut) + ' best'
        pl_id = self.find_pl_id(pl_name, create_missing = True)
        alr_in_names = self.pl_tr_names(pl_id)
        if alr_in_names == []:
            self.pl_add_tr(pl_id, pop_ids)
        print('exit')
        

    def complete_plist_file(self, filename):
        with open(filename, 'rb') as fp:
            plist = plistlib.load(fp)
            
        plist_copy = deepcopy(plist)
        
        for k,v in plist['Tracks'].items():
            if 'Podcast' not in v and '(notfound)' not in v['Name']:
                search_term = v['Name'] + ' ' +  v['Artist'] if 'Artist' in v else v['Name']
                search_term = self.normalize_name_for_search(search_term)
                tr = self.search(search_term, type='track', limit=1)['tracks']['items']
                if tr == []:
                    while tr == []:
                        correction = input(search_term + '\n')
                        if correction != '':
                            if correction != 'n':
                                tr = self.search(correction, type='track', limit=1)['tracks']['items']
                                if tr != [] :
                                    print(tr[0]['name'] + ' - ' + tr[0]['artists'][0]['name'])
                                    if input('ok ? y/n\n') == 'n': tr = []
                            else:
                                tr = 'notfound'
                print(k)
                if tr != 'notfound':
                    plist_copy['Tracks'][k]['Name'] = tr[0]['name']
                    plist_copy['Tracks'][k]['Artist'] = tr[0]['artists'][0]['name']
                    plist_copy['Tracks'][k]['Spotify ID'] = tr[0]['id']
                else:
                    plist_copy['Tracks'][k]['Name'] += ' (notfound)'
                    
            # if int(k)%500 == 0:
            #     with open(filename, 'wb+') as fp:
            #         plistlib.dump(plist_copy, fp)
                    
        with open(filename, 'wb+') as fp:
            plistlib.dump(plist_copy, fp)
        
        # with open('lib.2018.test.xml', 'wb+') as fp2:
        #     plistlib.dump(plist2, fp2)
        
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
    
    
    def normalize_name_for_search(self, tr_name):
            tr_name = unidecode.unidecode(tr_name).lower()
            to_remove = ['-','(',')','[',']',',',
                            ' feat. ', ' featuring ', ' feat ', ' & ',' ft. ',' ft ', ' mix '
                            ' version ', ' clean ', ' video ', ' prod ', ' produced ', ' bonus ', ' track '
                            ' clip ', '  officiel ', ' radio ', ' edit ', ' french '
                            ' by ', ' producer ', ' official ', ' with ',' from ', 'explicit', ' x ', 'lyrics','&quot']
            for i in to_remove : tr_name = tr_name.replace(i, ' ')
            return tr_name