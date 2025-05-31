import os
import subprocess
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CACHE_FILE = "yt_id_cache.json"

def get_authenticated_youtube(): # Get access to user profile
    creds = None

    if os.path.exists("token.json"):
        with open("token.json", "r") as token_file:
            creds_data = json.load(token_file)
            creds = Credentials.from_authorized_user_info(info=creds_data, scopes=SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("YouTube_client_info.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_youtube_id(playlist_tracks): # Uses yt-dlp to get a lot of metadata then uses jq to process the json
    cache = load_cache()

    for playlist_track in playlist_tracks:
        track_ISRC = playlist_track.get('ISRC')
        if track_ISRC:
            query = track_ISRC
        else:
            track_name = playlist_track.get('Name', '')
            if not track_name.strip():
                playlist_track['Video_ID'] = None
                continue
            query = track_name

        if query in cache:
            playlist_track['Video_ID'] = cache[query]
            continue

        safe_query = query.replace('"', '\\"')
        cmd = [
            "yt-dlp",
            f'ytsearch1:"{safe_query}"',
            "--skip-download",
            "--no-warnings",
            "--quiet",
            "--print", "id"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            video_id = None
        else:
            video_id = result.stdout.strip() or None

        playlist_track['Video_ID'] = video_id
        cache[query] = video_id
        print(f"Fetched {playlist_track['Name']}. Video url: https://www.youtube.com/watch?v={video_id}")
        
    save_cache(cache)
    return playlist_tracks

def main(playlist_tracks):
    youtube = get_authenticated_youtube()
    print("Authentication successful!")

    print("Working on getting the songs...")
    playlist_tracks = get_youtube_id(playlist_tracks)
    print(playlist_tracks)

# TO DO:
# Create playlist
# Update playlist with videos using video url
# Edit playlist name ect.