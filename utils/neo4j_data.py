import requests
from decouple import config

token = config('TOKEN')

def fetch_web_api(endpoint, method, body=None):
    url = f'https://api.spotify.com/{endpoint}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    if method.upper() == 'GET':
        response = requests.get(url, headers=headers)
    elif method.upper() == 'POST':
        response = requests.post(url, headers=headers, json=body)
    else:
        raise ValueError("Unsupported HTTP method")
    
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.json()['error']['message']}")
    
    return response.json()

def get_top_tracks():
    return fetch_web_api('v1/me/top/tracks?time_range=long_term&limit=20', 'GET')['items']

def get_artist_data(uri):
    return fetch_web_api(uri, 'GET')

def get_album_data(uri):
    return fetch_web_api(uri, 'GET')

def get_trimmed_uri(uri):
    start_index = uri.find('v1')
    return uri[start_index:]



def main():
    try:
        top_tracks = get_top_tracks()
        track_data = []
        for track in top_tracks:
            artist_uri = track['artists'][0]['href']
            album_uri = track['album']['href']

            artist_data = get_artist_data(get_trimmed_uri(artist_uri))
            album_data = get_album_data(get_trimmed_uri(album_uri))

            artist = {
                'name': artist_data['name'],
                'genres': artist_data['genres'],
                'popularity': artist_data['popularity']
            }

            album = {
                'name': album_data['name'],
                'release_date': album_data['release_date'],
                'total_tracks': album_data['total_tracks'],
                'tracks': [
                    {
                        'name': album_track['name'],
                        'artist_name': [artist['name'] for artist in album_track['artists']]
                    }
                    for album_track in album_data['tracks']['items']
                ]
            }

            track_data.append({
                'famous_track': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'release_date': track['album']['release_date'],
                'artist_data': artist,
                'album_data': album
            })

        print(track_data)


    except Exception as error:
        print(error)
