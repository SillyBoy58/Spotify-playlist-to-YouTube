import requests
import json
from urllib.parse import urlparse

base_url = "https://api.spotify.com/v1"
playlist_tracks = []

def get_client_info(): # Asks the user to input the Spotify App IDs
    try:
        with open("Spotify_client_info.json", 'r') as f:
            data = json.load(f)
            client_id = data['client_id']
            client_secret = data['client_secret']
    
    except FileNotFoundError:
        with open("Spotify_client_info.json", 'w') as f:
            client_id = input('Enter Spotify App client ID: ')
            client_secret = input("Enter Spotify App client secret: ")
            secrets = {
                'client_id': client_id,
                'client_secret': client_secret
            }
            json.dump(secrets, f)

    return client_id, client_secret

def get_spotify_access_token(client_id, client_secret): # Gets the access token
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def get_playlist_info(): # Gets playlist_tracks
    playlist_url = fr'{base_url}/playlists/{playlist_id}/tracks'
    print(f"Checking: {playlist_url}...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(playlist_url, headers=headers)
    if response.ok:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)
        return

    while True:
        response = input("Do you want to also try fetching local tracks? (Results might not be accurate) ['y', 'n']: ")
        if response == 'y':
            get_local_tracks = True
            break
        elif response == 'n':
            get_local_tracks = False
            break
        else:
            print("Wrong input! Type 'y' or 'n' only!")

    for item in data['items']:       
        track = item['track']
        track_name = track['name']

        if item['is_local']:
            if get_local_tracks:
                playlist_tracks.append({
                    'Name': track_name,
                    'Status': 'local'
                })
            continue

        track_ISRC = track['external_ids']['isrc']
        track_artist_names = []
        for artist in track['artists']:
            track_artist_names.append(artist['name'])

        # print(f"Got: {', '.join(track_artist_names)} - '{track_name}', with ISRC {track_ISRC}...")
        playlist_tracks.append({
            'Name': track_name, 
            'Artists': ', '.join(track_artist_names), 
            'ISRC': track_ISRC,
            'Status': 'online'
        })

def main():
    global playlist_id, access_token
    playlist_url = input("Enter the spotify playlist URL: ")
    path = urlparse(playlist_url).path
    playlist_id = path.split('/')[-1]

    client_id, client_secret = get_client_info()
    access_token = get_spotify_access_token(client_id, client_secret)
    get_playlist_info()

    return playlist_tracks