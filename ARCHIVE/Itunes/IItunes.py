
# Algorithme :
    
# 1. parse le xml et obtenir un dict avec les valeurs complètes de chaque track (id, name)
# 2. remove les '-' sans strip complètement. Parce que l'artist name est souvent dedans
# 2. parse les playlists et obtenir leur nom
# 3. pour chaque playlist:
    # obtenir le dict des ids de ses tracks
    # créer la playlist sur Spotify
    # associer à chaque id son nom dans un vecteur Names
    # sp.search(song)
    
    # montrer les songs introuvables, permettre d'éditer directement depuis le programmme 
    # (ou écrire les noms dans un txt et renvoyer bles indexs des duplis)
    
    # ajouter les sons à la playlist une fois que c'est satisfaisant, genre 90% (
    # len(introuvables)/len(names)<10%) (100% ideal et nécessaire seulement pour 25 les plus écoutées, 
    #                                    et 2012,2013 etc ... où l'ordre compte)
    
    # finir manuellement

import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
import datetime


from Util.credentials import *
from Itunes.itunes import Itunes

itunes = Itunes(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)
# itunes = Itunes()
itunes.most_recents_25_play_count()


print('stopped running at : ', datetime.datetime.now().time())
