import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')



from Util.credentials import *
from Util.MySpotify import MySpotify


discov = MySpotify(client_id=CLIENT_ID, 
              client_secret=CLIENT_SECRET,
              redirect_uri=REDIRECT_URI,
              scope=SCOPE)

week_number, month = discov.get_week_number()
# discov_name = discov.discov_name(f'S{week_number}')
discov_name = discov.discov_name("killian")
# discov_name = discov.discov_name('grime')

discov.discov(
    filename='discov.txt',
    discov_name = discov_name,
    tr_num=10, unsupervised = False
    )