#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 13:12:13 2022

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

