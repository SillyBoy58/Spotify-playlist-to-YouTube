import get_spotify
import post_youtube

def main():
    playlist_tracks = get_spotify.main()
    response = post_youtube.main(playlist_tracks)
    if response == 69420:
        print("A little boo boo happened in the code and now your playlist is lost into the abyss ;(")
    else:
        print("Congratulations on successfully transfering your playlist!")

if __name__ == "__main__":
    main()