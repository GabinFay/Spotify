##  26.02.22 ###

import sys
from os.path import expanduser

from Util.MySpotify import MySpotify
sys.path.append(expanduser('~')+'/Documents/Spotify')

import time
import datetime
import requests
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


class Top(MySpotify):
    
    def top(self):
        ### world ###
        week_number, month = self.get_week_number()
       
        world_top50_archive_id = self.find_pl_id('world top50 archive', create_missing=True)
        world_top_S_id = self.find_pl_id(f'world top S{week_number}', create_missing=True)
        world_top50_id = '37i9dQZEVXbMDoHDwVN2tF'
        alr_in_world_tr_names = self.pl_tr_names(world_top50_archive_id)
        world_top50_tr_names, world_top50_tr_ids = self.pl_tr_names_and_ids(world_top50_id)
        world_to_add_ids = [tr_id for tr_name, tr_id in zip(world_top50_tr_names, world_top50_tr_ids) if tr_name not in alr_in_world_tr_names]
        self.pl_add_tr(world_top_S_id, world_to_add_ids)
        self.pl_add_tr(world_top50_archive_id, world_to_add_ids)
     
        france_top50_archive_id = self.find_pl_id('france top50 archive', create_missing=True)
        france_top_S_id = self.find_pl_id(f'france top S{week_number}', create_missing=True)
        france_top50_id = '37i9dQZEVXbIPWwFssbupI'
        alr_in_france_tr_names = self.pl_tr_names(france_top50_archive_id)
        france_top50_tr_names, france_top50_tr_ids = self.pl_tr_names_and_ids(france_top50_id)
        france_to_add_ids = [tr_id for tr_name, tr_id in zip(france_top50_tr_names, france_top50_tr_ids) if tr_name not in alr_in_france_tr_names]
        self.pl_add_tr(france_top_S_id, france_to_add_ids)
        self.pl_add_tr(france_top50_archive_id, france_to_add_ids)
        