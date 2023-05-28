import os
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify
import requests
import urllib
import json
from flask_cors import CORS
import random


app = Flask(__name__)
CORS(app)
load_dotenv()
# Replace these placeholders with your actual client ID and client secret
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
# Spotify API endpoints
AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
# Redirect URI that Spotify will redirect back to after authentication
REDIRECT_URI = 'http://localhost:8000/callback'

@app.route('/')
def index():
    return '<a href="/login">Log in with Spotify</a>'

@app.route('/login')
def login():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-read-private user-read-email user-top-read playlist-modify-private',
    }
    authorize_url = f'{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}'
    return redirect(authorize_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    resp = response.json()
    return redirect('http://localhost:5500/FrontEnd/?token=' + resp['access_token'])

@app.route('/yourmoodplaylist', methods=['POST'])
def get_your_mood_playlist():
    token = json.loads(request.data)['authToken']
    mood_keyword = json.loads(request.data)['mood']
    auth_header = {'Authorization': 'Bearer ' + token}
    url = 'https://api.spotify.com/v1/me/top/artists'
    result = requests.get(url, headers=auth_header)

    artists_info = extract_artist_info(result)
    filter_artists(mood_keyword, artists_info)
    user_id = get_user_spotify_id(auth_header)
    similar_songs = get_similar_artists_top_songs(artists_info, auth_header)
    playlist_id, playlist_uri = create_new_playlist(user_id, token)
    playlist_add_songs(playlist_id, playlist_uri, similar_songs, token)
    return jsonify(result.json())

def extract_artist_info(result) -> dict:
    artist_info = {}
    for index in range(len(result.json()['items'])):
        info_dict = {}
        info_dict['id'] = result.json()['items'][index]['id']
        info_dict['genres'] = result.json()['items'][index]['genres']
        artist_info[result.json()['items'][index]['name']] = info_dict
    return artist_info

def filter_artists(mood_keyword, artists_info):
    mood_dict = {
        'happy': ['children', 'comedy', 'happy', 'kids', 'j-dance', 'j-idol', 'j-pop'
                  'j-rock', 'k-pop', 'pop', 'power-pop', 'indie', 'indie-pop'],
        'sad': ['blues', 'emo', 'honky-tonk', 'sad', 'indie', 'indie-pop'],
        'angry': ['alt-rock', 'black-metal', 'death-metal', 'goth', 'grindcore',
                  'grunge', 'hard-rock', 'hardcore', 'heavy-metal', 'industrial', 'metal',
                  'metal-misc', 'metalcore', 'psych-rock', 'punk', 'punk-rock', 'rock'],
        'romantic': ['country', 'romance'],
        'focused': ['acoustic', 'classical', 'groove', 'guitar', 'jazz',
                    'new age', 'piano', 'study'],
        'hype': ['breakbeat', 'chicago-house', 'club', 'dance', 'deep-house',
                 'detroit-techno', 'disco', 'drum-and-bass', 'dub', 'dubstep', 'edm',
                 'electro', 'electronic', 'forro', 'funk', 'garage', 'hardstyle',
                 'hip-hop', 'holidays', 'house', 'idm', 'minimal-techno', 'party',
                 'post-dubstep', 'progressive-house', 'road-trip', 'soul', 'summer',
                 'techno', 'work-out'],
        'chill': ['ambient', 'chill', 'rainy-day', 'sleep', 'trance'],
        'main character': ['anime', 'disney', 'movies', 'indie', 'indie-pop', 'opera',
                           'pop-film', 'show-tunes', 'soundtracks'],
        'cultural': ['afrobeat', 'bluegrass', 'bossanova', 'brazil', 'british', 'cantopop',
                     'dancehall', 'folk', 'french', 'german', 'gospel', 'indian', 'iranian',
                     'latin', 'latino', 'malay', 'mandopop', 'mpb', 'pagode', 'philippines-opm',
                     'reggae', 'reggaeton', 'salsa', 'samba', 'sertanejo', 'ska', 'spanish',
                     'swedish', 'tango', 'turkish', 'world-music'],
        'neutral': ['alternative', 'new-release', 'rockabilly', 'r-n-b', 'rock-n-roll',
                    'singer-songwriter', 'songwriter', 'synth-pop', 'trip-hop']
    }
    artists_to_delete = []
    for artist, info in artists_info.items():
        if not any(genre in mood_dict[mood_keyword] for genre in info['genres']):
            artists_to_delete.append(artist)
    
    if len(artists_to_delete) != len(artists_info):
        for artist in artists_to_delete:
            del artists_info[artist]

def get_user_spotify_id(auth_header):
    url = 'https://api.spotify.com/v1/me'
    result = requests.get(url, headers=auth_header)
    return result.json()['id']

def create_new_playlist(user_id, token) -> tuple:
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    auth_header = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'name': '~~mood~~',
        'description': 'A new curated playlist unique for you based on your mood!',
        'public': False
    })
    result = requests.post(url, headers=auth_header, data=data)
    playlist_id = result.json()['id']
    playlist_uri = result.json()['uri']
    return playlist_id, playlist_uri

def playlist_add_songs(playlist_id, playlist_uri, songs_uri, token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    auth_header = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    data = json.dumps(songs_uri)
    result = requests.post(url, headers=auth_header, data=data)

def get_similar_artists_top_songs(artists, auth_header):
    song_info = []
    for info in artists.values():
        id = info['id']
        url = f'https://api.spotify.com/v1/artists/{id}/related-artists'
        result = requests.get(url, headers=auth_header)
        five_similar_artists = result.json()['artists'][:4]
        for artists in five_similar_artists:
            artist_id = artists['id']
            url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'
            result = requests.get(url, headers=auth_header)
            random_index = random.randint(0, len(result.json()['tracks']) - 1)
            print('Artist name:', artists['name'])
            print('Artist id:', artist_id)
            print('Song:', result.json()['tracks'][random_index]['name'])
            print('Song uri:', result.json()['tracks'][random_index]['uri'])
            print()
            song_uri = result.json()['tracks'][random_index]['uri']
            if song_uri not in song_info:
                song_info.append(song_uri)
    return song_info


if __name__ == '__main__':
    app.run(port=8000)