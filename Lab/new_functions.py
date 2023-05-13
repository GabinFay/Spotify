import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify
from Util.credentials import *

spo = MySpotify(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

#%%

import datetime

def duplicate_user_lib(user_id, public=False):
    spied_pl_ids, spied_pl_names = spo.get_user_playlist_names_and_ids(user_id=user_id)
    my_pl_ids = spo.find_pl_id(spied_pl_names, create_all=True, public=public)
    for my_pl_id, spied_pl_id in zip(my_pl_ids,spied_pl_ids):
        spied_pl_tr_ids = spo.pl_tr_ids(spied_pl_id)
        spo.pl_add_tr(my_pl_id, spied_pl_tr_ids)


def clean_A_from_B(pl_id_A, pl_id_B):
    A_pl_tr_names, A_pl_tr_ids = spo.pl_tr_names_and_ids(pl_id_A)
    B_pl_tr_names = spo.pl_tr_names(pl_id_B)
    to_add_ids = [id for name,id in zip(A_pl_tr_names, A_pl_tr_ids) if name not in B_pl_tr_names]    
    spo.clean_playlist(pl_id_A)
    spo.pl_add_tr(pl_id_A, to_add_ids)

def songs_in_A_but_not_B_go_in_C(pl_id_A, pl_id_B, pl_name_C):
    A_pl_tr_names, A_pl_tr_ids = spo.pl_tr_names_and_ids(pl_id_A)
    B_pl_tr_names = spo.pl_tr_names(pl_id_B)
    to_add_ids = [id for name,id in zip(A_pl_tr_names, A_pl_tr_ids) if name not in B_pl_tr_names]
    pl_id_C = spo.user_playlist_create(spo.user_id, pl_name_C)["id"]
    spo.pl_add_tr(pl_id_C, to_add_ids)

def duplicate_playlist(old_pl_id, new_name = False, order_by_pop = False):
    old_pl = spo.playlist(old_pl_id)
    if new_name:
        name = new_name
    elif order_by_pop:
        name = '🏆 ' + old_pl['name'] + ' 🏆'
    else:
        name = old_pl['name']
    if order_by_pop:
        new_pl_id = spo.user_playlist_create(spo.user_id, name)['id']
        old_pl_tr = spo.pl_tr(old_pl_id)
        sorted_ids = [i['track']['id'] for i in sorted(old_pl_tr, key=lambda item: item['track']['popularity'], reverse=True)]
        spo.pl_add_tr(new_pl_id, sorted_ids)
    else:
        new_pl_id = spo.user_playlist_create(spo.user_id, name)['id']
        old_pl_tr_ids = spo.pl_tr_ids(old_pl_id)
        spo.pl_add_tr(new_pl_id, old_pl_tr_ids)



def pl_ids_from_txt(filename):
    with open(filename, 'r') as fp:
        lines = fp.readlines()
        fp.close()
    pl_ids = [i.replace('\n','') for i in lines]
    return pl_ids
    
def star_a_playlist(pl_id):
    star= '\u2b50'
    pl = spo.user_playlist(spo.user_id,pl_id)
    star_pl_name = f"{star} {pl['name']} {star}"
    duplicate_playlist(pl_id, new_name=star_pl_name)


#%% 
### ESPIONNAGE ###

# THEOCHAV_ID = '1291166989'
# PG_ID = '21la6726setn7yyak4qkcb5ay'
# PAUL_LAINE_ID='6aoEZ8IQfEOd8ixtzxpikE'

# duplicate_user_lib(PG_ID)

# #%% STAR PLAYLISTS

# star_ids = pl_ids_from_txt('to_star.txt')
# for star_id in star_ids:
#     star_a_playlist(star_id)

#%% GIANT YEARLY PLAYLIST

# a_year_ids = pl_ids_from_txt('all_playlists_of_a_year.txt') ##this countains all playlists you want in the global yyyy playlist
# yyyy_id = spo.find_pl_id('2020', create_all=True)
# for pl_id in a_year_ids:
#     injects_A_to_B(pl_id, yyyy_id, duplicates=False)
    
#%% ORDER BY POP

# pl_ids = '2t8p9tTvZoSR6y9XHKLTef'
# pl_ids = '042t7Ohn7EcmPEHPtVQ1s2'
# pl_ids = '3Smvuh3eqrO9nyIzGIjciW'
# pl_ids = '4ZSGvHRyKR1yR1QBRhNcTw'

# duplicate_playlist(pl_ids, order_by_pop=True)

#%% Duplicate playlist

pl_id = "47lz5hV5boVEpSKkpUgjKS"

duplicate_playlist(pl_id, new_name = 'aurel slow bonus')