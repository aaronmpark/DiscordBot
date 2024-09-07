import requests
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect


spotifyClientID = '6ed94440b43b4b369d3194454d3216df'
spotifyClientSecret = '51ebbef481914102a996a06fa08a3253'


app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'sfjsdnfdgn23tk2ngewg2ege3h#3532gf'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect():
    session.clear() #ensures previous sessions are cleared
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code) #exchanges oauth code for access token
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', external=True))

@app.route('/saveDiscoverWeekly')

def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    
    return("OAUTH SUCCESSFUL")

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', eternal=False))
    
    now = int(time.time())

    is_expired = token_info['expired_at'] = now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_ouath.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        spotifyClientID,
        spotifyClientSecret,
        redirect_url = url_for('redirect'), _external=True,
        scope = 'user-library-read playlist-modify-public playlist-modify-private'
    )


"""
def create_playlist(name, public):
    response = requests.post('https://api.spotify.com/users/mx6j6o2jlqjj8qjrce07o9kgi/playlists',
                             heaers={"Authorization": f"Bearer {spotifyClientID}"}
                             ,
                             json={
                                 "name": name,
                                 "public": public
                             }
                        )
    json_resp = response.json()
    return json.resp
"""

app.run(debug=True)