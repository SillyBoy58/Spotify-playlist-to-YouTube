import get_spotify
import post_youtube

def main():
    while True:
        playlist_tracks = get_spotify.main()
        post_youtube.main(playlist_tracks)

        while True:
            response = input("Do you want to transfer another playlist? ['y', 'n']: ").lower().strip()
            if response == 'y':
                break
            elif response == 'n':
                return
            else:
                print("Wrong input! Type 'y' or 'n' only!")

if __name__ == "__main__":
    main()