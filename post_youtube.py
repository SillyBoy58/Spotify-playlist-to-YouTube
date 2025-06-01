import os
import html
import json
import time

from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import googleapiclient.errors

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

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        for track in playlist_tracks:
            query = track.get('ISRC') or track.get('Name', '')
            if not query:
                track['Video_ID'] = None
                continue

            if query in cache:
                track['Video_ID'] = cache[query]
                continue
            
            safe_query = query.replace('"', '\\"')
            try:
                result = ydl.extract_info(f'ytsearch1:"{safe_query}"', download=False)
                entries = result['entries'] if 'entries' in result else []
                video_id = entries[0]['id'] if entries else None
            except Exception as e:
                print(f"[yt-dlp error] {query}: {e}")
                video_id = None

            track['Video_ID'] = video_id
            cache[query] = video_id
            print(f"Fetched '{track['Name']}' → https://www.youtube.com/watch?v={video_id}" if video_id else f"🔴🔴 Failed to find video for '{query}' 🔴🔴")
            
    save_cache(cache)
    return playlist_tracks

def create_playlist():
    while True:
        title = input("Enter your playlist's name (max 150 chars): ")
        if 0 < len(title) <= 150:
            break
        print("Error: Title must be 1-150 characters long. Please try again.")

    while True:
        description = input("Enter your playlist's description (max 5000 chars): ")
        if len(description) <= 5000:
            description = description.strip() if description.strip() else ""
            break
        print("Error: Description must be 0-5000 characters long. Please try again.")

    valid_visibilities = {"priv": "private", "pub": "public", "unl": "unlisted"}
    while True:
        visibility_input = input("Enter playlist visibility ['priv']ate, ['pub']lic, ['unl']isted: ").lower()
        if visibility_input in valid_visibilities:
            visibility = valid_visibilities[visibility_input]
            break
        print("Error: Invalid visibility option. Please enter 'priv', 'pub', or 'unl'.")

    safe_title = html.escape(title)
    snippet = {
        "title": safe_title,
        "description": description
    }

    try:
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": snippet,
                "status": {
                    "privacyStatus": visibility
                }
            }
        )
        response = request.execute()
        print("Playlist created successfully!")
    except Exception as e:
        print("API Error:", e)
        return None

    return response['id']

def select_playlist(): # Lists the playlist using the YouTube API or lets the user enter the URL manually
    while True:
        choice = input("Do you want to list playlist 'man'ually or with 'yt-api' (automatic, uses 1 unit)?: ").strip().lower()
        
        if choice == 'yt-api':
            request = youtube.playlists().list(
                part="snippet,contentDetails",
                maxResults=25,
                mine=True
            )
            response = request.execute()

            playlists = response.get("items", [])
            if not playlists:
                print("No playlists found.")
                return None

            print("\nYour playlists:")
            for i, playlist in enumerate(playlists, 1):
                title = playlist['snippet']['title']
                count = playlist['contentDetails']['itemCount']
                print(f"{i}. {title} ({count} videos)")
         
            while True:
                try:
                    selection = int(input("\nSelect a playlist number: "))
                    if 1 <= selection <= len(playlists):
                        playlist_id = playlists[selection - 1]['id']
                        return playlist_id
                    else:
                        print("Invalid number. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
        
        elif choice == 'man':
            playlist_url = input("Enter the playlist URL: ").strip()
            try:
                playlist_id = parse_qs(urlparse(playlist_url).query)["list"][0]
                return playlist_id
            except Exception as e:
                print("Invalid URL. Please try again.")
        
        else:
            print("Wrong input! Choose only 'man' or 'yt-api'")

def insert_tracks(playlist_id, playlist_tracks):
    for track in playlist_tracks:
        video_id = track['Video_ID']
        if not video_id:
            print(f"🔴🔴 Skipping track '{track.get('Name', 'Unknown')}' — no video ID found. 🔴🔴")
            continue
        
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
                }
            }
            }
        )
        try:
            response = request.execute()
            video_id = response['snippet']['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"Added '{track['Name']}' to the playlist. Video URL: {video_url}.")
        except Exception as e:
            print(f"Failed to add '{track['Name']}' ({video_id}): {e}")
            time.sleep(0.5)
            continue

def main(playlist_tracks):
    global youtube
    print("Authenticating...")
    youtube = get_authenticated_youtube()
    print("Authentication successful!")

    print("Working on getting the songs' video IDs...")
    playlist_tracks = get_youtube_id(playlist_tracks)

    while True:
        response = input("Create a new playlist ['1'] or choose an existing one? ['2']: ").strip().lower()
        if response == '1':
            print("Creating playlist...")
            playlist_id = create_playlist()
            if not playlist_id:
                print("Playlist creation failed. Aborting track insertion.")
                return 69420
            break
        if response == '2':
            playlist_id = select_playlist()
            break
        else:
            print("Invalid input! Choose only ['1'] or ['2']")

    print("Adding the tracks to the playlist...")
    insert_tracks(playlist_id, playlist_tracks)
    print("Added tracks successfully!")



# TO DO:

# Update playlist with videos using video url || DONE NOT TESTED
# Create multiple google project's automatically or something