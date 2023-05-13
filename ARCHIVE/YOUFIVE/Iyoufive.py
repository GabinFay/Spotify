Algorithme :

Recherche basée sur 'Mikano : Cool things can't die'
Scrape les pages principales Ofive
Récupérer les 10 premières pages, pour chaque vid, extraire le href vers la page concernée (parce que Youtube n'apparait que dessus)
pour i dans le link vers la page de la vid:
scrape le source code
ligne 658 : https://www.youtube.com/embed/PuxROocN-U4?feature=oembed (derniere mention de 'youtube' dans le source code)
ligne 783 : href="/2021/04/06/mikano-cool-kids-cant-die/#respond" => on a la date
on crée une playlist youtube en fonction de la date
on utilise l'api youtube.insert(id, pl_id) pour ajouter la vid à la playlist (si les vids ne sont pas déja dedans)

ALGORITHME 2:
query les sons des 2 derniers mois de Galbus:
query les sons des playlists youtube
rechercher les sons sur Youtube avec le nom
ajouter aux playlists ssi c'est pas déja dedans

UTILISATION:
suivre les playlists sur le compte Premium et ainsi avoir les vidéos download automatiquement.

