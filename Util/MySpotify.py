import spotipy
import os
import unidecode
import requests
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image, ImageDraw, ImageFont
import base64
import random
import datetime

class MySpotify(spotipy.Spotify):
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.auth_manager = self.oauth2_manager(client_id, client_secret, redirect_uri, scope)
        super().__init__(auth_manager=self.auth_manager)
        self.user_id = self.me()['id'] if '#' not in self.me()['id'] else self.me()['id'].replace('#','%23',1)
        self.pl_ids, self.pl_names = self.get_user_playlist_names_and_ids()
        self.fish_emoji = '\ud83d\udc1f'.encode('utf-16', 'surrogatepass').decode('utf-16')
    
    
    def ars_from_ids(self, ids):
        artists = []
        for y in self.chunks(ids, 50):
            artists.extend(self.artists(y)['artists'])
        return artists


    def chunks(self, foo, n):
        """Yield successive n-sized chunks from foo."""
        for i in range(0, len(foo), n):
            yield foo[i:i + n]
    

    def clean_liked_songs(self, liked_tr_ids):
        for tr_id in liked_tr_ids:
            self.current_user_saved_tracks_delete([tr_id])

    def clean_playlist(self, playlist_id):
        self.playlist_replace_items(playlist_id, [])
        
    def complete_txt_ids(self, filename, unsupervised = False):
        lines = self.read_txt_to_array(filename)
        
        full = []

        if all(len(line.split(' - ')) == 2 for line in lines):
            for line in lines:
                ar_name, ar_id = [x.strip('\n') for x in line.split(' - ', 1)]
                full.append([ar_name, ar_id])
        else:
            for line in lines:
                if len(line.split(' - ')) == 2:
                    ar_name, ar_id = [x.rstrip() for x in line.split(' - ', 1)]
                    full.append([ar_name, ar_id])
                else:
                    if unsupervised:
                        try:
                            artist = self.search(line, type="artist")["artists"]["items"][0]
                        except:
                            print (f'{line} was not found')
                    else:
                        test0 = False; j = 0
                        while test0 == False:
                            print("moi : ", line)
                            artist = self.search(line, type="artist")["artists"]["items"][j]
                            answer = input(artist["name"] + "\nEst ce le bon artiste ? (y)/(n) \n")
                            if answer == "y":
                                test0 = True
                            elif answer == "n":
                                j +=1
                    full.append([artist["name"], artist["id"]])
            self.write_2d_array_to_txt(full, filename)
        artists = self.ars_from_ids([y for x,y in full])
        return artists



    flatten = lambda self, seq: [k for l in seq for k in l]

    has_dupli = lambda self, seq: len(seq) > len(set(seq))

    normalize_string = lambda self, foo: unidecode.unidecode(foo.lower())

    def clean_dupli(self, L):
        return list(dict.fromkeys(L))
    
    def emoji_from_surrogates(self, surrogate_codes):
        return surrogate_codes.encode('utf-16',  'surrogatepass').decode('utf-16')

    def emoji_from_long_code(self, long_code):
        return self.emoji_from_surrogates(self.get_surrogates(long_code))
    
    def find_all_pl_ids_containing_foo(self, foo, name = False):
        if name:
            return [[pl_id, pl_name] for pl_id, pl_name in zip(self.pl_ids, self.pl_names) if foo in pl_name]            
        else:
            return [pl_id for pl_id, pl_name in zip(self.pl_ids, self.pl_names) if foo in pl_name]

    def find_pl_id(self, pl_names, create_missing = False, create_all = False, public=True):
        if type(pl_names) == str:
            pl_names = pl_names.split('aaaaaaaaaaaaaaaaaaaaaaa')
        pl_names = list(pl_names)
        pl_ids = [False for i in pl_names]
        k = 0
        while k < len(self.pl_ids) and not all(pl_ids):
            if self.pl_names[k] in pl_names:
                for j, l in enumerate(pl_names):
                    if l == self.pl_names[k]:
                        pl_ids[j] = self.pl_ids[k]
            k += 1
        if create_all:
            for i in [i for i,j in enumerate(pl_ids)]:
                pl_ids[i] = self.user_playlist_create(self.user_id, pl_names[i],public=public)["id"]
                self.pl_names.append(pl_names[i])
                self.pl_ids.append(pl_ids[i])
        elif create_missing:
            for i in [i for i,j in enumerate(pl_ids) if j == False]:
                pl_ids[i] = self.user_playlist_create(self.user_id, pl_names[i], public=public)["id"]
                self.pl_names.append(pl_names[i])
                self.pl_ids.append(pl_ids[i])
        ### to return a string if the query was for a single playlist
        if len(pl_ids) == 1:
            pl_ids = pl_ids[0]
        return pl_ids

    def get_year(self):
        date = datetime.datetime.now()
        return date.strftime("%D").split('/')[-1]
    
    def get_week_number(self):
        date = datetime.datetime.now()
        month = date.strftime("%B").lower()
        week_date = date.strftime("%D").split('/')
        week_number = datetime.date(int(week_date[2]), int(week_date[0]), int(week_date[1])).isocalendar()[1]
        return str(week_number), month
    
    def get_year(self):
        return str(datetime.date.today().year)[2:]

    def get_liked_songs(self):
        results = self.current_user_saved_tracks()
        tr = results['items']
        while results['next']:
            results = self.next(results)
            tr.extend(results['items'])
        tr_ids = [i['track']['id'] for i in tr]
        tr_names = [i['track']['name'] for i in tr]
        return tr_ids, tr_names

    def get_surrogates(self, long_code):
        h = int(np.floor((long_code - 0x10000) / 0x400) + 0xD800)
        l = int((long_code - 0x10000) % 0x400 + 0xDC00)
        return ''.join(map(chr, [h,l]))
    
    def get_nested_list_dim(self, seq):
        if not type(seq) == list:
            return []
        return [len(seq)] +self.get_nested_list_dim(seq[0])


    def get_path(self, filename):
        """ if file is in the same folder as the running program"""
        return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/" + filename

    def get_user_playlist_names_and_ids(self, user_id = False):
        if not user_id:
            user_id = self.user_id
        pl_ids = []
        pl_names = []
        results = self.user_playlists(user_id)
        playlists = results['items']
        while results['next']:
            results = self.next(results)
            playlists.extend(results['items'])
        for i in playlists:
            pl_ids.append(i['id'])
            pl_names.append(i['name'])
        return pl_ids, pl_names
    
    def injects_A_to_B(self, pl_id_A, pl_id_B, duplicates=False, reverse=False):
        A_tr_names, A_tr_ids = self.pl_tr_names_and_ids(pl_id_A)
        B_tr_names = self.pl_tr_names(pl_id_B)
        if not duplicates:
            to_add_ids = [id for name,id in zip(A_tr_names,A_tr_ids) if name not in B_tr_names]
        else:
            to_add_ids = A_tr_ids
        if not reverse:
            self.pl_add_tr(pl_id_B, to_add_ids)
        else:
            to_add_ids.reverse()
            self.pl_add_tr(pl_id_B, to_add_ids)
            
    def inject_liked_songs_into_pl(self, pl_id, duplicate=False, reverse=False, clean_afterwards = False, debug = False):
        tr_ids, tr_names = self.get_liked_songs()
        alr_in_names = self.pl_tr_names(pl_id)
        if not duplicate:
            to_add_ids = [tr_id for name, tr_id in zip(tr_names, tr_ids) if self.normalize_name(name) not in alr_in_names]
        else:
            to_add_ids = tr_ids
        if reverse:
            to_add_ids.reverse()
        if not debug:
            self.pl_add_tr(pl_id, to_add_ids)
        if clean_afterwards:
            self.clean_liked_songs(tr_ids)
        
    def normalize_name(self, foo):
        foo = unidecode.unidecode(foo.lower())
        to_cut = [' - ', ' (', ' [',' (feat',' (Feat',' (Prod',' (prod',' (with',' (from',' (From',' feat']
        for i in to_cut : foo = foo.split(i)[0]
        return foo
    
    def oauth2_manager(self, client_id, client_secret, redirect_uri, scope):
        oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
        return oauth

    def order_by_popularity(self, pl_id):
        pl_tr = self.pl_tr(pl_id)
        sorted_ids = [i['track']['id'] for i in sorted(pl_tr, key=lambda item: item['track']['popularity'], reverse=True)]
        self.clean_playlist(pl_id)
        self.pl_add_tr(pl_id, sorted_ids)

    def pl_tr(self, pl_id):
        results = self.playlist_tracks(pl_id, market = 'FR')
        pl_tr = results['items']
        while results['next']:
            results = self.next(results)
            pl_tr.extend(results['items'])
        pl_tr = [i for i in pl_tr if i['track'] != None]
        pl_tr = [i for i in pl_tr if i['track']['id'] != None]
        return pl_tr

    def pl_tr_names(self, pl_id):
        pl_tr = self.pl_tr(pl_id)
        tr_names = [self.normalize_name(i["track"]["name"]) for i in pl_tr]
        return tr_names
    
    def pl_tr_ids(self, pl_id):
        pl_tr = self.pl_tr(pl_id)
        tr_ids = [i["track"]["id"] for i in pl_tr]
        return tr_ids

    def pl_tr_names_and_ids(self, pl_id):
        pl_tr = self.pl_tr(pl_id)
        tr_names = [self.normalize_name(i["track"]["name"]) for i in pl_tr]
        tr_ids = [i["track"]["id"] for i in pl_tr]
        return tr_names, tr_ids


    def pl_add_tr(self, pl_id, tr_ids):
        if type(tr_ids) == str:
            tr_ids = tr_ids.split('aaaaaaaaaaaaaaaaaaaaaaa')
        tr_ids = [tr_ids[i:i + 100] for i in range(0, len(tr_ids), 100)]
        for j in tr_ids:
            self.playlist_add_items(pl_id, items=j)
    
    def read_txt_to_array(self, filename):
        with open(filename, 'r') as us:
            lines = us.readlines()
            us.close()
        return [i.strip('\n') for i in lines]

    def unfollow_pl_from_ids(self, pl_ids):
        if type(pl_ids) in [tuple, list]:
            for i in pl_ids:
                if i != False:
                    self.current_user_unfollow_playlist(i)
        else:
            if pl_ids != False:
                self.current_user_unfollow_playlist(pl_ids)
                
    def unfollow_pl_from_names(self, pl_names, all_occ = False):
        pl_ids = self.find_pl_id(pl_names)
        self.unfollow_pl_from_ids(pl_ids)
        if all_occ == True:
            if not isinstance(pl_ids,bool):
                while any(pl_ids):
                        self.unfollow_pl_from_ids(pl_ids)
                        pl_ids = self.find_pl_id(pl_names)
            else:
                while pl_ids != False:
                    self.unfollow_pl_from_ids(pl_ids)
                    pl_ids = self.find_pl_id(pl_names)

    def write_pl_ids_to_txt(self, pl_ids, path):
        with open(path, 'w+') as f:
            for item in pl_ids:
                f.write("%s\n" % item)

    def write_2d_array_to_txt(self, array, filename):
        with open(filename, 'w+') as f:
            for x, y in array:
                f.write('{} - {}\n'.format(x, y))
    
    def write_1d_array_to_txt(self, array, filename,mode='w+'):
        with open(filename, mode) as f:
            for x in array:
                f.write('{}\n'.format(x))



