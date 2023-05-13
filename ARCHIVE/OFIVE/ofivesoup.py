#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:02:41 2022

@author: gabinfay
"""

# -*- coding: utf-8 -*-
"""
April 2022
@author: gabin
"""

######### SPOTIFY AUTH ################

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify

import datetime
import requests
import re



class Ofive(MySpotify):

    def ofive(self, until_page):
        
        NOTFOUND=[]
        to_include = '-'
        not_to_include = ['movies' ,'records', 'interview']
        Href = self.get_href(until_page, to_include, not_to_include)
        
        tr_dates = [i.split('/')[3:-2] for i in Href]
        tr_names = [' '.join(re.split('/|-', i)[6:-1]) for i in Href]

        clean_tr_names = []
        for i in tr_names:
            for k in ['ft.', 'featuring', 'feat.', 'ft', 'feat', 'aap', 'producer', 'prod']:
                i = i.replace(k, '')
            clean_tr_names.append(i)
        
        for date, tr_name in zip(tr_dates, clean_tr_names):
            week_number, _ = self.get_week_number()
            month = datetime.datetime(int(date[0]), int(date[1]), int(date[2])).strftime("%B").lower()
            ofive_s_id = self.find_pl_id(self.fish_emoji + ' S' + week_number + ' ' + self.fish_emoji, create_missing=True)
            pl_name = self.fish_emoji + ' ' + month + ' ' + str(date[0])[2:] + ' ' + self.fish_emoji
            pl_id = self.find_pl_id(pl_name, create_missing=True)
            alr_in_names = self.pl_tr_names(pl_id)
            tr = self.search(tr_name, type="track", market="FR", limit=1)['tracks']['items']
            if tr != []:
                tr_id = tr[0]["id"] ; tr_name = tr[0]['name']
                if self.normalize_name(tr_name) not in alr_in_names:
                    print(tr[0]['artists'][0]['name'], ' - ', tr_name)
                    self.pl_add_tr(pl_id, tr_id)
                    self.pl_add_tr(ofive_s_id, tr_id)
                    alr_in_names.append(self.normalize_name(tr_name))
            else:
                NOTFOUND.append(date[0] +'-'+date[1] + '    ' + tr_name)
        print('########### NOTFOUND ###########')
        for i in NOTFOUND: print(i)
    
    def get_href(self, until_page, to_include, not_to_include):

    
    all_script_tags = soup.select('source')
    matched_images_data = re.findall(r"https:\/\/i\.guim\.co\.uk\/img\/media\/[^\/]*\/[^\/]*\/master\/[0-9]*\.jpg\?width=1010&amp;quality=85[\S\n]*", str(all_script_tags))
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36')]
    urllib.request.install_opener(opener)
    for ii,i in enumerate(matched_images_data):
        try:
            urllib.request.urlretrieve(i.replace(';','&').replace('&amp',''), f'/home/gabinfay/RN/Guard/yessai{ii}.png')
        except:
            print(ii)
            pass
        if isinstance(to_include,str):
            to_include = to_include.split('aaaaaaaaaaaaaaaaaaaaaaa')
        if isinstance(not_to_include,str):
            not_to_include = not_to_include.split('aaaaaaaaaaaaaaaaaaaaaaa')
        Href = []
        for num in reversed(range(1,until_page)):
            print(num)
            page = []
            html = requests.get("http://www.ofive.tv/page/"+str(num)+"/")
            soup = BeautifulSoup(html.text, 'lxml')
            href_tags = soup.select('a')
            ### regex : year number between 2015 & 2014 etc
            urls = re.findall(r"http://www.ofive.tv/[2015-2024]/",str(href_tags))
                if i[:31] in ['href="http://www.ofive.tv/'+str(j)+'/' for j in range(2015,2024)]:
                    not_in_test = [j not in i for j in not_to_include]
                    in_test = [j in i for j in to_include]
                    not_in_test.extend(in_test)
                    if all(not_in_test):
                        page.append(i)
            page.reverse()
            Href.extend(page)
        return Href