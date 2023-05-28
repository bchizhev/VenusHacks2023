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
# REDIRECT_URI = 'http://localhost:5000'

@app.route('/')
def index():
    return '<a href="/login">Log in with Spotify</a>'

@app.route('/login')
def login():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-read-private user-read-email user-top-read',
    }
    authorize_url = f'{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}'
    # print(authorize_url.access_token)
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
    # Handle the response and retrieve the access token
    # You can save the access token in a session or a database for further use
    resp = response.json()

    print(resp['access_token'])
    return redirect('http://localhost:5500/FrontEnd/?token=' + resp['access_token'])

@app.route('/topTenTracks', methods=['POST'])
def get_top_10_tracks():
    token = json.loads(request.data)['authToken']
    auth_header = {'Authorization': 'Bearer ' + token}
    # modify me in url to get user's spotify information
    url = 'https://api.spotify.com/v1/me/top/artists'
    msg = '?time_range=medium_term&limit=10&offset=5'
    try: 
        result = requests.get(url,
                            #    params = {
                            #        'time_range': 'medium_term',
                            #        'limit': 10,
                            #        'offset': 5
                            #    },
                          headers=auth_header)
    except e:
        print(e)
    """print(result)
    print('RESULTS:',len(result.json()['items']))
    print('RESULTS:', result.json()['items'][0])
    print('RESULTS:', result.json()['items'][0]['name'])
    print('RESULTS:', result.json()['items'][0]['id'])"""
    artists_to_id = extract_artists(result)
    return jsonify(result.json())
    # json_result = json.loads(result.content)
    # print(json_result)

def extract_artists(result) -> dict:
    artist_to_id = {}
    for index in range(len(result.json()['items'])):
        id_dict = {'id': result.json()['items'][index]['id']}
        artist_to_id[result.json()['items'][index]['name']] = id_dict
    """print(artist_to_id)
    for artist, id in artist_to_id.items():
        print('Artist:', artist)
        print('Information:', id)
        print()"""
    return artist_to_id


if __name__ == '__main__':
    app.run(port=8000)