import spotipy
from spotipy import oauth2
from hidden_keys import *               #used to access CLIENT_ID and CLIENT_SECRET

REDIRECT_URI = "https://github.com/Matthew-W-G"
SCOPE = 'user-library-read user-read-currently-playing playlist-modify-private playlist-modify-public user-top-read'

CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE, cache_path=CACHE)
token_info = sp_oauth.get_cached_token()
token = ''

if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    token = token_info['access_token']

sp = spotipy.Spotify(auth=token)


