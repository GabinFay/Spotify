import sys
from os.path import expanduser
sys.path.append(expanduser('~')+'/Documents/Spotify')
from Util.MySpotify import MySpotify



class Complete(MySpotify):
    
    def complete(self, filename, plus_txt=True, update_descr = False):
        if plus_txt:
            artists = self.complete_txt_ids('txt/'+filename)
        else:
            artists = self.complete_txt_ids(filename)
        pl_names = [f"{artist['name']} Complete" for artist in artists]
        pl_ids = self.find_pl_id(pl_names, create_missing=True)
        if update_descr:
            self.update_completes_description(pl_ids)
        if isinstance(pl_ids,str):
            pl_ids=pl_ids.split('aaaaaaa')
        for artist, pl_id in zip(artists, pl_ids):
            self.one_complete(artist, pl_id)

    def update_completes_description(self, pl_ids):
        # description = "updated Completes available here : "
        description = "Updated every month ! Sort by recently added to get albums in the right order"
        for pl_id in pl_ids:
            self.user_playlist_change_details(self.user_id, pl_id, description=description)

    def get_all_albums(self, ar_id):
        results = self.artist_albums(ar_id, country='FR')
        ar_albums = results["items"]
        while results["next"]:
            results = self.next(results)
            ar_albums.extend(results["items"])
        return ar_albums

    """entry :
    {ar_albums} : list of all albums items of an artist
    {ar_name} : artist_name
    exit :
    {ar_tr_ids} : all track ids of an artist, where explicit version is chosen over unexplicit if possible
    {ar_tr_names} : all track names of an artist
    """
    def normalized_artist_complete(self, artist, ar_name):
        ar_albums = self.get_all_albums(artist['id'])
        ar_tr_names = [] ; ar_tr_ids = [] ; is_explicit = [] ; explicit = []
        for i in ar_albums:
            tracks = self.album_tracks(i["id"], market = 'FR')
            if i["album_group"] in ["album","single"]:
                for j in tracks["items"]:
                    if self.normalize_name(j["name"]) not in ar_tr_names:
                        ar_tr_names.append(self.normalize_name(j["name"]))
                        ar_tr_ids.append(j["id"])
                        is_explicit.append(j['explicit'])
                    elif j['explicit']:
                        explicit.append(j["id"])

            else:
                for j in tracks["items"]:
                    if len(j["artists"]) > 1:
                        for k in j["artists"][1:]:
                            if k["name"] == ar_name:
                                if self.normalize_name(j["name"]) not in ar_tr_names:
                                    ar_tr_names.append(self.normalize_name(j["name"]))
                                    ar_tr_ids.append(j["id"])
                                    is_explicit.append(j['explicit'])
                                elif j['explicit']:
                                    explicit.append(j["id"])
        # ALGO : above, duplicates (tracks that don't enter the if) are often due to explicit vs censored versions, having the same name)
        # Duplicates are found only with the 2nd similar track. If it is explicit, its id is added to {explicit}
        # Then, you replace the unexplicit version by the explicit one with the below code
        for i in explicit:
            track = self.track(i)
            for j, k in enumerate(ar_tr_names):
                if k == self.normalize_name(track['name']) and not is_explicit[j]:
                    ar_tr_ids[j] = track['id']
        return (ar_tr_ids, ar_tr_names)

    def one_complete(self, artist, pl_id):
        self.update_complete_cover(artist, pl_id)
        ar_tr_ids, ar_tr_names = self.normalized_artist_complete(artist, artist['name'])
        alr_in_names = self.pl_tr_names(pl_id)
        new_ids = [ar_tr_ids[i] for i, item in enumerate(ar_tr_names) if item not in alr_in_names]
        new_names = [item for i, item in enumerate(ar_tr_names) if item not in alr_in_names]        
        if new_names != [] and alr_in_names != []:
            for i,j in zip(new_ids, new_names):
                print(artist['name'] + ' --- ' + j + '\n')
        new_ids.reverse()
        new_names.reverse()
        self.pl_add_tr(pl_id, new_ids)
        return new_ids, new_names, alr_in_names