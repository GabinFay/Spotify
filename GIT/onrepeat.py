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


class OnRepeat(MySpotify):
    
    def onrepeat(self):
        week_number, month = self.get_week_number()
        on_repeat_archive_id = self.find_pl_id('On Repeat 2022', create_missing=True)        
        on_repeat_id = self.find_pl_id(f'On Repeat')
        alr_in_on_repeat_tr_ids = self.pl_tr_ids(on_repeat_archive_id)
        on_repeat_tr_ids = self.pl_tr_ids(on_repeat_id)
        to_add_ids = [i for i in on_repeat_tr_ids if i not in alr_in_on_repeat_tr_ids]
        self.pl_add_tr(on_repeat_archive_id, to_add_ids)