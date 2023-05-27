from dotenv import load_dotenv
import os
import requests
import base64
import json


def get_token(client_id, client_secret):
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def search_for_keyword(token, keyword):
    auth_header = {'Authorization': 'Bearer ' + token}
    url = 'https://api.spotify.com/v1/search'
    query = f'?q={keyword}&type=track&limit=5'

    query_url = url + query
    result = requests.get(query_url, headers=auth_header)
    print(result)
    json_result = json.loads(result.content)
    print(json_result)


"""def get_top_10_tracks(token):
    auth_header = {'Authorization': 'Bearer ' + token}
    # modify me in url to get user's spotify information
    url = 'https://api.spotify.com/v1/me/top/artists'
    msg = '?medium_term='
    result = requests.get(url,
                           params = {
                               'time_range': 'medium_term',
                               'limit': 10,
                           },
                          headers=auth_header)
    print(result.json())"""
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



def run():
    load_dotenv()

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    token = get_token(client_id, client_secret)
    # get_top_10_tracks(token)
    search_for_keyword(token, 'stray kids')


def main():
    run()

if __name__ == "__main__":
    main()