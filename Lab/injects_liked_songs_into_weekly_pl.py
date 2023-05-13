#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 08:30:33 2022

@author: gabinfay
"""

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')

from Util.MySpotify import MySpotify
from Util.credentials import *

spo = MySpotify(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)


# pl_ids_to_inject = ['6YEYLii73vtKPo1eVF4k6C', '4rZ6xlHj1jw8wMpxwiP76Y', '7b2rEDUOKI86N0209J0eAb', '7soVXaB3hovB6cQGRnvrOO', '6Mr8oHnRxuGANvGq7kcrZN', '5cmZ8fn3a7RHyAhmv3JrXJ', '5eTqHxrkwswArqbF7KIr43']
# pl_ids_to_inject = ['6JnIQy89nseOIvnvPHxd2D', '5wk96NvPvW5XSfd7u4dgM6', '4EeVewO2ErcwCwzsXjL7dN', '1XwdJBvI9Zs6e84YE5lf4B', "2c7cXuSvITtlKtius4nX9K", '6Cm0bOMhbxxrc2A5SAlJ8w', '5ZpIR4gXDwzK0zzPHEDKtd']
# pl_bilan_id = spo.find_pl_id('yyyy', create_all = True)

# for pl_id_A in pl_ids_to_inject:
#     spo.injects_A_to_B(pl_id_A, pl_bilan_id, duplicates=False, reverse=False)

week, month = spo.get_week_number()
year = spo.get_year()

pl_name = f'S{int(week)}.{year}'
# pl_name = f'S{week}.{year}'

pl_id = spo.find_pl_id(pl_name, create_missing = True)

# spo.inject_liked_songs_into_pl(pl_id, duplicate=False, reverse=True, clean_afterwards = True, debug=False)



tr_ids, tr_names = spo.get_liked_songs()
#alr_in_names = spo.pl_tr_names(pl_id)
# if not duplicate:
#     to_add_ids = [tr_id for name, tr_id in zip(tr_names, tr_ids) if spo.normalize_name(name) not in alr_in_names]



# to_add_ids = tr_ids[27:]
# to_add_ids.reverse()
# spo.pl_add_tr(pl_id, to_add_ids)
# spo.clean_liked_songs(to_add_ids)








