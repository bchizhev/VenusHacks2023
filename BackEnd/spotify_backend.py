# app.py
import os
from dotenv import load_dotenv
from flask import Flask, redirect, request
import requests
import urllib
import json

app = Flask(__name__)
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
        'scope': 'user-read-private user-read-email',
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
    url = 'https://api.spotify.com/v1/me/top/tracks'
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
    print(result.data)
    return ""
    # json_result = json.loads(result.content)
    # print(json_result)

    """if result.status_code == 200:
        data = result.json()
        # Process the data as needed
        print(data)
    else:
        print('Error:', result.status_code)"""
    """auth_header = {'Authorization': 'Bearer ' + token}
    # modify me to get user's spotify information
    url = 'https://api.spotify.com/v1/me/top/tracks'
    # query = f'?offset=1&limit=10'
    query_url = url
    result = requests.get(query_url, headers = auth_header)
    json_result = json.loads(result.content)
    print(json_result)"""


if __name__ == '__main__':
    app.run(port=8000)