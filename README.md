100% FREE YouTube -> Spotify Playlist Transfer Tool
*(One-way only. No support for other platforms.)*

Still using:
    tunemymusic.com, soundiiz.com ect.? 🤮🤮🤮🤮🤮
USE THIS INSTEAD 😎😎😎😎😎😎

PROS:
    100% ACCURATE: Uses ISRC codes* to match tracks precisely (local songs may vary). 🤯🤯🤯🤯🤯🤯
    NO LIMITS: Everything runs locally on your system, no usage caps. (excluding your YouTube Data API limits(10,000 per day if using the free plan))😲😲😲😲😲😲
    NO FEES OR SUBSCRIPTIONS: Self-hosted, so there's nothing to pay. 💯💯💯💰💰💰💸💸💸🤑
    NO SPOTIFY LOGINS REQUIRED: Transfers from public playlists only, so your account credentials stay private. 😱😱😱😱😱😱
    FULLY OPEN-SOURCE: duh 🙄🙄🙄🙄🙄🙄

CONS:
    No music videos: Transfers typically link to audio tracks, not official music videos.
    Public playlists only: The Spotify playlist must be public during transfer (you can change it back afterward).
    Requires a YouTube log-in as it is impossible to create playlists on your account without proper access.
    Spotify Dev & YouTube Data API Setup Required: You’ll need to create your own Spotify Developer App & YouTube Data API to avoid rate limits.

REQUIREMENTS:
    1. A YouTube account and a Spotify account with a playlist (obviously),
    2. Spotify Developer App ([Tutorial](https://developer.spotify.com/documentation/web-api))
    3. YouTube Data API ([Tutorial](https://developers.google.com/youtube/v3/getting-started)) Or use my short-hand version (because I found the UX to be terrible when following the official tutorial):
        3.1. Go to [Google Cloud Console](https://console.developers.google.com)
        3.2. Create a new project (or use an existing one)
        3.3. Enable the YouTube Data API v3
        3.4. Go to APIs & Services > Credentials
        3.5. Create OAuth 2.0 Client ID (choose Desktop App)
        3.6. Download the client_secret_XXX.json file
        3.7. Rename it to YouTube_client_info.json
        3.8. Place it in the same directory as 'main.py'
        3.9. Make sure to add the google account (from which you will be transfering the YouTube playlist) to the Test users list (which is in APIs & Services > Credentials > OAuth 2.0 Client IDs > Audience > Test users > + Add users > Type in the gmail)
    4. All of the required Python libraries installed (pip install <library>)

🟥 !!!! DO NOT SHARE YOUR "token.json", "Spotify_client_info.json" or "YouTube_client_info.json" UNLESS YOU 100% TRUST THE PERSON YOURE SENDING IT TO !!!! 🟥

*
ISRC (International Standard Recording Code):
    This is a unique identifier used by music distributors (like DistroKid, Vevo, etc.) when uploading tracks. It allows accurate cross-platform identification of songs - YouTube and Spotify included - by matching this metadata.