############ GRAPHICS ##########
#~~~~ util ~~~~~~#

    def im_2_b64(self, image, quality):
        buff = BytesIO()
        image.save(buff, format="JPEG", quality=quality)
        img_str = base64.b64encode(buff.getvalue())
        return img_str

    def plt_imshow(self, img):
        plt.axis('off')
        plt.imshow(img)
        plt.show()
            

    def arrshow(self, im_array):
        img = PIL.Image.fromarray(im_array, "RGB")
        self.plt_imshow(img)
        return img

    def apply_average(self, img):
        av_array = np.average(np.array(img), axis=2)
        return PIL.Image.fromarray(av_array, "RGB")
        
    def apply_pixelization(self, img, pixel_size):
        img = img.resize(
            (img.size[0] // pixel_size, img.size[1] // pixel_size),
            PIL.Image.NEAREST
        )
        img = img.resize(
            (img.size[0] * pixel_size, img.size[1] * pixel_size),
            PIL.Image.NEAREST
        )
        return img

#~~~~~ functions ~~~~~#

    def update_complete_cover(self, artist, pl_id):
        i = 0 ; err = False
        while not err and i < len(artist['images']):
            try:
                response = requests.get(artist['images'][i]['url'])
                img = PIL.Image.open(BytesIO(response.content))
                full_im64 = self.im_2_b64(img, quality = 70)
                self.playlist_upload_cover_image(pl_id, full_im64)
                err = True
            except IndexError:
                pass
            except requests.exceptions.HTTPError:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except spotipy.exceptions.SpotifyException:
                pass
                i += 1

    def upload_cover(self, pl_id, img):
        k = 70
        size = 1000
        while size > 185:
            full_im64 = self.im_2_b64(img, quality = k)
            size = 0.75/1000*len(full_im64)
            k -= 5
        self.playlist_upload_cover_image(pl_id, full_im64)

    def cover_grid(self, objects, pl_id, pixelize = False, average = False):
        img = self.grid(objects, pixelize=pixelize, average=average)
        self.upload_cover(pl_id, img)

    def get_list_of_images(self, objects):
        size = 320
        expected_size=(size, size, 3)
        imglist=[]
        for obj in objects:
            try:
                for j in obj["images"]:
                    if abs(j['height'] -  expected_size[0]) < 50:
                        response = requests.get(j['url'])
                        img = PIL.Image.open(BytesIO(response.content))
                        imglist.append(img)
            except requests.exceptions.HTTPError:
                n = 0 ; test = False
                while not test and n < len(obj['images']):
                    try:
                        response = requests.get(obj['images'][n]['url'])
                        img = PIL.Image.open(BytesIO(response.content))
                        imglist.append(img)
                        test = True
                    except requests.exceptions.HTTPError:
                        n += 1
        return imglist
    
    def grid(self, objects, pixelize=False, average=False):
        imglist = self.get_list_of_images(objects)
        backcolor = (245, 245, 220)
        nrows = int(np.ceil(np.sqrt(len(imglist))))
        holes = random.sample(range(nrows*nrows), nrows*nrows-len(imglist))
        # single_im_size = int(np.ceil(expected_size/np.ceil(np.sqrt(len(imglist)))))
        single_im_size = min([min(img.size) for img in imglist])
        im_size = int(nrows * single_im_size)
        new_im = PIL.Image.new('RGB', (im_size, im_size), backcolor)
        #Iterate through a 4 by 4 grid with 100 spacing, to place my image
        k = 0 ; n = 0
        for i in range(0,im_size,single_im_size):
            for j in range(0,im_size,single_im_size):
                #paste the image at location i,j:
                if n not in holes:
                    img = imglist[k]
                    #Here I resize my opened image, so it is no bigger than 100,100
                    img = img.resize((single_im_size, single_im_size))                    
                    new_im.paste(img, (i,j))
                    # self.plt_imshow(new_im)
                    k += 1
                n += 1
        if average:
            new_im = self.apply_average(new_im)
        if pixelize:
            new_im = self.apply_pixelization(new_im, 40)
        return new_im

    def name_grid(self, ar_names):
        random.shuffle(ar_names)
        img = Image.new('RGB', (10000, 10000), color = (73, 109, 137))
        fnt = ImageFont.truetype('NewTegomin-Regular.ttf', 750)
        d = ImageDraw.Draw(img)
        for i in ar_names:
            d.text((10,10), "Hello world", font=fnt, fill=(0, 0, 0))
            self.plt_imshow(img)

###### This is the discov used by radar to create the weekly spotting new artists playlist and by iDiscov, it should lie in its own bed

    def discov(self, filename = False, discov_name = False, ids = False, tr_num = 5, unsupervised = True):
        if filename or ids:
            if filename:
                if unsupervised:
                    artists = self.complete_txt_ids(filename, unsupervised = True)
                else:
                    artists = self.complete_txt_ids(filename, unsupervised = False)                    
            else:
                artists = self.ars_from_ids(ids)
            if not discov_name:
                discov_name = self.discov_name()
            pl_id = self.find_pl_id(discov_name, create_missing=True)
            # self.clean_playlist(pl_id)
            self.cover_grid(artists, pl_id)
            for artist in artists:
                self.one_discov(artist, pl_id, tr_num)
            
    def discov_name(self, pl_name):
        return self.emoji_from_long_code(0x1F31C) + ' ' + pl_name + ' ' + self.emoji_from_long_code(0x1F31B)

    def one_discov(self, artist, pl_id, tr_num):
        top_tracks = self.artist_top_tracks(artist['id'], country='US')['tracks']
        tr_ids = [i['id'] for i in top_tracks][:tr_num]
        tr_names = [i['name'] for i in top_tracks][:tr_num]
        alr_in_names = self.pl_tr_names(pl_id)
        to_add_ids = [i for i,j in zip(tr_ids,tr_names) if self.normalize_name(j) not in alr_in_names]
        self.pl_add_tr(pl_id, to_add_ids)