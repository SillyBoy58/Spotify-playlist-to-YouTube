# 100% FREE YouTube → Spotify Playlist Transfer Tool  
*(One-way only. No support for other platforms.)*

Still using:  
`tunemymusic.com`, `soundiiz.com`, etc.? 🤮🤮🤮🤮🤮  
**USE THIS INSTEAD** 😎😎😎😎😎😎

---

## ✅ PROS:

- **100% ACCURATE:** Uses ISRC codes to match tracks precisely (local songs may vary). 🤯  
- **NO LIMITS:** Everything runs locally on your system, no usage caps. 😲  
- **NO FEES OR SUBSCRIPTIONS:** Self-hosted, so there's nothing to pay. 💯💰💸  
- **NO SPOTIFY LOGINS REQUIRED:** Transfers from public playlists only, so your credentials stay private. 😱  
- **FULLY OPEN-SOURCE:** duh 🙄  
- **CACHES YOUTUBE VIDEO IDs:** If a song has already been transferred, it reuses the result instead of fetching again.

---

## ❌ CONS:

- No music videos: Transfers typically link to audio tracks, not official music videos.  
- Public playlists only: The Spotify playlist must be public during transfer (you can change it back afterward).  
- Requires a YouTube login to create playlists.  
- **Spotify Dev & YouTube Data API Setup Required** to avoid rate limits.

---

## ⚙️ REQUIREMENTS:

1. A YouTube account and a Spotify account with a playlist (obviously)  
2. Spotify Developer App ([Tutorial](https://developer.spotify.com/documentation/web-api))  *You only need the "Getting started" part*
3. YouTube Data API ([Tutorial](https://developers.google.com/youtube/v3/getting-started))  
   Or use my short-hand version:  
   - Go to [Google Cloud Console](https://console.developers.google.com)  
   - Create a new project (or use an existing one)  
   - Enable the YouTube Data API v3  
   - Go to APIs & Services > Credentials  
   - Create OAuth 2.0 Client ID (choose Desktop App)  
   - Download the `client_secret_XXX.json` file  
   - Rename it to `YouTube_client_info.json`  
   - Place it in the same directory as `main.py`  
   - Add the Google account (used to transfer playlists) to the **Test users** list under OAuth settings
4. All of the required Python libraries installed (pip install *xyz*)
5. [yt-dlp](https://github.com/yt-dlp/yt-dlp) - I could've used the official YouTube API for search queries and it would be much faster, but I didn't to use up less units

---

## 🟥 !!!! DO NOT SHARE:
``token.json``

``Spotify_client_info.json``

``YouTube_client_info.json``

...unless you 100% trust the person you're sending it to!

---

## 📌 Additional Notes:
1. Accuracy might not be 100% with locally added songs.

2. ISRC (International Standard Recording Code): A unique identifier used by music distributors. It enables accurate cross-platform matching between YouTube and Spotify.

3. Rate Limits: YouTube API allows 10,000 units per day on the free plan.

    Rough estimate:
    
    1 track = 50 units
    
    199 tracks = 9,950 units
    
    Playlist creation = 50 units
    
    So about 200 songs/day max under default quota.
    [Learn more](https://developers.google.com/youtube/v3/determine_quota_cost)
