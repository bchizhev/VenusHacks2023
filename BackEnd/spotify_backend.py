import os
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify
import requests
import urllib
import json
from flask_cors import CORS

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

    print(resp['access_token'])
    return redirect('http://localhost:5500/FrontEnd/?token=' + resp['access_token'])

@app.route('/topTenTracks', methods=['POST'])
def get_top_10_tracks():
    token = json.loads(request.data)['authToken']
    auth_header = {'Authorization': 'Bearer ' + token}
    url = 'https://api.spotify.com/v1/me/top/artists'
    result = requests.get(url, headers=auth_header)

    artists_info = extract_artist_info(result)
    user_id = get_user_spotify_id(auth_header)
    similar_songs = get_similar_artists_top_songs(artists_info, auth_header)
    # playlist_id, playlist_uri = create_new_playlist(user_id, token)
    # print(result.json()['items'][0])
    # artists_info['Stray Kids']
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
    for artist, info in artists_info.items():
        if mood_keyword not in info['genres']:
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

def get_similar_artists_top_songs(artists, auth_header):
    song_info = []
    print(artists)
    for artist, info in artists.items():
        # print(info['id'])
        id = info['id']
        # print(artist, info['id'])
        url = f'https://api.spotify.com/v1/artists/{id}/related-artists'
        result = requests.get(url, headers=auth_header)
        # print(result)
        five_similar_artists = result.json()['artists'][:4]
        for artists in five_similar_artists:
            artist_id = artists['id']
            url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'
            result = requests.get(url, headers=auth_header)
            # print(artist)
            
            print('Artist name:', artists['name'])
            print('Artist id:', artist_id)
            print('Song:', result.json()['tracks'][0]['name'])
            print('Song uri:', result.json()['tracks'][0]['uri'])
            print()
            song_uri = result.json()['tracks'][0]['uri']
            if song_uri not in song_info:
                song_info.append(song_uri)
    return song_info

def get_artist_top_song(artist_id, auth_header):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'



if __name__ == '__main__':
    app.run(port=8000)