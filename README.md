# Projects
Radar to discover new songs from selected artists  
Build complete of an artist  
Detect new track from updated playlists  
Clean liked songs  
Extends the spotify API with new functions (clean liked songs, duplicate playlist, ...)  
Experimentations with artists covers  
Automatically populate playlist from Ofive.tv movie clips  

# How to use
Register an app on Spotify for developers to get credentials
Create a credentials.py file in the Util folder, with the following variables  
CLIENT_ID='provided by Spotify on your developer page'  
CLIENT_SECRET='provided by Spotify on your developer page'  
REDIRECT_URI = 'http://google.com/'  
SCOPE = "playlist-modify-private playlist-modify-public user-read-private \
    ugc-image-upload user-read-recently-played user-top-read user-read-playback-position \
            user-read-playback-state user-modify-playback-state user-read-currently-playing \
    app-remote-control streaming playlist-read-private playlist-read-collaborative \
    user-follow-modify user-follow-read user-library-modify \
    user-library-read user-read-email"  
